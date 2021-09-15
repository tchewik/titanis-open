from .base_classifier import BaseClassifier


class ClassifierFrustration(BaseClassifier):
    PORT = 3137

    def __init__(self, host: str):
        super().__init__(host=host)

    def __call__(self, text) -> dict:
        return self._get_request({'text': text})
