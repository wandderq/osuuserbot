import tomllib
from argparse import Namespace
from pathlib import Path

# setting & checking config path
config_path = Path('osuuserbot.toml').absolute()

if not config_path.exists():
    raise FileNotFoundError(f'config file was not found! ({str(config_path)})')


# loading config
with config_path.open(mode='rb') as file:
    config = tomllib.load(file)


# setting variables
telegram = Namespace(
    api_id=config['telegram']['api_id'],
    api_hash=config['telegram']['api_hash'],
    bot_token=config['telegram']['bot_token'],
)

osu = Namespace(
    app_id=config['osu']['app_id'],
    app_secret=config['osu']['app_secret'],
)