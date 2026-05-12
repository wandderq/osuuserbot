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

import asyncio
import logging as lg
import sys
from pathlib import Path

from telethon import TelegramClient
from telethon.events import InlineQuery, NewMessage

from utils import config, setup_logging

# logging setup
setup_logging()
logger = lg.getLogger('osuuserbot')


# telegram bot client
client = TelegramClient(
    Path('bot/telegram.session').absolute(),
    config.telegram.api_id,
    config.telegram.api_hash
)


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


# main function
async def main():
    logger.info('starting bot client')
    await client.start(bot_token=config.telegram.bot_token)

    logger.info('bot started')
    await client.run_until_disconnected()


# entry point
if __name__ == '__main__':
    try:
        asyncio.run(main())
        sys.exit(0)
    
    except KeyboardInterrupt:
        print("\n\033[32mInterrupted\033[0m")
        sys.exit(0)

    except Exception as e:
        print(f"\033[32m{e.__class__.__name__}\033[0m: {str(e)}")
        sys.exit(1)
