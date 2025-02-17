from typing import Union

from requests import Response

from autotests_coverage.config import EnvConfig
from autotests_coverage.results_writers.openapi_schemas_manager import (
    OpenApiSchemasManager,
)
from autotests_coverage.results_writers.swagger_schemas_manager import (
    SwaggerSchemasManager,
)
from autotests_coverage.uri import URI


class RequestSchemaHandler:
    def __init__(self, uri: URI, method: str, response: Response, kwargs: dict):
        self.__manager = self.__get_manager(uri, method, response, kwargs)

    @staticmethod
    def __get_manager(uri, method, response, kwargs) -> Union[SwaggerSchemasManager, OpenApiSchemasManager]:
        variables = EnvConfig.get_variables()

        if variables.api_docs_type == "swagger":
            return SwaggerSchemasManager(uri, method, response, kwargs)

        return OpenApiSchemasManager(uri, method, response, kwargs)

    def write_schema(self):
        self.__manager.write_schema()
