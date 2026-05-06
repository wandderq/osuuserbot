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