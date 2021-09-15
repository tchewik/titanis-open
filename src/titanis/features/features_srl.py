from isanlp import PipelineCommon
from isanlp.processor_remote import ProcessorRemote

from .base_docker_extractor import BaseDockerExtractor


class FeaturesSRL(BaseDockerExtractor):
    PORT = 3135

    def __init__(self, host: str):
        super().__init__(host=host)

        self.pipeline = PipelineCommon([(
            ProcessorRemote(host=self.host, port=self.PORT, pipeline_name='default'),
            ['tokens', 'postag_mys', 'morph_mys', 'lemma_ud', 'syntax_dep_tree_ud'],
            {'srl': 'srl_framebank'})
        ])

    def __call__(self, tokens, postag_mys, morph_mys, lemma_ud, syntax_dep_tree_ud) -> dict:
        return self.pipeline(tokens, postag_mys, morph_mys, lemma_ud, syntax_dep_tree_ud)
