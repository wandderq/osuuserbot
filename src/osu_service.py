import logging as lg

from aiolimiter import AsyncLimiter
from cachetools import TTLCache
from ossapi import OssapiAsync

import config


class OsuService:
    def __init__(self):
        self.osuapi = OssapiAsync(
            client_id=config.osu.app_id,
            client_secret=config.osu.app_secret
        )

        self.limiter = AsyncLimiter(max_rate=20, time_period=1)
        self.cache = TTLCache(maxsize=1000, ttl=300)
        self.logger = lg.getLogger('osuuserbot.osu_service')
    

    async def get_user(self, user_val: str | int):
        if user_val in self.cache:
            self.logger.debug(f'using cached result for user: \'{user_val}\'')
            return self.cache[user_val]
        
        async with self.limiter:
            try:
                self.logger.debug(f'requesting user info for \'{user_val}\'')
                user = await self.osuapi.user(user_val)
                self.cache[user_val] = user
                return user
            
            except Exception as e:
                self.logger.error(f'Error requesting to osu!api: {str(e)}')
                return None

osu_service = OsuService()