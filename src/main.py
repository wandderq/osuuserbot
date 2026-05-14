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

from telethon import TelegramClient, connection
from telethon.events import InlineQuery, NewMessage

from utils import config, get_text, is_valid_osu_user_id, is_valid_osu_username, setup_logging
from bot.responses import respond_invalid_format, respond_user_not_found

# logging setup
setup_logging()
logger = lg.getLogger('osuuserbot')

proxy_params = {
    'connection': connection.ConnectionTcpMTProxyRandomizedIntermediate,
    'proxy': (
        config.mtproxy.server,
        config.mtproxy.port,
        config.mtproxy.secret,
    )
} if config.mtproxy is not None else {}

client = TelegramClient(
    Path('bot/telegram.session').absolute(),
    config.telegram.api_id,
    config.telegram.api_hash,
    **proxy_params
)


# bot handlers
@client.on(NewMessage(pattern='/start'))
async def start_handler(event):
    await event.respond(
        get_text(
            'en', 'start'
        ),
        parse_mode='html'
    )


@client.on(NewMessage(pattern='/about'))
async def about_handler(event):
    await event.respond(
        get_text(
            'en', 'about',
            author=config.metadata.author,
            repo_url=config.metadata.repo_url
        ),
        parse_mode='html'
    )


@client.on(InlineQuery)
async def inline_handler(event):
    query = event.query.query.strip()
    if not query: return

    # validating query
    if is_valid_osu_user_id(query):
        user_val = int(query)
    elif is_valid_osu_username(query):
        user_val = query
    else:
        return await respond_invalid_format(event, query)
    
    

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
        print("\n\033[31mInterrupted\033[0m")
        sys.exit(0)

    except Exception as e:
        print(f"\033[31m{e.__class__.__name__}\033[0m: {str(e)}")
        sys.exit(1)
