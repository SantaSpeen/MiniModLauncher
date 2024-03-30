import glob
import os
import sys
import zipfile
from datetime import datetime

from loguru import logger

from .core import Core

log_dir = Core.dir / "logs"
log_file = log_dir / "info.log"
os.makedirs(log_dir, exist_ok=True)
if os.path.exists(log_file):
    ftime = os.path.getmtime(log_file)
    index = 1
    while True:
        zip_path = log_dir / f"{datetime.fromtimestamp(ftime).strftime('%Y-%m-%d')}-{index}.zip"
        if not os.path.exists(zip_path):
            break
        index += 1
    with zipfile.ZipFile(zip_path, "w") as zipf:
        logs_files = glob.glob(f"{log_dir}/*.log")
        for file in logs_files:
            if os.path.exists(file):
                zipf.write(file, os.path.basename(file))
                os.remove(file)
logger.remove()
logger.add(log_file, level="INFO", backtrace=False, diagnose=False,
           format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {message}")
if sys.stdout:
    logger.add(sys.stdout, level="INFO", backtrace=False, diagnose=False,
               format="\r<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | {message}")
if Core.debug:
    logger.add(log_dir / "debug.log", level=0, backtrace=True, diagnose=True)
logger.success("Logger initialized.")
logger.info(f"Starting MiniModLauncher ({Core.__version__})..")
