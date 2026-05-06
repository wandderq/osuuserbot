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

