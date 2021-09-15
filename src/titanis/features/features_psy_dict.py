import os
import json

from .base_features_extractor import BaseFeaturesExtractor


class FeaturesPsyDict(BaseFeaturesExtractor):
    # load psydicts
    psydict_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'psydicts.json')
    with open(psydict_path) as fp:
        psydicts = json.load(fp)

    def __init__(self, psy_dict_normalization):
        super().__init__()
        self.psy_dict_normalization = psy_dict_normalization

    def __call__(self, lemma_mys, ) -> dict:
        lemma_text, sentence_count, words_count = FeaturesPsyDict.lem_info(lemma_mys)
        div = self._get_div(self.psy_dict_normalization, sentence_count, words_count)

        tgw_normalized_occur_count = self.occur_count_with_normalization(self.psydicts['tgw'], lemma_text, div)
        basic_emotions_normalized_occur_count = self.occur_count_with_normalization(
            self.psydicts['basic_emotions'], lemma_text, div)
        emowords = self.emowords(self.psydicts['emowords'], lemma_text, div)
        sentiment = self.sentiment(self.psydicts['linis-crowd'], lemma_text, div)

        return {
            **tgw_normalized_occur_count, **basic_emotions_normalized_occur_count,
            **emowords, **sentiment
        }

    @staticmethod
    def lem_info(lemma):
        words_count = 0
        lemma_text = ' '
        sentence_count = len(lemma)
        for sentence in lemma:
            for token in sentence:
                if token.isalpha():
                    words_count += 1
                    lemma_text += token+' '
        return lemma_text, sentence_count, words_count

    def occur_count_with_normalization(self, psydict, lemma_text, div):
        res = {}
        for _dict in psydict:
            res[_dict] = 0.0
            for word in psydict[_dict]:
                res[_dict] += lemma_text.count(' '+word+' ')
        self._normalize(res, div)
        return res

    def emowords(self, psydict, lemma_text, div):
        res = {}
        for _dict in psydict:
            res[_dict] = 0.0
            for word in psydict[_dict]:
                res[_dict] += lemma_text.count(' '+word+' ')

        res['ew_negative'] += res['+-']
        res['ew_negative'] += res['/-']
        res['ew_de_emotives'] += res['?/']
        res['ew_de_emotives'] += res['-/']
        res['ew_positive'] -= res.pop('+-')
        res['ew_ambivalent'] -= res.pop('?/')
        res['ew_negative'] -= res.pop('-/')
        res['ew_de_emotives'] -= res.pop('/-')

        self._normalize(res, div)

        return res

    def sentiment(self, psydict, lemma_text, div):
        res = {'sentiment_rate': 0.0}
        for word in psydict:
            res['sentiment_rate'] += psydict[word] * lemma_text.count(' '+word+' ')
        res['sentiment_rate'] = res['sentiment_rate'] / div
        return res

    def _get_div(self, psy_dict_normalization, sentence_count, words_count):
        if psy_dict_normalization == 'abs':
            div = 1
        elif psy_dict_normalization == 'sentences':
            div = sentence_count
        elif psy_dict_normalization == 'words':
            div = words_count
        else:
            raise TypeError("psy_dict_normalization arg should be 'abs', 'words' or 'sentences'")
        return div

    def _normalize(self, res, div):
        for _dict in res:
            res[_dict] /= div
