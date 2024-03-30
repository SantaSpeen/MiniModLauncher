import os
import sys
from configparser import ConfigParser
from pathlib import Path

from loguru import logger

parser = ConfigParser()


class Core:

    debug = False
    __version__ = '0.0.1'
    dir = Path("./MiniModLauncher")

    def __init__(self):
        self.run = False
        self.config_file = self.dir / "config.ini"

    @staticmethod
    def format_bytes(size):
        power = 2 ** 10
        n = 0
        units = {0: 'B', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
        while size > power:
            size /= power
            n += 1
        return f"{size:.2f}{units[n]}"

    @staticmethod
    def format_time(seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        remaining_seconds = seconds % 60

        result = ""
        if hours > 0:
            result += f"{int(hours)}h "
        if minutes > 0:
            result += f"{int(minutes)}min "
        if remaining_seconds > 0:
            result += f"{int(remaining_seconds)}sec"

        return result.strip()

    @staticmethod
    def format_speed(file_size_bytes, time_seconds):
        logger.debug(f"{file_size_bytes=}; {time_seconds=}")
        if time_seconds == 0 or time_seconds == 0.0:
            time_seconds = 0.1
        speed_bps = file_size_bytes / time_seconds
        if speed_bps >= 1024 ** 3:
            speed = speed_bps / (1024 ** 3)
            unit = 'GB/s'
        elif speed_bps >= 1024 ** 2:
            speed = speed_bps / (1024 ** 2)
            unit = 'MB/s'
        elif speed_bps >= 1024:
            speed = speed_bps / 1024
            unit = 'KB/s'
        else:
            speed = speed_bps
            unit = 'B/s'
        return f"{speed:.2f}{unit}"

    def exit_with_error(self, s, err=None):
        self.run = False
        logger.error(s)
        if err:
            logger.exception(err)
        input(f"\n\nPress Enter to exit..")
        sys.exit(1)

    def _config_setup(self):
        if os.path.isfile(self.dir):
            os.remove(self.dir)
        if not os.path.exists(self.dir):
            os.mkdir(self.dir)

        if not os.path.exists(self.config_file):
            parser.add_section('auth')
            parser.set('auth', "token", "0")
            parser.add_section('general')
            parser.set('general', "lang", "en")
            parser.add_section('minecraft')
            parser.set('minecraft', "dot minecraft", "0")
            parser.set('minecraft', 'start exe', "0")
            parser.add_section('history')
            parser.set('history', 'last', "0")
            with open(self.config_file, "w", encoding="utf-8-sig") as f:
                parser.write(f)
        parser.read(self.config_file, "utf-8-sig")
        _needed = [
            ['minecraft', 'dot minecraft'],
            ['minecraft', 'start exe'],
        ]
        bad = False
        for i in _needed:
            if not parser.has_option(*i):
                logger.error(f'[{i[0]}] {i[1]} not in configuration file!')
                bad = True
        if bad:
            self.exit_with_error(f"Bad configuration file: {self.config_file!r}")
        else:
            logger.success("Configuration file is OK!")

    def start(self):
        self._config_setup()

    def stop(self):
        pass
