from abc import ABC
from dataclasses import dataclass

from .base_features_extractor import BaseFeaturesExtractor


@dataclass
class BaseDockerExtractor(BaseFeaturesExtractor, ABC):
    PORT: str

    def __init__(self, host: str):
        super().__init__()
        self.host = host
