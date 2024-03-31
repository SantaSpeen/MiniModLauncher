from loguru import logger
import argparse

from MiniModLauncher import core

parser = argparse.ArgumentParser(description='KuiToi-Server - BeamingDrive server compatible with BeamMP clients!')
parser.add_argument('-v', '--version', action="store_true", help='Print version and exit.', default=False)
parser.add_argument('-c', '--config', help='Path to config file.', nargs='?', default=None, type=str)
parser.add_argument('-l', '--language', help='Setting localisation.', nargs='?', default=None, type=str)
parser.add_argument('-C', '--code', help='ModPack code, they downloaded to dir in config.', nargs='?', default=None, type=str)
parser.add_argument('-U', '--upload', help='Path to modpack (mods, config)', nargs='?', default=None, type=str)
parser.add_argument('-A', '--token', help='Token for upload modpack.', nargs='?', default=None, type=str)

if __name__ == '__main__':

    try:
        core.start()
    except KeyboardInterrupt:
        pass
    except SystemExit as e:
        raise e
    except Exception as e:
        logger.exception(e)
    finally:
        core.stop()
