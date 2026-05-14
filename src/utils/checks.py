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

import re

valid_osu_username_pattern = re.compile(r'^[a-zA-Z0-9_\[\]\- ]+$')


def is_valid_osu_username(query: str):
    if not (3 <= len(query) <= 15):
        return False

    return bool(valid_osu_username_pattern.match(query))


def is_valid_osu_user_id(query: str):
    if isinstance(query, str):
        if not query.isdigit():
            return False
        query = int(query)
    
    return isinstance(query, int) and query > 0

