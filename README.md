![python](https://img.shields.io/badge/python-3.7%2B-blue)
![license](https://img.shields.io/badge/license-MIT-green)

# autotests-coverage

Этот проект является форком оригинальной библиотеки 
[swagger-coverage-py](https://github.com/JamalZeynalov/swagger-coverage-py), с внесенными изменениями 
для улучшения функциональности. Основная цель библиотеки — оценить покрытие автотестами API на основе 
Swagger/OpenAPI спецификации.

### Основные изменения

- Добавлена возможность указания единого файла конфигурации для всех сервисов.
- Добавлена возможность указания папки с конфигурациями и папки для сгенерированных отчетов.
- Внесены изменения для корректной работы при использовании библиотеки pytest-xdist.

### 0. Установить зависимости:

* Python 3.7+
* Java JDK 11+ (с указанием переменной JAVA_HOME)

### 1. Установить пакет `autotests-coverage`

```shell
pip install swagger-coverage-metrics
```

### 2. Указать переменные

```dotenv
API_DOCS_TYPE="openapi" # Тип API документации. Возможные значения: "swagger", "openapi". По умолчанию указано "openapi".
API_DOCS_VERSION="3.0.0" # Версия API документации. По умолчанию указано "3.0.0".
API_DOCS_FORMAT="json" # Формат API документации. Возможные значения: "json", "yaml". По умолчанию указано "json".
DEBUG_MODE=False # Включение debug-режима. По умолчанию False.
COVERAGE_REPORTS_DIR="C:/repositories/project_name/coverage/reports" # Путь до папки, в которую будут сгенерированы отчеты.
COVERAGE_CONFIGS_DIR="C:/repositories/project_name/coverage/configs" # Пусть до папки, в которой хранятся файлы конфигураций.
```
**ВНИМАНИЕ:** Перед запуском тестов из директории, указанной в переменной "COVERAGE_REPORTS_DIR" будут удалены все данные!
Не нужно указывать в переменной директорию, в которой содержатся нужные данные.

### 3. Добавить трассировку всех вызовов API с помощью RequestSchemaHandler

```python
from autotests_coverage.request_schema_handler import RequestSchemaHandler
from autotests_coverage.uri import URI

def _send_requests(self, method, path, **kwargs):
    full_url = self.host + path
   
    rest_response = self.session.request(method=method, url=full_url, **kwargs)
        
    url = URI(
        host=self.host,
        base_path="",
        unformatted_path=path,
        uri_params=kwargs.get("params"),
    )
        
    RequestSchemaHandler(
        url, method.lower(), rest_response, kwargs
    ).write_schema()
        
    return rest_response
```

### 4. Добавить инициализацию отчетов

```python
import pytest
from autotests_coverage.reporter import CoverageReporter
from requests.auth import HTTPBasicAuth


@pytest.fixture(scope="session", autouse=True)
def setup_swagger_coverage():
    CoverageReporter.cleanup_input_files()
    
    reporter = CoverageReporter(
        api_name="petstore",
        host="https://petstore.swagger.io",
        coverage_config_file_name="base_config.json"
    )
    
    reporter.setup(
        path_to_swagger_json="/api/v1/resources/my_project/doc/swagger.json",
        auth=HTTPBasicAuth("username", "password")
    )

    yield
    
    reporter.generate_report()
```

#### Для снятия метрик нескольких сервисов добавьте инициализацию для каждого сервиса

```python
import pytest
from autotests_coverage.reporter import CoverageReporter
from requests.auth import HTTPBasicAuth


@pytest.fixture(scope="session", autouse=True)
def setup_swagger_coverage():
    CoverageReporter.cleanup_input_files()
    
    reporter1 = CoverageReporter(
        api_name="petstore",
        host="https://petstore.swagger.io",
        coverage_config_file_name="base_config.json"
    )
    
    reporter1.setup(
        path_to_swagger_json="/v2/swagger.json",
        auth=HTTPBasicAuth("username", "password")
    )

    reporter2 = CoverageReporter(
        api_name="my-project",
        host="http://my-project.com",
        coverage_config_file_name="my_project_config.json",
        use_custom_config=True
    )
    
    reporter2.setup(
        path_to_swagger_json="/api/v1/swagger.json",
        auth=HTTPBasicAuth("username", "password")
    )

    yield
    
    reporter1.generate_report()
    
    reporter2.generate_report()
```



> #### Шаги и параметры
> `api_name` - Определите имя API. Это имя будет использоваться для формирования отчета.
> Для API в этом примере будут сгенерированы отчеты с названиями "petstore-coverage.html" и "my-project-coverage.html".
>
> `host` - Хост API. Он будет использоваться для загрузки файла swagger.json и для определения выходной директории.
>
> `coverage_config_file_name` - Название файла с конфигурацией. Можно указать один и тот же файл конфигурации 
> для нескольких сервисов. Также можно указать кастомную конфигурацию для сервисов, но тогда 
> нужно указать значение True для параметра use_custom_config.
>
> `cleanup_input_files()` - этот метод удаляет все сгенерированные файлы в папке, указанной в переменной REPORTS_DIR.
>
> `path_to_swagger_json` — Вторая часть HTTP-ссылки на вашу документацию OpenAPI/Swagger в формате JSON.
> &nbsp;&nbsp;&nbsp;&nbsp; Адаптированный файл swagger-doc-<api_name>.json будет создан в директории, указанной в переменной REPORTS_DIR.
>
> `auth` - Параметр аутентификации для библиотеки requests. Не указывайте его, если ваш API не требует аутентификации.

### 5. Создайте и разместите файл(ы) swagger-coverage-config.json в вашем проекте

```json
{
    "rules": {
        "status": {
            "enable": true,
            "ignore": [
                "500"
            ],
            "filter": []
        },
        "paths": {
            "enable": true,
            "ignore": [
                "/user/{username}"
            ]
        },
        "only-declared-status": {
            "enable": false
        },
        "exclude-deprecated": {
            "enable": true
        }
    }
}
```
Раздел path предназначен для исключения определенных эндпоинтов (всех методов) из итогового HTML-отчета. 
Для этого нужно установить параметр enable в значение true и указать список эндпоинтов 
(как они отображаются в документации Swagger) в разделе ignore. Затем эти эндпоинты будут удалены из документации API 
перед сохранением локально.

Если вам нужно сделать кастомный файл конфигурации для сервисов, то создайте json-файл в папке с конфигурациями:

```json
{
    "rules": {
        "status": {
            "enable": true,
            "ignore": [
                "500",
                "401"
            ],
            "filter": []
        },
        "paths": {
            "enable": true,
            "ignore": [
                "/user/{username}"
            ]
        },
        "only-declared-status": {
            "enable": false
        },
        "exclude-deprecated": {
            "enable": true
        },
       "writers": {
        "html": {
            "locale": "ru",
            "filename": "swagger-coverage-report-petstore.html"
        }
    }
    }
}
```

И укажите название этого файла при инициализации отчета.
При этом нужно передать аргумент use_custom_config со значением True:

```python
import pytest
from autotests_coverage.reporter import CoverageReporter


@pytest.fixture(scope="session", autouse=True)
def setup_swagger_coverage():
    CoverageReporter.cleanup_input_files()
    
    reporter = CoverageReporter(
        api_name="petstore",
        host="https://petstore.swagger.io",
        coverage_config_file_name="my_custom_config.json",
        use_custom_config=True
    )
    
    reporter.setup(
        path_to_swagger_json="/api/v1/swagger.json"
    )

    yield
    
    reporter.generate_report()
```

Дополнительные примеры настроек конфигурации вы можете найти в разделе [Configuration options](https://github.com/JamalZeynalov/swagger-coverage#configuration-options) документации.

### 6. Запустите ваши тесты и откройте в браузере "<api_name>-coverage.html" отчет, созданный в директории "COVERAGE_REPORTS_DIR"

## Created by

[Jamal Zeinalov](https://github.com/JamalZeynalov)

## License

swagger-coverage-metrics распространяется под версией 2.0 [Apache License](http://www.apache.org/licenses/LICENSE-2.0)