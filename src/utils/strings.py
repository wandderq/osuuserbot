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
from pathlib import Path

import yaml
from jinja2 import Template

# checking strings file
strings_path = Path('res/strings.yml').absolute()
if not strings_path.exists():
    raise FileNotFoundError('res/strings.yml not found!')

# loading strings
with strings_path.open(encoding='utf-8') as file:
    strings = yaml.safe_load(file)


# main functions
def get_text(lang: str, key: str, **kwargs) -> str:
    raw_template = strings.get(lang, {}).get(key, "")
    return Template(raw_template).render(**kwargs)


def get_flag_emoji(country_code: str) -> str:
    if not country_code or len(country_code) != 2:
        return "🏳"
    
    return "".join(
        chr(ord(char.upper()) + 0x1F1A5)
        for char in country_code
    )