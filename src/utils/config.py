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


class ConfigParseError(Exception):
    pass


class Config:
    def __init__(self):
        self.path = Path('config.toml').absolute()
        self.logger = lg.getLogger('osuuserbot.config-loader')
        self.schema = {
            'telegram': {
                'required': True,
                'keywords': {
                    'api_id': {'required': True, 'type': int},
                    'api_hash': {'required': True, 'type': str},
                    'bot_token': {'required': True, 'type': str}
                }
            },
            'osu': {
                'required': True,
                'keywords': {
                    'client_id': {'required': True, 'type': int},
                    'client_secret': {'required': True, 'type': str}
                }
            },
            'metadata': {
                'required': True,
                'keywords': {
                    'bot_name': {'required': True, 'type': str},
                    'bot_username': {'required': True, 'type': str},
                    'source_code_url': {'required': True, 'type': str},
                    'author': {'required': True, 'type': str}
                }
            },
            'mtproxy': {
                'required': False,
                'keywords': {
                    'server': {'required': True, 'type': str},
                    'port': {'required': True, 'type': int},
                    'secret': {'required': True, 'type': str}
                }
            }
        }
        self._data = {}  # raw dict from toml

        for table_name in self.schema:
            setattr(self, table_name, None)


    def load(self) -> None:
        if not self.path.exists():
            cwd_str = str(Path.cwd())
            raise ConfigParseError(f"Config file not found in {cwd_str}!")
        
        # trying to load config
        try:
            with self.path.open(mode="rb") as file:
                self._data = tomllib.load(file)

        except Exception as e:
            raise ConfigParseError(f"Failed to parse TOML: {str(e)}") from e
        
        # validating config
        self._validate()
        
        # saving config to attributes
        for table_name, _ in self.schema.items():
            if table_name in self._data:
                setattr(self, table_name, self._data[table_name])
            else:
                setattr(self, table_name, None)
        
        self.logger.info(f"Config was successfully loaded from {self.path}")


    def _validate(self) -> None:
        for table_name, table_schema in self.schema.items():
            table_required = table_schema.get('required', False)
            table_present = table_name in self._data
            
            if table_required and not table_present:
                raise ConfigParseError(f"Required table [{table_name}] is missing!")

            if not table_present:
                continue
            
            table_data = self._data[table_name]
            if not isinstance(table_data, dict):
                raise ConfigParseError(
                    f"\'{table_name}\' should be table (dict), "
                    f"but it\'s {type(table_data).__name__}"
                )
            
            # validating keys
            keywords_schema = table_schema.get('keywords', {})

            for kw_name, kw_schema in keywords_schema.items():
                kw_required = kw_schema.get('required', False)
                kw_present = kw_name in table_data
                
                if kw_required and not kw_present:
                    raise ConfigParseError(
                        f"Required key {kw_name} is missing in the [{table_name}]"
                    )
                if not kw_present:
                    continue
                
                # checking type
                expected_type = kw_schema.get('type')
                if expected_type is not None:
                    actual_value = table_data[kw_name]
                    if not isinstance(actual_value, expected_type):
                        raise ConfigParseError(
                            f"Key {table_name}.{kw_name} should be "
                            f"{expected_type.__name__}, but it\'s {type(actual_value).__name__}"
                        )
            
            allowed_keys = set(keywords_schema.keys())
            extra_keys = set(table_data.keys()) - allowed_keys
            if extra_keys:
                self.logger.warning(
                    f"[{table_name}] contains extra keysr: {extra_keys}"
                )

config = Config()
config.load()