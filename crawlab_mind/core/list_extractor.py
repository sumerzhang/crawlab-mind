from lxml import etree
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA

from crawlab_mind.core.html_node import HtmlNode, HtmlNodeCollection
from crawlab_mind.utils import is_invalid_tag

MIN_CHILDREN_COUNT = 5
PCA_N_COMPONENTS = 10


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

    def extract(self):
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
                    for item in html_list.items:
                        # print(f'{HtmlNode(html_list.root).get_self_path()}\t{HtmlNode(item).get_self_path()}')
                        print(f'{HtmlNode(html_list.root).get_self_path()}\t{HtmlNode(item).get_self_path()}')

            # for node in nodes:
            #     print(f'{str(label)}\t{node.self_path}\t{node.attributes}\t{node.children_count}')


if __name__ == '__main__':
    # identifier = ListExtractor('/Users/marvzhang/projects/crawlab-team/crawlab-mind/tmp/v2ex.html')
    # identifier = ListExtractor('/Users/marvzhang/projects/crawlab-team/crawlab-mind/tmp/baidu.html')
    # identifier = ListExtractor('/Users/marvzhang/projects/crawlab-team/crawlab-mind/tmp/juejin.html')
    # identifier = ListExtractor('/Users/marvzhang/projects/crawlab-team/crawlab-mind/tmp/bing.html')
    # identifier = ListExtractor('/Users/marvzhang/projects/crawlab-team/crawlab-mind/tmp/jd.html')
    # identifier = ListExtractor('/Users/marvzhang/projects/crawlab-team/crawlab-mind/tmp/taobao.html')
    # identifier = ListExtractor('/Users/marvzhang/projects/crawlab-team/crawlab-mind/tmp/zhihu.html')
    # identifier = ListExtractor('/Users/marvzhang/projects/crawlab-team/crawlab-mind/tmp/douban_movie.html')
    # identifier = ListExtractor('/Users/marvzhang/projects/crawlab-team/crawlab-mind/tmp/dianping.html')
    # identifier = ListExtractor('/Users/marvzhang/projects/crawlab-team/crawlab-mind/tmp/163.html')
    identifier = ListExtractor('/Users/marvzhang/projects/crawlab-team/crawlab-mind/tmp/music.163.html')
    identifier.extract()
