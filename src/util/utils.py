import datetime
import logging
import os.path
from typing import TextIO

import discord

DEFAULT_LOG_FORMATTER = logging.Formatter(
    fmt="[{asctime}] [{levelname:<8}] {name}: {message}",
    datefmt="%Y-%m-%d %H:%M:%S",
    style="{",
)

_LOG_FILE_PATTERN = "%Y-%m-%d (%H-%M-%S %Z)"


def archive_old_log_files(logs_folder: str = "./logs") -> None:
    """Moves any log files in the provided folder into a subfolder

    Pattern:

    old/[year]/[year]-[month]/[files here]

    Example:
        .logs/...
    gets moved to:
        .logs/old/2026/2026-01/...
    """
    archive_path = os.path.join(logs_folder, "old")
    if not os.path.exists(archive_path):
        os.mkdir(archive_path)

    for filename in os.listdir(logs_folder):
        if filename.endswith(".log"):
            dt = datetime.datetime.strptime(filename.removesuffix(".log"), _LOG_FILE_PATTERN)
            year_path = os.path.join(archive_path, f"{dt.year}")
            if not os.path.exists(year_path):
                os.mkdir(year_path)

            year_month_path = os.path.join(year_path, f"{dt.year}-{dt.month:02}")
            if not os.path.exists(year_month_path):
                os.mkdir(year_month_path)

            os.rename(os.path.join(logs_folder, filename), os.path.join(year_month_path, filename))


def get_file_handler(
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
        now = datetime.datetime.now(datetime.UTC).replace(microsecond=0)
        date_str = now.strftime(_LOG_FILE_PATTERN)
    else:
        date_str = startup_time.strftime(_LOG_FILE_PATTERN)
    file_handler = logging.FileHandler(filename=f"{logs_folder.rstrip('/')}/{date_str}.log", encoding="utf-8", mode="w")
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    return file_handler


def get_stream_handler(
    formatter: logging.Formatter = DEFAULT_LOG_FORMATTER,
    level: int = logging.WARNING,
    stream: TextIO | None = None,
) -> logging.StreamHandler[TextIO]:
    """Adds a StreamHandler with the given stream (default: stderr) to the provided Logger with the given formatter and
    level (default: WARNING)"""
    stream_handler = logging.StreamHandler(stream)
    stream_handler.setLevel(level)  # will log to stderr, more immediately visible than file
    stream_handler.setFormatter(formatter)
    return stream_handler


def even_out_embed_fields(embed: discord.Embed) -> discord.Embed:
    """Evens out Embed fields to avoid a misaligned last row
    (does not account for inline=False being set on any field)"""
    if len(embed.fields) % 3 != 0:  # even out the last line of embed fields
        embed.add_field(name="\u200b", value="\u200b")
        if len(embed.fields) % 3 == 2:  # if we added one and still need one more to make it 3
            embed.add_field(name="\u200b", value="\u200b")
    return embed


def rint(value: int | float, digits: int = 2) -> int | float:
    """Round to [digits] (default: 2) digits. Returns int if rounded float has only zeroes after the decimal point."""
    rounded = round(value, digits)
    int_value = int(rounded)
    return int_value if rounded == int_value else rounded
