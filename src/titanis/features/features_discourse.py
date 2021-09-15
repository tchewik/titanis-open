from collections import Counter
from string import punctuation

from nltk.tokenize import TweetTokenizer

from .base_features_extractor import BaseFeaturesExtractor


class FeaturesDiscourse(BaseFeaturesExtractor):
    def __init__(self):
        super(FeaturesDiscourse, self).__init__()
        self.tokenizer = TweetTokenizer()
        self.features_list = (
            self.number_of_units,
            self.number_of_trees,
            self.first_tree_edus_number,
            self.last_tree_edus_number,
            self.suspended_edus_number,
            self.average_du_length,
            self.average_edu_length,
            self.average_tree_depth,
            self.symmetric_relations,
            self.first_word_uniqueness,
            self.du_len_imbalance,
            self.simple_sentence_ratio,
            self.rst_relations_string
        )

    def __call__(self, rst) -> dict:
        result = dict()

        for feature in self.features_list:
            result[feature.__name__] = feature(rst)

        if result.get('rst_relations_string'):
            relations = result.get('rst_relations_string').split()
            result.update(Counter(relations))
            del result['rst_relations_string']

        return result

    def get_rst_relation(self, tree):
        rr = []
        if tree.left:
            rr.append(tree.relation + '_' + tree.nuclearity)
            rr += self.get_rst_relation(tree.left)
            rr += self.get_rst_relation(tree.right)
        return rr

    def rst_relations_string(self, trees: list):
        """ Returns relations from discourse tree """
        result = []
        for tree in trees:
            result += self.get_rst_relation(tree)

        return ' '.join(result)

    def count_units(self, tree):
        n = 0
        if tree.left:
            n += 1
            n += self.count_units(tree.left)
            n += self.count_units(tree.right)
        else:
            n += 1
        return n

    def number_of_units(self, trees):
        """ Returns number of units including EDUs """
        result = 0
        for tree in trees:
            result += self.count_units(tree)
        return result

    @staticmethod
    def number_of_trees(trees):
        return len(trees)

    def dummy_tokenize(self, text):
        res = [token for token in self.tokenizer.tokenize(text.lower()) if token not in punctuation]
        if not res:
            return text.split(' ')
        return res

    def extract_dus_length(self, tree):
        tt = [len(self.dummy_tokenize(tree.text))]
        if tree.left:
            tt += self.extract_dus_length(tree.left)
            tt += self.extract_dus_length(tree.right)
        return tt

    def extract_edus_length(self, tree):
        if not tree.left:
            tt = [len(self.dummy_tokenize(tree.text))]
        else:
            tt = []
            tt += self.extract_edus_length(tree.left)
            tt += self.extract_edus_length(tree.right)
        return tt

    def average_du_length(self, trees):
        result = []
        for tree in trees:
            result += self.extract_dus_length(tree)
        return sum(result) / len(result)

    def average_edu_length(self, trees):
        result = []
        for tree in trees:
            result += self.extract_edus_length(tree)
        return sum(result) / len(result)

    def count_tree_depth(self, tree):
        left_depth = self.count_tree_depth(tree.left) if tree.left else 0
        right_depth = self.count_tree_depth(tree.right) if tree.right else 0
        return max(left_depth, right_depth) + 1

    def average_tree_depth(self, trees):
        """ Returns average DU depth """
        depths = []
        for tree in trees:
            depths.append(self.count_tree_depth(tree))
        return sum(depths) / len(depths)

    def first_tree_edus_number(self, trees):
        return len(self.extract_edus_length(trees[0]))

    def last_tree_edus_number(self, trees):
        return len(self.extract_edus_length(trees[-1]))

    @staticmethod
    def suspended_edus_number(trees):
        """ Returns number of EDUs not involved in trees """
        return sum([tree.relation == 'elementary' for tree in trees])

    def get_nuclearities(self, tree):
        nc = []
        if tree.left:
            nc = [tree.nuclearity]
            nc += self.get_nuclearities(tree.left)
            nc += self.get_nuclearities(tree.right)
        return nc

    @staticmethod
    def d_len(x):
        return len(x) if len(x) else 1e-5

    def symmetric_relations(self, trees):
        """ Returns monononuclear relations ratio """
        result = []
        for tree in trees:
            result += self.get_nuclearities(tree)
        return sum([nc == 'NN' for nc in result]) / FeaturesDiscourse.d_len(result)

    def get_first_words(self, tree):
        if tree.relation == 'elementary':
            tt = [self.dummy_tokenize(tree.text)[0]]
        else:
            tt = []
            tt += self.get_first_words(tree.left)
            tt += self.get_first_words(tree.right)
        return tt

    def first_word_uniqueness(self, trees):
        """ Returns unique EDU starts ratio """
        fw = []
        for tree in trees:
            fw += self.get_first_words(tree)

        return len(set(fw)) / len(fw)

    def right_left_ratio(self, tree):
        rt = []
        if tree.left:
            rt.append(len(self.dummy_tokenize(tree.right.text)) / len(self.dummy_tokenize(tree.left.text)))
            rt += self.right_left_ratio(tree.left)
            rt += self.right_left_ratio(tree.right)
        return rt

    def du_len_imbalance(self, trees):
        """ Returns average [right DU length] / [left DU length] ratio """
        result = []
        for tree in trees:
            result += self.right_left_ratio(tree)

        return sum(result) / FeaturesDiscourse.d_len(result)

    def extract_simple_edus(self, tree):
        if not tree.left:
            tt = [tree.text[0].isupper() and tree.text[-1] in ".?!"]
        else:
            tt = []
            tt += self.extract_simple_edus(tree.left)
            tt += self.extract_simple_edus(tree.right)
        return tt

    def simple_sentence_ratio(self, trees):
        result = []

        for tree in trees:
            result += self.extract_simple_edus(tree)

        return sum(result) / len(result)
