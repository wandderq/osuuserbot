import re

from ossapi import User


def is_valid_osu_username(username):
    if not (3 <= len(username) <= 15):
        return False

    pattern = r'^[a-zA-Z0-9_\[\]\- ]+$'
    
    return bool(re.match(pattern, username))


def is_valid_osu_user_id(user_id):
    if isinstance(user_id, str):
        if not user_id.isdigit():
            return False
        user_id = int(user_id)
    
    return isinstance(user_id, int) and user_id > 0


def get_flag_emoji(country_code: str) -> str:
    if not country_code or len(country_code) != 2:
        return "🏳️"
    
    return "".join(chr(ord(char.upper()) + 127397) for char in country_code)


def format_user_info(user: User) -> str:
    uname = user.username
    uid = user.id
    online = user.is_online
    mode = user.playmode if not user.playmode == 'osu' else 'standard'

    rank_global = user.statistics.global_rank
    rank_local = user.statistics.country_rank

    pp = round(user.statistics.pp)
    acc = round(user.statistics.accuracy * 100, 2)
    level = user.statistics.level.current
    ss = user.statistics.grade_counts.ss
    s = user.statistics.grade_counts.s
    a = user.statistics.grade_counts.a

    playtime_h = round(user.statistics.play_time / 3600, 1)
    playcount = user.statistics.play_count

    user_link = f"https://osu.ppy.sh/users/{uid}"
    status = "🟢 Online" if online else "🔴 Offline"
    flag_emoji = get_flag_emoji(user.country_code)

    user_info =  f"**[{uname}]({user_link})** - **{status}**\n"
    user_info += f"osu!**{mode}** - **#{rank_global}**"
    user_info += f" (**{flag_emoji} #{rank_local}**)\n\n"

    user_info += create_text_table(
        (3, 2),
        [
            f"**{pp}**pp", f"**{acc}%**", f"Lv. **{level}**",
            f"SS: **{ss}**", f"S: **{s}**", f"A: **{a}**"
        ]
    ) + '\n'

    user_info += f"Playime: **{playtime_h}h** | "
    user_info += f"Playcount: **{playcount}**"

    return user_info


def create_text_table(dimensions, items):
    cols, rows = dimensions
    if len(items) != cols * rows:
        raise ValueError(f"Invalid items count: {len(items)} (expected: {cols*rows})")

    str_items = [str(item) for item in items]
    matrix = [str_items[i * cols:(i + 1) * cols] for i in range(rows)]

    col_widths = [0] * cols
    for j in range(cols):
        max_width = 0
        for i in range(rows):
            max_width = max(max_width, len(matrix[i][j]))
        col_widths[j] = max_width

    lines = []
    for i in range(rows):
        row_cells = []
        for j in range(cols):
            cell = matrix[i][j].ljust(col_widths[j])
            row_cells.append(cell)
        lines.append(" | ".join(row_cells))

    return "\n".join(lines)


async def respond_invalid_format(event, query):
    response = event.builder.article(
        title='Invalid format',
        description=f'Invalid username or id: \'{query}\'',
        text='Invalid username or id: \'{query}\''
    )
    await event.answer([response], cache_time=3000)


async def respond_user_not_found(event, user_val):
    response = event.builder.article(
        title='User not found',
        description=f'User \'{user_val}\' not found!',
        text=f'User \'{user_val}\' not found!'
    )
    await event.answer([response], cache_time=3000)


async def respond_user_info(event, user: User):
    user_info = format_user_info(user)

    response = event.builder.article(
        title=user.username,
        description=f"{user.country.name.capitalize()}, {user.statistics.pp}pp",
        text=user_info,
        parse_mode='md'
    )

    await event.answer([response], cache_time=60)