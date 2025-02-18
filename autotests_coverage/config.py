import os
from pathlib import Path

from pydantic import BaseModel, ValidationError, field_validator
from functools import lru_cache


class EnvConfig(BaseModel):
    tmp_configs_dir: str
    api_docs_type: str
    api_docs_version: str
    api_docs_format: str
    debug_mode: bool
    coverage_reports_dir: str
    coverage_configs_dir: str

    @classmethod
    @lru_cache(maxsize=None)
    def get_variables(cls) -> "EnvConfig":
        try:
            return cls(
                tmp_configs_dir=os.path.join(Path(__file__).parent, "tmp_configs_dir"),
                api_docs_type=os.environ.get("API_DOCS_TYPE", default="openapi"),
                api_docs_version=os.environ.get("API_DOCS_VERSION", default="3.0.0"),
                api_docs_format=os.environ.get("API_DOCS_FORMAT", default="json"),
                debug_mode=os.environ.get("DEBUG_MODE", default=False),
                coverage_reports_dir=os.environ.get("COVERAGE_REPORTS_DIR"),
                coverage_configs_dir=os.environ.get("COVERAGE_CONFIGS_DIR")
            )
        except ValidationError as e:
            raise ValueError(f"Ошибка валидации конфигурации: {e}")

    @field_validator("coverage_reports_dir", "coverage_configs_dir")
    def check_not_none(cls, value):
        if value is None:
            raise ValueError("Значение не может быть None")
        return value
