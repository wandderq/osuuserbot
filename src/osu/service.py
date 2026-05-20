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

from aiolimiter import AsyncLimiter
from cachetools import TTLCache
from ossapi import OssapiAsync

from utils import config


class OsuService:
    def __init__(self):
        self.osuapi = OssapiAsync(
            client_id=config.osu['client_id'],
            client_secret=config.osu['client_secret']
        )

        self.limiter = AsyncLimiter(
            max_rate=config.osu['service']['max_request_rate'],
            time_period=1
        )
        self.cache = TTLCache(
            maxsize=config.osu['service']['ttlcache']['max_size'],
            ttl=config.osu['service']['ttlcache']['ttl']
        )
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