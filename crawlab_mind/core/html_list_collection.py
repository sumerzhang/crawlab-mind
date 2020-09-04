from collections import defaultdict

from crawlab_mind.core.html_list import HtmlList


class HtmlNodeCollection(object):
    def __init__(self, nodes, min_list_item_count=5):
        # parameters
        self.min_list_item_count = min_list_item_count

        # objects
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
            if len(items) < self.min_list_item_count:
                continue
            html_list = HtmlList(parent, items)
            lists.append(html_list)
        return lists

    def has_lists(self) -> bool:
        return len(self.lists) > 0
