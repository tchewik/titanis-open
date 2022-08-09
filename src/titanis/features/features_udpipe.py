from isanlp import PipelineCommon
from isanlp.processor_remote import ProcessorRemote
from isanlp.utils.parsing_by_paragraphs import parse_by_paragraphs

from .base_docker_extractor import BaseDockerExtractor

ISANLP_TEXT_LEN_CONSTRAINT = 40000


class FeaturesUDPipe(BaseDockerExtractor):
    PORT = 3134

    def __init__(self, host):
        super().__init__(host=host)
        self.pipeline = PipelineCommon([(
            ProcessorRemote(host=self.host, port=self.PORT, pipeline_name='0'),
            ['text'],
            {'sentences': 'sentences',
             'tokens': 'tokens',
             'lemma': 'lemma_ud',
             'syntax_dep_tree': 'syntax_dep_tree_ud',
             'postag': 'postag_ud'}
        )])

    def __call__(self, text) -> dict:
        if len(text) > ISANLP_TEXT_LEN_CONSTRAINT:
            return parse_by_paragraphs(text, self.pipeline)
        else:
            return self.pipeline(text)
