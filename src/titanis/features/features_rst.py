from isanlp import PipelineCommon
from isanlp.pipeline_conditional import PipelineConditional
from isanlp.processor_remote import ProcessorRemote

from .base_docker_extractor import BaseDockerExtractor


class FeaturesRST(BaseDockerExtractor):
    PORT = 3136

    def __init__(self, host, discourse_long_text_only=False):
        super().__init__(host=host)

        pipeline_variants = {0: DummyProcessor(output={'rst': []}),
                             1: ProcessorRemote(host=host, port=self.PORT, pipeline_name='default')}
        condition = lambda _te, _to, sentences, _po, _mo, _le, _sy: not discourse_long_text_only or (
            discourse_long_text_only and len(sentences) > 1)

        self.pipeline = PipelineCommon([(
            PipelineConditional(
                condition,
                pipeline_variants,
                default_ppl=pipeline_variants[1]
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
