# Copyright (C) 2026 wandderq
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://gnu.org>.

import logging as lg
import tomllib
from pathlib import Path

from utils.const import CONFIG_SCHEMA


class ConfigParseError(Exception):
    pass


class Config:
    def __init__(self):
        self.path = Path('config.toml').absolute()
        self.logger = lg.getLogger('osuuserbot.config-loader')
        self.schema = CONFIG_SCHEMA

        self._load()


    def _load(self):
        if not self.path.exists():
            raise ConfigParseError(f"Config file not found: {self.path}")
        
        # loading raw data
        try:
            with self.path.open(mode="rb") as file:
                data = tomllib.load(file)

            self.logger.info(f"Config loaded from {self.path}")

        except Exception as e:
            raise ConfigParseError(f"TOML parsing error: {str(e)}") from e
        
        # validating data
        self._validate_data(data)

        # applying validated data
        for table_name in self.schema:
            setattr(self, table_name, data.get(table_name))
    

    def _validate_data(self, data):
        for table_name, table_schema in self.schema.items():
            required = table_schema.get('required', False)
            exists = table_name in data

            if required and not exists:
                raise ConfigParseError(f'Missing required table [{table_name}]')
            
            if not exists:
                default = table_schema.get('default', {})
                data[table_name] = default
          
            table_data = data[table_name]
            table_datatype_name = type(table_data).__name__

            if table_data is None:
                self.logger.warning(f'skipping table: [{table_name}]')
                continue

            if not isinstance(table_data, dict):
                raise ConfigParseError(
                    f'{table_name} must be a table, '
                    f'got {table_datatype_name}'
                )
            
            self._validate_table(table_schema, table_data, table_name, required)


    def _validate_table(self, schema, data, path="", table_required=True):
        self.logger.debug(f'validating {path}')

        # parsing keywords
        expected_keywords = schema.get('keywords', {})

        for keyword_name, keyword_schema in expected_keywords.items():
            current_path = f"{path}.{keyword_name}" if path else keyword_name

            required = keyword_schema.get('required', False)
            default = keyword_schema.get('default')
            choices = keyword_schema.get('choices', None)
            expected_type = keyword_schema.get('type')

            key_exists = keyword_name in data

            self.logger.debug(f'validating {current_path}')

            if not key_exists:
                if required and table_required:
                    raise ConfigParseError(f'Missing required key: {current_path}')
                
                if default is not None:
                    data[keyword_name] = default
                    self.logger.warning(f'using default value for {current_path}: {default}')
                    key_exists = True
                
                else:
                    self.logger.warning(f'skipping unknown key: {current_path}')
                    continue

            if key_exists and expected_type is not None:
                value = data[keyword_name]
                value_type_name = type(value).__name__

                if not isinstance(value, expected_type):
                    try:
                        data[keyword_name] = expected_type(value)
                        self.logger.debug(
                            f'{current_path} converted from {value_type_name} '
                            f'to {expected_type.__name__}'
                        )
                    
                    except ValueError as e:
                        raise ConfigParseError(
                            f'{current_path} must be of type {expected_type.__name__} ',
                            f'got {value_type_name}'
                        ) from e

            if choices is not None and value not in choices:
                choices_str = ', '.join(choices)
                raise ConfigParseError(
                    f'Invalid value for {current_path}: {value}. '
                    f'Choose from: {choices_str}'
                )
        
        # parsing subtables
        subtables = schema.get('subtables', {})

        for subtable_name, subtable_schema in subtables.items():
            current_path = f"{path}.{subtable_name}" if path else subtable_name

            required = subtable_schema.get('required', False)
            subtable_exists = subtable_name in data

            if not subtable_exists:
                if required:
                    raise ConfigParseError(f'Missing required subtable [{current_path}]')
                
                else:
                    data[subtable_name] = {}
            
            subtable_data = data[subtable_name]
            subtable_datatype_name = type(subtable_data).__name__

            if not isinstance(subtable_data, dict):
                raise ConfigParseError(
                    f'{current_path} must be a table, '
                    f'got {subtable_datatype_name}'
                )
            
            self._validate_table(subtable_schema, subtable_data, current_path)



config = Config()
