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

from utils.logging import setup_logging

setup_logging()

from utils.checks import is_valid_osu_user_id, is_valid_osu_username  # noqa: E402
from utils.config import config  # noqa: E402
from utils.const import CONFIG_SCHEMA, CONNECTIONS  # noqa: E402
from utils.strings import get_flag_emoji, get_text  # noqa: E402

__all__ = [
    'config',
    'is_valid_osu_user_id',
    'is_valid_osu_username',
    'setup_logging',
    'get_text',
    'get_flag_emoji',
    'CONNECTIONS',
    'CONFIG_SCHEMA'
]
