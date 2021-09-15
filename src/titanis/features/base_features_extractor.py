from abc import (
    ABC,
    abstractmethod
)


class BaseFeaturesExtractor(ABC):
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def __call__(self, *args, **kwargs):
        raise NotImplementedError


class DummyFeaturesExtractor(BaseFeaturesExtractor):
    def __call__(self, text):
        return {'text': text}
