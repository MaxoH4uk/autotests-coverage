from typing import Union

from requests import Response

from autotests_coverage.configs import API_DOCS_TYPE
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
        if API_DOCS_TYPE == "swagger":
            return SwaggerSchemasManager(uri, method, response, kwargs)

        return OpenApiSchemasManager(uri, method, response, kwargs)

    def write_schema(self):
        self.__manager.write_schema()
