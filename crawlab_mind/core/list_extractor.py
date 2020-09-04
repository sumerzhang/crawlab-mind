from lxml import etree
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.feature_extraction.text import TfidfVectorizer

from crawlab_mind.constants.list import ListSelectMethod
from crawlab_mind.core.html_list_collection import HtmlNodeCollection
from crawlab_mind.core.html_node import HtmlNode
from crawlab_mind.entity.method import Method
from crawlab_mind.utils import is_invalid_tag, get_list_select_method


class ListExtractor(object):
    def __init__(self, html_source_path, min_children_count=3, max_sub_level=5, min_list_item_count=5, **kwargs):
        # html source path
        self.html_source_path = html_source_path

        # parameters
        self.min_children_count = min_children_count
        self.max_sub_level = max_sub_level
        self.min_list_item_count = min_list_item_count

        # construct dom tree
        with open(html_source_path) as f:
            raw = f.read()
        self.tree = etree.HTML(raw)

        self.docs = []
        self.nodes = []
        for el in self.tree.iter():
            # html node
            node = HtmlNode(el, max_sub_level=max_sub_level)

            # exclude invalid tags
            if is_invalid_tag(el):
                continue

            # exclude too-few children tags
            if node.children_count < min_children_count:
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
        # self.pca = PCA(n_components=PCA_N_COMPONENTS)

        # data array transformed by pca
        # self.X_transformed = self.pca.fit_transform(self.X.todense())

    def extract_html_node_collections(self) -> list:
        node_collections = []
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
            node_col = HtmlNodeCollection(nodes, min_list_item_count=self.min_list_item_count)

            if node_col.has_lists():
                node_collections.append(node_col)
        return node_collections

    def extract(self) -> list:
        html_lists = []
        node_collections = self.extract_html_node_collections()
        for node_col in node_collections:
            if node_col.has_lists():
                for html_list in node_col.get_lists():
                    html_lists.append(html_list)
        return html_lists

    def extract_best_node_collection(self, method=ListSelectMethod.MeanMaxTextLength):
        node_collections = self.extract_html_node_collections()
        attr = self._get_item_attr_by_method(method)
        if attr is None:
            return None
        return self._extract_by_attr_value(node_collections, attr, is_max=True)

    def extract_items(self, method=ListSelectMethod.MeanMaxTextLength) -> list:
        items = []
        node_col = self.extract_best_node_collection(method)
        for item in node_col.items:
            items.append(item)
        return items

    def extract_all(self) -> list:
        return self.extract()

    def extract_best(self, method=ListSelectMethod.MeanMaxTextLength):
        html_lists = self.extract_all()
        item_attr = self._get_item_attr_by_method(method)
        if item_attr is None:
            return None
        return self._extract_by_method(html_lists, method, is_max=True)

    def extract_custom(self, html_lists) -> list:
        # to be implemented
        raise NotImplementedError

    @staticmethod
    def _extract_by_method(o_list, method, is_max=True):
        best_o = None
        best_score = 0
        for o in o_list:
            if not hasattr(o, 'get_score'):
                continue
            score = o.get_score(method)
            condition = score > best_score if is_max else score < best_score
            if condition:
                best_o = o
                best_score = score
        return best_o

    @staticmethod
    def _get_item_attr_by_method(method) -> str:
        return get_list_select_method(method).item_attr
