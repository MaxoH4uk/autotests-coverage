import os
from pathlib import Path


TMP_CONFIGS_DIR = os.path.join(Path(__file__).parent, "tmp_configs_dir")
API_DOCS_TYPE = os.environ.get("API_DOCS_TYPE", default="openapi")  # "swagger"
API_DOCS_VERSION = os.environ.get("API_DOCS_VERSION", default="3.0.0")  # "2.0"
API_DOCS_FORMAT = os.environ.get("API_DOCS_FORMAT", default="json")  # "yaml"
COVERAGE_REPORTS_DIR = os.environ.get("COVERAGE_REPORTS_DIR")
COVERAGE_CONFIGS_DIR = os.environ.get("COVERAGE_CONFIGS_DIR")
DEBUG_MODE = os.environ.get("DEBUG_MODE", default=False)  # Set to True to see commandline output

if COVERAGE_REPORTS_DIR is None:
    raise ValueError("Укажите значение переменной 'COVERAGE_REPORTS_DIR'.")

if COVERAGE_CONFIGS_DIR is None:
    raise ValueError("Укажите значение переменной 'COVERAGE_CONFIGS_DIR'.")
