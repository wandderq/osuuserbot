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

import tomllib
from argparse import Namespace
from pathlib import Path

# getting & checking config file
_config_path = Path('bot/osuuserbot.toml')
if not _config_path.exists():
    raise FileNotFoundError('osuuserbot.toml not found!')


# loading config
with _config_path.open(mode='rb') as file:
    _config = tomllib.load(file)


# setting variables
telegram = Namespace(
    api_id=_config['telegram']['api_id'],
    api_hash=_config['telegram']['api_hash'],
    bot_token=_config['telegram']['bot_token']
)

osu = Namespace(
    client_id=_config['osu']['client_id'],
    client_secret=_config['osu']['client_secret']
)