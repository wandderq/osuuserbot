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

import yaml
from jinja2 import Template

with open("strings.yml", encoding='utf-8') as file:
    strings = yaml.safe_load(file)


def get_text(lang: str, key: str, **kwargs) -> str:
    raw_template = strings.get(lang, {}).get(key, "")
    return Template(raw_template).render(**kwargs)
