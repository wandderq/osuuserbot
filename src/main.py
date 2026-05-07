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
import sys

from telethon import TelegramClient, events

import config
import utils
from logger import setup_logger
from osu_service import osu_service

client = TelegramClient('osuuserbot.session', config.telegram.api_id, config.telegram.api_hash)
logger = setup_logger('osuuserbot')


@client.on(events.InlineQuery)
async def inline_handler(event):
    query = event.query.query.strip()
    if not query: return

    # validating query
    if utils.is_valid_osu_user_id(query):
        user_val = int(query)
    elif utils.is_valid_osu_username(query):
        user_val = query
    else:
        return await utils.respond_invalid_format(event, query)
    
    # getting user
    user = await osu_service.get_user(user_val)
    if not user:
        return await utils.respond_user_not_found(event, user_val)
    
    # responding with user info
    return await utils.respond_user_info(event, user)


@client.on(events.NewMessage(pattern='/about'))
async def about_handler(event):
    me_username = await client.get_me().username
    await event.reply(f"""🤖 About {me_username}
Author: **wandderq** (2026)
This bot is free software. In accordance with the **GNU AGPLv3** license, the source code of this bot is open and available for inspection or improvement.
📦 Source Code: https://github.com/wandderq/osuuserbot
You have the right to distribute and modify this code, provided that your changes also remain open-source under the AGPLv3 license.""")


async def main():
    logger.info('starting bot client')
    await client.start(bot_token=config.telegram.bot_token)

    me = await client.get_me()

    logger.info(f'@{me.username}/{me.id} started')
    await client.run_until_disconnected()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    
    except KeyboardInterrupt:
        print('\nKeyboardInterrupt')
        sys.exit(0)

