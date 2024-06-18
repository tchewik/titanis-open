from isanlp import PipelineCommon
from isanlp.processor_remote import ProcessorRemote

from .base_docker_extractor import BaseDockerExtractor


class FeaturesRST(BaseDockerExtractor):
    PORT = 3136

    def __init__(self, host, *args):
        super().__init__(host=host)

        self.pipeline = PipelineCommon([(
            ProcessorRemote(host=host, port=self.PORT, pipeline_name='default'),
            ['text',],
            {'rst': 'rst'}
        )])

    def __call__(self, text):
        return self.pipeline(text)
