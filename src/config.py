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

# setting & checking config path
config_path = Path('osuuserbot.toml').absolute()

if not config_path.exists():
    raise FileNotFoundError(f'config file was not found! ({str(config_path)})')


# loading config
with config_path.open(mode='rb') as file:
    config = tomllib.load(file)


# setting variables
telegram = Namespace(
    api_id=config['telegram']['api_id'],
    api_hash=config['telegram']['api_hash'],
    bot_token=config['telegram']['bot_token'],
)

osu = Namespace(
    app_id=config['osu']['app_id'],
    app_secret=config['osu']['app_secret'],
)