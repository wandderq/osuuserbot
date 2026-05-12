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
from pathlib import Path

from telethon import TelegramClient
from telethon.events import InlineQuery, NewMessage

from utils import config

# setting up client & getting logger
client = TelegramClient(
    Path('bot/telegram.session').absolute(),
    config.telegram.api_id,
    config.telegram.api_hash
)
logger = lg.getLogger('osuuserbot.bot')


# bot handlers
@client.on(NewMessage(pattern='/start'))
async def start_handler(event):
    pass


@client.on(NewMessage(pattern='/about'))
async def about_handler(event):
    pass


@client.on(InlineQuery)
async def inline_handler(event):
    pass