from .base_features_extractor import BaseFeaturesExtractor
import requests
from typing import List, Dict, Optional


class EmotiveSRLFeaturesExtractor(BaseFeaturesExtractor):
    def __init__(self, host: str, port: int = 8081, **kwargs):
        self.host = host
        self.port = port

    def __get_clauses_from_rst(self, rst) -> List[str]:
        clauses = []
        if isinstance(rst, list):
            queue = rst
        else:
            queue = [rst]
        while queue:
            node = queue.pop()
            if node.left is not None:
                queue.append(node.left)

            if node.right is not None:
                queue.append(node.right)

            if node.relation == "elementary":
                clauses.append(node.text)

        return clauses

    def __call__(self, rst: Optional[List]) -> Dict:
        if rst is None:
            return {}
        else:
            clauses = self.__get_clauses_from_rst(rst)

        response = requests.post(
            f'http://{self.host}:{self.port}/predict',
            json=clauses,
            headers={'Content-Type': 'application/json'},
        )

        if response.status_code == 200:
            return response.json()
