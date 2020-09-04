from collections import defaultdict

from crawlab_mind.core.html_base import HtmlBase
from crawlab_mind.core.html_list import HtmlList
from crawlab_mind.utils import get_list_select_method


class HtmlNodeCollection(HtmlBase):
    def __init__(self, nodes, min_item_count=5, max_link_count=10):
        # parameters
        self.min_list_item_count = min_item_count
        self.max_link_count = max_link_count

        # objects
        self.nodes = nodes
        self.parent = None
        self.lists = self.get_lists()
        self.items = self.get_items()

    def get_lists(self) -> list:
        # compute parent count
        parent_dict = defaultdict(list)
        for node in self.nodes:
            parent_dict[node.el.getparent()].append(node.el)

        # get html lists
        lists = []
        for parent, items in parent_dict.items():
            if len(items) < self.min_list_item_count:
                continue
            html_list = HtmlList(parent, items)
            lists.append(html_list)
        return lists

    def has_lists(self) -> bool:
        return len(self.lists) > 0

    def get_items(self) -> list:
        items = []
        for html_list in self.lists:
            for item in html_list.items:
                items.append(item)
        return items

    def is_invalid(self) -> bool:
        mean_link_count = self.get_mean_value(self.items, 'link_count')
        return mean_link_count > self.max_link_count

    def get_score(self, method) -> float:
        method_obj = get_list_select_method(method)
        if self.is_invalid():
            return 0
        return self.get_mean_value(self.items, method_obj.item_attr)
