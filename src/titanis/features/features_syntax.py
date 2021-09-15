from .base_features_extractor import BaseFeaturesExtractor


class FeaturesSyntax(BaseFeaturesExtractor):
    def __call__(self, syntax_dep_tree_ud, syntax_normalization='words') -> dict:
        features = dict()
        max_tree, min_tree, trees_len = FeaturesSyntax.stat_from_synt_dep_tree(syntax_dep_tree_ud)

        synt_rels = {
            'flat:foreign:': 0.0,
            'csubj': 0.0,
            'acl': 0.0,
            'acl:relcl': 0.0,
            'advcl': 0.0,
            'advmod': 0.0,
            'amod': 0.0,
            'appos': 0.0,
            'aux': 0.0,
            'aux:pass': 0.0,
            'case': 0.0,
            'cc': 0.0,
            'cc:preconj': 0.0,
            'ccomp': 0.0,
            'conj': 0.0,
            'cop': 0.0,
            'det': 0.0,
            'discourse': 0.0,
            'fixed': 0.0,
            'flat': 0.0,
            'goeswith': 0.0,
            'iobj': 0.0,
            'list': 0.0,
            'mark': 0.0,
            'nmod': 0.0,
            'nsubj': 0.0,
            'nsubj:pass': 0.0,
            'nummod': 0.0,
            'nummod:gov': 0.0,
            'obj': 0.0,
            'obl': 0.0,
            'orphan': 0.0,
            'parataxis': 0.0,
            'punct': 0.0,
            'root': 0.0,
            'xcomp': 0.0,
            'compound': 0.0,
            'flat:foreign': 0.0
        }

        sentence_count = len(syntax_dep_tree_ud)
        word_count = 0
        for sentence in syntax_dep_tree_ud:
            word_count += len(sentence)
            for word in sentence:
                if word.link_name in synt_rels:
                    synt_rels[word.link_name] += 1
        word_count -= synt_rels['punct']

        if syntax_normalization == 'abs':
            self.div = 1
        elif syntax_normalization == 'sentences':
            self.div = sentence_count if sentence_count else 1
        else:
            self.div = word_count if word_count else 1

        for s_rel in synt_rels:
            synt_rels[s_rel] = synt_rels[s_rel] / self.div

        features['max_synt_tree'] = max_tree
        features['min_synt_tree'] = min_tree
        features['mean_synt_tree'] = sum(trees_len) / len(trees_len)
        features.update(synt_rels)

        return features

    @staticmethod
    def stat_from_synt_dep_tree(tree):
        all_paths = []
        for sen_id, sentence in enumerate(tree):
            tree_paths = []
            for w_id in range(len(sentence)):
                is_root = False
                cur_id = w_id
                path = []
                while not is_root:
                    path.append(cur_id)
                    if sentence[cur_id].link_name != 'root':
                        cur_id = sentence[cur_id].parent
                    else:
                        is_root = True
                tree_paths.append(path)
            all_paths.append(max([len(x) for x in tree_paths]))

        if all_paths:
            return max(all_paths), min(all_paths), all_paths
        else:
            return 0, 0, [0]
