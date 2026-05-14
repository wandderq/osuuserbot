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

async def respond_invalid_format(event, query: str):
    response = event.builder.article(
        title='Invalid format',
        description=f'Invalid username or ID: \'{query}\'',
        text=f'Invalid username or ID: \'{query}\''
    )
    await event.answer([response], cache_time=3000)


async def respond_user_not_found(event, user_val: str | int):
    response = event.builder.article(
        title='User not found',
        description=f'User \'{user_val}\' not found!',
        text=f'User \'{user_val}\' not found!'
    )
    await event.answer([response], cache_time=3000)
