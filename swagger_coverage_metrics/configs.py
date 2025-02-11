import os
from pathlib import Path

from environs import Env

import rootpath
from dotenv import load_dotenv

load_dotenv(f"{rootpath.detect()}/.env")
env = Env()

TMP_CONFIGS_DIR = os.path.join(Path(__file__).parent, "tmp_configs_dir")

API_DOCS_TYPE = env.str("API_DOCS_TYPE", default="openapi")  # "swagger"
API_DOCS_VERSION = env.str("API_DOCS_VERSION", default="3.0.0")  # "2.0"
API_DOCS_FORMAT = env.str("API_DOCS_FORMAT", default="json")  # "yaml"
DEBUG_MODE = env.bool("DEBUG_MODE", default=False)  # Set to True to see commandline output
REPORTS_DIR = env.str("REPORTS_DIR", default=None)
CONFIGS_DIR = env.str("CONFIGS_DIR", default=None)

if REPORTS_DIR is None:
    raise ValueError(f"Укажите значение переменной {REPORTS_DIR}.")

if CONFIGS_DIR is None:
    raise ValueError(f"Укажите значение переменной {CONFIGS_DIR}.")
