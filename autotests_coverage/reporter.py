import json
import os
import platform
import re
import shutil
import subprocess
from pathlib import Path
from typing import List

import requests
from filelock import FileLock

from swagger_coverage_metrics.configs import (
    API_DOCS_FORMAT,
    DEBUG_MODE,
    COVERAGE_REPORTS_DIR,
    COVERAGE_CONFIGS_DIR,
    TMP_CONFIGS_DIR
)
from swagger_coverage_metrics.docs_writers.api_doc_writer import write_api_doc_to_file


class CoverageReporter:
    def __init__(
        self,
        api_name: str,
        host: str,
        coverage_config_file_name: str,
        use_custom_config: bool = False,
        verify: bool = True
    ):
        self.host = host
        self.verify = verify
        self.output_dir = self.__get_output_dir(host=self.host)
        self.swagger_doc_file = f"{COVERAGE_REPORTS_DIR}/swagger-doc-{api_name}.{API_DOCS_FORMAT}"

        if not use_custom_config:
            self.coverage_config_file_path = self.__copy_config_file_to_tmp_dir(
                file_path=os.path.join(COVERAGE_CONFIGS_DIR, coverage_config_file_name),
                api_name=api_name
            )

        else:
            self.coverage_config_file_path = os.path.join(COVERAGE_CONFIGS_DIR, coverage_config_file_name)

        self.ignored_paths = self.__get_ignored_paths_from_config()

    def __copy_config_file_to_tmp_dir(self, file_path: str, api_name: str):
        tmp_file_path = os.path.join(TMP_CONFIGS_DIR, f"swagger-coverage-config-{api_name}.json")

        lock_path = file_path + ".lock"
        lock = FileLock(lock_path)

        with lock:
            if not os.path.isfile(tmp_file_path):
                tmp_file_path = shutil.copy(
                    file_path, os.path.join(
                        TMP_CONFIGS_DIR, f"swagger-coverage-config-{api_name}.json"
                    )
                )

                with open(tmp_file_path, "r+", encoding="utf-8") as f:
                    file_data = json.load(f)

                file_data["writers"] = {
                    "html": {
                        "locale": "ru",
                        "filename": f"{COVERAGE_REPORTS_DIR}/{api_name}-coverage.html"
                    }
                }

                with open(tmp_file_path, 'w', encoding='utf-8') as f:
                    json.dump(file_data, f, indent=2, ensure_ascii=False)

            return tmp_file_path

    @staticmethod
    def __get_output_dir(host: str):
        subdir = re.match(r"(^\w*)://(.*)", host).group(2)

        output_dir = os.path.join(str(COVERAGE_REPORTS_DIR), subdir)

        if not os.path.exists(output_dir):
            Path(output_dir).mkdir(parents=True, exist_ok=True)

        return os.path.join(str(COVERAGE_REPORTS_DIR), subdir)

    def __get_ignored_paths_from_config(self) -> List[str]:
        """
        Reads the swagger-coverage-config-<api_name>.json file and returns
        a list of endpoints/paths to exclude from the report
        """
        paths_to_ignore = []

        with open(self.coverage_config_file_path, "r") as file:
            data = json.load(file)
            paths = data.get("rules").get("paths", {})

            if paths.get("enable", False):
                paths_to_ignore = paths.get("ignore")

        return paths_to_ignore

    def setup(self, path_to_swagger_json: str, auth: object = None, cookies: dict = None):
        """
        Setup all required attributes to generate report

        :param path_to_swagger_json: The relative URL path to the swagger.json (example: "/docs/api")
        :param auth: Authentication object acceptable by "requests" library
        :param cookies: Cookies dictionary. (Usage example: set this to bypass Okta auth locally)

        """
        link_to_swagger_json = f"{self.host}{path_to_swagger_json}"

        response = requests.get(
            link_to_swagger_json, auth=auth, cookies=cookies, verify=self.verify
        )

        assert response.ok, (
            f"Swagger doc is not pulled. See details: "
            f"{response.status_code} {response.request.url}"
            f"{response.content}\n{response.content}"
        )

        write_api_doc_to_file(
            self.swagger_doc_file,
            api_doc_data=response,
            paths_to_delete=self.ignored_paths,
        )

    def generate_report(self):
        inner_location = "swagger-coverage-commandline/bin/swagger-coverage-commandline"

        cmd_path = os.path.join(os.path.dirname(__file__), inner_location)

        assert Path(cmd_path).exists(), f"No commandline tools is found in following locations:\n{cmd_path}\n"

        if platform.system() == "Windows":
            cmd_path_with_ext = f"{cmd_path}.bat"

            assert Path(cmd_path_with_ext).exists(), f"File not found: {cmd_path_with_ext}"

            command = [cmd_path_with_ext, "-s", self.swagger_doc_file, "-i", self.output_dir]

        else:
            command = [cmd_path, "-s", self.swagger_doc_file, "-i", self.output_dir]

        if self.coverage_config_file_path:
            command.extend(["-c", self.coverage_config_file_path])

        # Suppress all output if not in debug mode
        if not DEBUG_MODE:
            with open(os.devnull, 'w') as devnull:
                subprocess.run(command, stdout=devnull, stderr=devnull)
        else:
            subprocess.run(command)

    @staticmethod
    def cleanup_input_files():
        if not os.path.exists(COVERAGE_REPORTS_DIR):
            return

        for item in os.listdir(COVERAGE_REPORTS_DIR):
            item_path = os.path.join(COVERAGE_REPORTS_DIR, item)

            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path, ignore_errors=True)

        shutil.rmtree(TMP_CONFIGS_DIR, ignore_errors=True)

        if not os.path.exists(TMP_CONFIGS_DIR):
            Path(TMP_CONFIGS_DIR).mkdir(parents=True, exist_ok=True)
