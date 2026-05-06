import re
from ossapi import User


USER_INFO_TEMPLATE = """{username} 
"""


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


def format_user_info(user: User) -> str:
    pass
