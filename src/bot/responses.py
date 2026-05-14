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

import html

from ossapi import User

from utils import get_flag_emoji, get_text


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


async def respond_user_info(event, user: User):
    user_id = user.id
    user_name = html.escape(user.username)
    status_emoji = "🟢" if user.is_online else "🔴"

    play_mode = user.playmode if not user.playmode == 'osu' else 'standard'
    rank_global = str(user.statistics.global_rank) if user.statistics.global_rank is not None else '-'
    flag_emoji = get_flag_emoji(user.country_code)
    rank_local = str(user.statistics.country_rank) if user.statistics.country_rank is not None else '-'

    pp = round(user.statistics.pp)
    accuracy = round(user.statistics.accuracy * 100, 3)
    level = user.statistics.level.current

    ss_count = user.statistics.grade_counts.ss
    s_count = user.statistics.grade_counts.s
    a_count = user.statistics.grade_counts.a

    play_time = round(user.statistics.play_time / 3600, 1)
    play_count = user.statistics.play_count

    text = get_text(
        'en', 'user-info',

        user_id=user_id, user_name=user_name, status_emoji=status_emoji,
        play_mode=play_mode, rank_global=rank_global, flag_emoji=flag_emoji,
        rank_local=rank_local, pp=pp, accuracy=accuracy, level=level,
        ss_count=ss_count, s_count=s_count, a_count=a_count,
        play_time=play_time, play_count=play_count
    )

    response = event.builder.article(
        title=user_name,
        description=f'#{rank_global} • {pp}pp',
        text=text,
        parse_mode='html'
    )
    await event.answer([response], cache_time=120)
    