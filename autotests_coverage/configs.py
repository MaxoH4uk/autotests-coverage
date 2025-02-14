import os
from pathlib import Path


TMP_CONFIGS_DIR = os.path.join(Path(__file__).parent, "tmp_configs_dir")

API_DOCS_TYPE = os.environ.get("API_DOCS_TYPE", default="openapi")
API_DOCS_VERSION = os.environ.get("API_DOCS_VERSION", default="3.0.0")
API_DOCS_FORMAT = os.environ.get("API_DOCS_FORMAT", default="json")
DEBUG_MODE = os.environ.get("DEBUG_MODE", default=False)

COVERAGE_REPORTS_DIR = os.environ.get("COVERAGE_REPORTS_DIR")
COVERAGE_CONFIGS_DIR = os.environ.get("COVERAGE_CONFIGS_DIR")
