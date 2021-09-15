import re

from .base_features_extractor import BaseFeaturesExtractor


class FeaturesPsyCues(BaseFeaturesExtractor):
    def __init__(self, psy_cues_normalization):
        super().__init__()
        self.psy_cues_normalization = psy_cues_normalization

    def __call__(self, text, lemma_mys, postag_mys_unconverted) -> dict:
        features = {}
        postags_count = {
            'postag_A': 0.0,
            'postag_ADV': 0.0,
            'postag_ADVPRO': 0.0,
            'postag_ANUM': 0.0,
            'postag_APRO': 0.0,
            'postag_COM': 0.0,
            'postag_CONJ': 0.0,
            'postag_INTJ': 0.0,
            'postag_NUM': 0.0,
            'postag_PART': 0.0,
            'postag_PR': 0.0,
            'postag_S': 0.0,
            'postag_SPRO': 0.0,
            'postag_V': 0.0
        }

        w_count = 0
        neg_forms_count = 0
        inf_count = 0
        past_verbs = 0
        gerunds = 0
        participles = 0
        verbs_1p = 0
        verbs_2p = 0
        verbs_3p = 0
        pro_1p = 0
        pro_1p_single = 0
        pro_1p_plural = 0
        pro_2p = 0
        pro_3p = 0
        neg_forms = ('не', 'бес', 'без', 'ни')
        unique_words = []

        for sentence_id in range(len(postag_mys_unconverted)):
            for token_id in range(len(postag_mys_unconverted[sentence_id])):
                g_info = FeaturesPsyCues.grammeme_info(postag_mys_unconverted[sentence_id][token_id])
                if g_info:
                    word = lemma_mys[sentence_id][token_id]
                    postags_count['postag_' + g_info['postag']] += 1
                    w_count += 1
                    if word.startswith(neg_forms):
                        neg_forms_count += 1
                    if word not in unique_words:
                        unique_words.append(word)

                    if 'инф' in g_info['all']:
                        inf_count += 1
                    if g_info['postag'] == 'V' and 'прош' in g_info['all'] and 'деепр' not in g_info['all']:
                        past_verbs += 1
                    if 'деепр' in g_info['all']:
                        gerunds += 1
                    if 'прич' in g_info['all']:
                        participles += 1

                    if not g_info['multiple'] and g_info['postag'] == 'V':
                        if '1-л' in g_info['all']:
                            verbs_1p += 1
                        if '2-л' in g_info['all']:
                            verbs_2p += 1
                        if '3-л' in g_info['all']:
                            verbs_3p += 1

                    if g_info['postag'] == 'SPRO':
                        if '1-л' in g_info['all']:
                            pro_1p += 1
                            if 'ед' in g_info['all']:
                                pro_1p_single += 1
                            if 'мн' in g_info['all']:
                                pro_1p_plural += 1
                        if '2-л' in g_info['all']:
                            pro_2p += 1
                        if '3-л' in g_info['all']:
                            pro_3p += 1

        r = re.findall(r'[а-яА-Я]', text)
        features['char_count'] = len(r) if len(r) else 1
        features['word_count'] = w_count if w_count else 1
        features['sentence_count'] = len(postag_mys_unconverted) if len(postag_mys_unconverted) else 1
        features['unique_words_count'] = len(unique_words)
        features['punctuation_count'] = len(re.findall(r'[.,!?;-]', text))
        features['punctuation_per_word'] = features['punctuation_count'] / features['word_count']
        features['uppercase_rate'] = len(re.findall(r'[А-Я]', text)) / features['char_count']
        features['mean_word_len'] = features['char_count'] / features['word_count']
        features['mean_sentence_len'] = features['word_count'] / features['sentence_count']
        features['unique_words_rate'] = len(unique_words) / features['word_count']
        features['verbs_1p_rate'] = verbs_1p / postags_count['postag_V'] if postags_count['postag_V'] else 0
        features['verbs_2p_rate'] = verbs_2p / postags_count['postag_V'] if postags_count['postag_V'] else 0
        features['verbs_3p_rate'] = verbs_3p / postags_count['postag_V'] if postags_count['postag_V'] else 0
        features['verbs_past_tense_rate'] = past_verbs / postags_count['postag_V'] if postags_count['postag_V'] else 0
        features['infinitives_rate'] = inf_count / postags_count['postag_V'] if postags_count['postag_V'] else 0
        features['pro_1p_rate'] = pro_1p / postags_count['postag_SPRO'] if postags_count['postag_SPRO'] else 0
        features['pro_1p_sing_rate'] = pro_1p_single / postags_count['postag_SPRO'] if postags_count['postag_SPRO'] else 0
        features['pro_1p_plural_rate'] = pro_1p_plural / postags_count['postag_SPRO'] if postags_count['postag_SPRO'] else 0
        features['pro_2p_rate'] = pro_2p / postags_count['postag_SPRO'] if postags_count['postag_SPRO'] else 0
        features['pro_3p_rate'] = pro_3p / postags_count['postag_SPRO'] if postags_count['postag_SPRO'] else 0
        trager_adjectives = postags_count['postag_A'] + postags_count['postag_APRO'] + postags_count['postag_ANUM']
        trager_verbs = postags_count['postag_V'] - gerunds - participles
        features['trager_coef'] = trager_verbs / trager_adjectives if trager_adjectives else trager_verbs
        features['logical_coh_coef'] = (postags_count['postag_CONJ'] + postags_count['postag_PR']) / (
                features['sentence_count'] * 3)
        features['verbs_per_nouns_coef'] = postags_count['postag_V'] / postags_count['postag_S'] if postags_count['postag_S'] else 0
        features['participles_gerunds_coef'] = (participles + gerunds) / features['sentence_count']
        features['negation_rate'] = neg_forms_count / features['word_count']

        if self.psy_cues_normalization == 'abs':
            div = 1
        elif self.psy_cues_normalization == 'sentences':
            div = features['sentence_count']
        elif self.psy_cues_normalization == 'words':
            div = features['word_count']
        else:
            raise TypeError("psy_cues_normalization arg should be 'abs', 'sentences' or 'words'")

        for postag_mys_unconverted in postags_count:
            postags_count[postag_mys_unconverted] = postags_count[postag_mys_unconverted] / div

        features.update(postags_count)

        return features

    @staticmethod
    def grammeme_info(mystem_grammeme_str):
        res = {}
        if mystem_grammeme_str:
            res['static'] = mystem_grammeme_str.split('=')[0].split(',')
            res['postag'] = res['static'][0]
            res['multiple'] = False
            res['all'] = [] + res['static']
            mutable_str = mystem_grammeme_str.split('=')[1]
            if '|' not in mutable_str:
                res['mutable'] = mutable_str.split(',')
                res['all'] += res['mutable']
            else:
                res['multiple'] = True
                res['mutable'] = [i.split(',') for i in mutable_str[1:-1].split('|')]
                for i in res['mutable']:
                    for g in i:
                        if g not in res['all']:
                            res['all'].append(g)
        return res
