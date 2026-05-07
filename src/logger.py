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
import sys

from colorlog import ColoredFormatter


def setup_logger(name: str) -> lg.Logger:
    stream_handler = lg.StreamHandler(stream=sys.stdout)
    stream_handler.setFormatter(ColoredFormatter(
        fmt="[{name} {log_color}{levelname}{reset}]: {message}",
        style='{',
        log_colors={
            'DEBUG': 'blue',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROr': 'red',
            'CRITICAL': 'red'
        }

    ))

    lg.basicConfig(
        level=lg.DEBUG,
        handlers=[stream_handler]
    )

    return lg.getLogger(name)