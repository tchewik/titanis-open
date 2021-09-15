from isanlp import PipelineCommon
from isanlp.ru.converter_mystem_to_ud import ConverterMystemToUd
from isanlp.ru.processor_mystem import ProcessorMystem

from .base_features_extractor import BaseFeaturesExtractor


class FeaturesMystem(BaseFeaturesExtractor):
    pipeline = PipelineCommon([
        (
            ProcessorMystem(delay_init=False),
            ['tokens', 'sentences'],
            {'postag': 'postag_mys_unconverted',
             'lemma': 'lemma_mys'}),
        (
            ConverterMystemToUd(),
            ['postag_mys_unconverted'],
            {'morph': 'morph_mys',
             'postag': 'postag_mys'})
    ])

    def __call__(self, tokens, sentences) -> dict:
        return self.pipeline(tokens, sentences)
