from lxml import etree
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA

from crawlab_mind.constants.list import ListSelectMethod
from crawlab_mind.core.html_list_collection import HtmlNodeCollection
from crawlab_mind.core.html_node import HtmlNode
from crawlab_mind.setting import MIN_CHILDREN_COUNT, PCA_N_COMPONENTS
from crawlab_mind.utils import is_invalid_tag


class ListExtractor(object):
    def __init__(self, html_source_path):
        with open(html_source_path) as f:
            raw = f.read()
        self.tree = etree.HTML(raw)
        self.docs = []
        self.nodes = []
        for el in self.tree.iter():
            # html node
            node = HtmlNode(el)

            # exclude invalid tags
            if is_invalid_tag(el):
                continue

            # exclude too-few children tags
            if node.children_count < MIN_CHILDREN_COUNT:
                continue

            # added to list
            self.docs.append(node.attributes_text)
            self.nodes.append(node)

        # vectorizer
        self.vec = TfidfVectorizer()
        self.vec.fit(self.docs)

        # data array
        self.X = self.vec.transform(self.docs)

        # clusterer
        self.cl = DBSCAN()

        # pca
        self.pca = PCA(n_components=PCA_N_COMPONENTS)

        # data array transformed by pca
        # self.X_transformed = self.pca.fit_transform(self.X.todense())

    def extract(self) -> list:
        html_lists = []
        # self.cl.fit(self.X_transformed)
        self.cl.fit(self.X)
        unique_labels = set(self.cl.labels_)
        for label in unique_labels:
            # exclude unidentified nodes
            if label == -1:
                continue

            # filter labeled nodes
            mask = self.cl.labels_ == label
            nodes = np.array(self.nodes)[mask]

            # html node collection
            node_col = HtmlNodeCollection(nodes)

            if node_col.has_lists():
                for html_list in node_col.get_lists():
                    html_lists.append(html_list)
        return html_lists

    def extract_all(self) -> list:
        return self.extract()

    def extract_best(self, method=ListSelectMethod.MeanMaxTextLength):
        html_lists = self.extract_all()
        if method == ListSelectMethod.MeanMaxTextLength:
            return self._extract_by_mean_max_text_length(html_lists)
        elif method == ListSelectMethod.MeanTextTagCount:
            return self._extract_by_mean_text_tag_count(html_lists)
        else:
            return []

    @staticmethod
    def _extract_by_attr_value(html_lists, html_list_attr, is_max=True) -> list:
        best_html_list = None
        best_value = 0
        for html_list in html_lists:
            value = getattr(html_list, html_list_attr)
            condition = value > best_value if is_max else value < best_value
            if condition:
                best_html_list = html_list
                best_value = value
        return best_html_list

    def _extract_by_mean_max_text_length(self, html_lists) -> list:
        return self._extract_by_attr_value(html_lists, 'mean_max_text_length', True)

    def _extract_by_mean_text_tag_count(self, html_lists) -> list:
        return self._extract_by_attr_value(html_lists, 'mean_text_tag_count', True)
