from collections import defaultdict

from crawlab_mind.core.html_list import HtmlList
from crawlab_mind.utils import is_invalid_tag

MAX_SUB_LEVEL = 5
MIN_LIST_ITEM_COUNT = 8


class HtmlNode(object):
    def __init__(self, el, root=None):
        self.el = el
        self.root = root
        if root is None:
            self.root = el

    def get_path(self):
        paths = []
        el = self.el
        paths.append(self.get_self_path(el))
        while self.root != el:
            el = el.getparent()
            paths.insert(0, self.get_self_path(el))
        return '>'.join(paths)

    def get_self_path(self, el=None) -> str:
        if el is None:
            el = self.el
        if el.attrib.get('class') is None:
            return el.tag
        return f'{el.tag}.{el.attrib.get("class").strip().replace(" ", "_")}'

    def get_children(self, el=None):
        if el is None:
            el = self.el
        for sub_el in el.getchildren():
            if is_invalid_tag(sub_el):
                continue
            yield sub_el

    def get_attributes(self, el=None, root=None, level=0):
        if el is None:
            el = self.el
        if root is None:
            root = self.el
        if level >= MAX_SUB_LEVEL:
            return []
        node = HtmlNode(el, root)
        yield node.get_path()
        for sub_el in self.get_children(el):
            for attr in self.get_attributes(sub_el, root, level + 1):
                yield attr

    def get_children_count(self):
        return len([_ for _ in self.get_attributes()])

    def get_inner_text(self):
        return ''.join(self.el.itertext())

    @property
    def attributes(self) -> list:
        return [attr for attr in self.get_attributes()]

    @property
    def attributes_text(self) -> str:
        return ' '.join(self.attributes)

    @property
    def self_path(self) -> str:
        return self.get_self_path()

    @property
    def children_count(self) -> int:
        return self.get_children_count()

    @property
    def text(self) -> str:
        return self.get_inner_text()

    @property
    def inner_text(self) -> str:
        return self.get_inner_text()


class HtmlNodeCollection(object):
    def __init__(self, nodes):
        self.nodes = nodes
        self.parent = None
        self.lists = self.get_lists()

    def get_lists(self) -> list:
        # compute parent count
        parent_dict = defaultdict(list)
        for node in self.nodes:
            parent_dict[node.el.getparent()].append(node.el)

        # get html lists
        lists = []
        for parent, items in parent_dict.items():
            if len(items) < MIN_LIST_ITEM_COUNT:
                continue
            html_list = HtmlList(parent, items)
            lists.append(html_list)
        return lists

    def has_lists(self) -> bool:
        return len(self.lists) > 0