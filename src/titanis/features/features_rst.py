from isanlp import PipelineCommon
from isanlp.pipeline_conditional import PipelineConditional
from isanlp.processor_remote import ProcessorRemote

from .base_docker_extractor import BaseDockerExtractor


class FeaturesRST(BaseDockerExtractor):
    PORT = 3136

    def __init__(self, host, discourse_long_text_only=False):
        super().__init__(host=host)
        strange_dict = {0: DummyProcessor(output={'rst': []})}

        if discourse_long_text_only:
            strange_dict[1] = DummyProcessor(output={'rst': []})

        self.pipeline = PipelineCommon([(
            PipelineConditional(
                (lambda text, tokens, sentences, postag, morph, lemma, syntax: len(sentences)),
                strange_dict,
                default_ppl=ProcessorRemote(host=host, port=self.PORT, pipeline_name='default')
            ),
            ['text', 'tokens', 'sentences', 'postag_mys', 'morph_mys', 'lemma_ud', 'syntax_dep_tree_ud'],
            {'rst': 'rst'}
        )])

    def __call__(self, text, tokens, sentences, postag_mys, morph_mys, lemma_ud, syntax_dep_tree_ud):
        return self.pipeline(text, tokens, sentences, postag_mys, morph_mys, lemma_ud, syntax_dep_tree_ud)


class DummyProcessor:
    def __init__(self, output):
        self.output = output

    def __call__(self, *args, **kwargs):
        return self.output
