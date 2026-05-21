<h2 align="center"><b>osuuserbot</b></h2>
<p align="center">
  <a href="https://github.com/wandderq/osuuserbot/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/wandderq/osuuserbot?color=blue" alt="License">
  </a>
  <a href="https://github.com/wandderq/osuuserbot/releases">
    <img src="https://img.shields.io/github/v/tag/wandderq/osuuserbot?label=version&color=green" alt="Version">
  </a>
  <a href="https://www.python.org/downloads/release/python-3120/">
    <img src="https://img.shields.io/badge/python-3.12-blue.svg" alt="Python 3.12">
  </a>
  <a href="https://github.com/astral-sh/uv">
    <img src="https://img.shields.io/badge/uv-package%20manager-purple" alt="uv">
  </a>

</p>

**osuuserbot** is a Telegram bot that displays brief player stats for [**osu!**](https://osu.ppy.sh)

The bot works primarily in *inline mode*, allowing you to quickly send stats in any chat.

### Features
- Display brief user stats: `@osuuserbot peppy`

### Running your own instance

```bash
# Clone the repository
git clone https://github.com/wandderq/osuuserbot.git
cd osuuserbot

# Create virtual env and install dependencies
uv venv && uv sync

# Set up configuration
cp example_config.toml config.toml

# Edit config.toml with your bot token and other settings
$EDITOR config.toml

# Run project
uv run src/main.py
```
The bot should now be up and responding to inline queries.

### Tech stack
- **Python 3.12**
- **Telethon** - Telegram API library

*The full dependencies list is available in [pyproject.toml](https://github.com/wandderq/osuuserbot/blob/main/pyproject.toml)*

### Licensing
Copyright (c) 2026 wandderq
This project is distributed under the **GNU AGPLv3** license.
The full license text is available in the **[LICENSE](https://github.com/wandderq/osuuserbot/blob/main/LICENSE)** file.

**tl;dr:** *Anyone who modifies the code of this bot and runs their own version (for example, another Telegram bot with similar logic) must publish the source code of their modifications under the same AGPLv3 license.*
