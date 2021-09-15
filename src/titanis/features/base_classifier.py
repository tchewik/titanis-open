import json
from abc import ABC

import requests

from .base_docker_extractor import BaseDockerExtractor


class BaseClassifier(BaseDockerExtractor, ABC):
    def _get_request(self, input_data: dict) -> dict:
        headers = {'Content-type': 'application/json'}
        url = f"http://{self.host}:{self.PORT}/"
        response = requests.post(url, headers=headers, data=json.dumps(input_data))
        result = json.loads(response.text)
        return result
