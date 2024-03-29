from loguru import logger

from mml import Core

if __name__ == '__main__':
    core = Core()
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
