import datetime
import logging
from typing import TextIO

import discord
import mariadb  # type: ignore

DEFAULT_LOG_FORMATTER = logging.Formatter(
    fmt="[{asctime}] [{levelname:<8}] {name}: {message}",
    datefmt="%Y-%m-%d %H:%M:%S",
    style="{",
)


def add_file_logging(
    logger: logging.Logger,
    formatter: logging.Formatter = DEFAULT_LOG_FORMATTER,
    level: int = logging.INFO,
    logs_folder: str = "./logs",
    startup_time: datetime.datetime | None = None,
) -> logging.FileHandler:
    """Adds a FileHandler to the provided Logger with the given formatter and level (default: INFO) and returns it
    for future use.

    The created log file will be named after the startup_time and reside in the **./logs/** folder by default.

    If no startup_time is provided, it will be generated based on the time of calling this method."""
    if startup_time is None:
        now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
        date_str = now.strftime("%Y-%m-%d (%H-%M-%S %Z)")
    else:
        date_str = startup_time.strftime("%Y-%m-%d (%H-%M-%S %Z)")
    file_handler = logging.FileHandler(filename=f"{logs_folder.rstrip('/')}/{date_str}.log", encoding="utf-8", mode="w")
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return file_handler


def add_stream_logging(
    logger: logging.Logger,
    formatter: logging.Formatter = DEFAULT_LOG_FORMATTER,
    level: int = logging.WARNING,
    stream: TextIO | None = None,
) -> None:
    """Adds a StreamHandler with the given stream (default: stderr) to the provided Logger with the given formatter and
    level (default: WARNING)"""
    stream_handler = logging.StreamHandler(stream)
    stream_handler.setLevel(level)  # will log to stderr, more immediately visible than file
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)


def even_out_embed_fields(embed: discord.Embed):
    """Evens out Embed fields to avoid a misaligned last row
    (does not account for inline=False being set on any field)"""
    if len(embed.fields) % 3 != 0:  # even out the last line of embed fields
        embed.add_field(name="\u200b", value="\u200b")
        if len(embed.fields) % 3 == 2:  # if we added one and still need one more to make it 3
            embed.add_field(name="\u200b", value="\u200b")
    return embed


def rint(value: int | float, digits: int = 2) -> int | float:
    """Round to [digits] (default: 2) digits. Returns int if rounded float has only zeroes after the decimal point."""
    return int_value if (rounded := round(value, digits)) == (int_value := int(rounded)) else rounded
