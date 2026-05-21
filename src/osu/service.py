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
from ossapi import OssapiAsync, User

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


    async def search_users(self, query: str | int) -> list[User] | None:
        cache_key = f"search_{str(query)}"
        if cache_key in self.cache:
            self.logger.debug(f'using cached search result for query: \'{query}\'')
            return self.cache[cache_key]

        async with self.limiter:
            try:
                self.logger.debug(f'searching users with query: \'{query}\'')
                result = await self.osuapi.search(str(query), mode="user")
                users = [
                    await user.expand()
                    for user in result.users.data[:5]
                ]
                self.cache[cache_key] = users
                return users

            except Exception as e:
                self.logger.error(f'Error searching users via osu!api: {str(e)}')
                return None

osu_service = OsuService()