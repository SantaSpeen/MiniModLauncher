import json
import os
import platform
import sys
from configparser import ConfigParser
from pathlib import Path

from loguru import logger

parser = ConfigParser()


class Core:
    debug = False
    __version__ = '0.0.2'
    __title__ = "MiniModLauncher"
    __build__ = 24
    dir = Path("./mml")

    def __init__(self, args):
        config_file = args.config
        if not config_file:
            config_file = self.dir / "config.ini"
        self.run = False
        self.config_file = config_file
        self._modpacks = {"count": 0}

        self.language = args.language
        self.code = args.code
        self.upload = args.upload
        self.token = args.token

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

    def _setup_config(self):
        if os.path.isfile(self.dir):
            os.remove(self.dir)
        if not os.path.exists(self.dir):
            os.mkdir(self.dir)

        if not os.path.exists(self.config_file):
            if platform.system() == "windows":
                ad = Path(os.getenv("AppData"))
            else:
                ad = Path(os.getenv("AppData"))
            parser.add_section('auth')
            parser.set('auth', "server", "https://mml.anidev.ru/")
            parser.set('auth', "token", "user")
            parser.add_section('general')
            parser.set('general', "lang", "en")
            parser.set('general', "temp", f"{self.dir / "modpacks"}")
            parser.add_section('minecraft')
            parser.set('minecraft', "mods", f"{ad / ".minecraft" / "mods"}")
            parser.set('minecraft', "config", f"{ad / ".minecraft" / "config"}")
            parser.set('minecraft', '.exe', "none")
            with open(self.config_file, "w", encoding="utf-8-sig") as f:
                parser.write(f)
        parser.read(self.config_file, "utf-8-sig")
        _needed = [
            ['auth', 'server'],
        ]
        bad = False
        for i in _needed:
            if not parser.has_option(*i):
                logger.error(f'[{i[0]}] {i[1]} not in configuration file!')
                bad = True
        if bad:
            self.exit_with_error(f"Bad configuration file: {self.config_file!r}")

        logger.success("Configuration file is OK!")
        self._modpacks_temp = Path(parser.get("general", "temp"))
        self._modpacks_info = self._modpacks_temp / "info.json"

        if not self.language:
            self.language = parser.get("general", "lang")
        if not self.token:
            self.token = parser.get("auth", "token")

    def _setup_modpacks(self):
        mods = Path(parser.get("minecraft", "mods"))
        config = Path(parser.get("minecraft", "config"))
        os.makedirs(self._modpacks_temp, exist_ok=True)
        os.makedirs(mods, exist_ok=True)
        os.makedirs(config, exist_ok=True)
        if not os.path.exists(self._modpacks_info):
            with open(self._modpacks_info, "w") as f:
                json.dump(self._modpacks, f, indent=2)

    def _setup_lang(self):
        # TODO: Get lang repo from API server and download needed lang, then setup it
        pass

    def start(self):
        self._setup_config()
        self._setup_modpacks()
        self._setup_lang()

    def stop(self):
        pass
