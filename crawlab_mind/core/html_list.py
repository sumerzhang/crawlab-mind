from crawlab_mind.core.html_list_item import HtmlListItem
from crawlab_mind.core.html_node import HtmlNode


class HtmlList(object):
    def __init__(self, root, items):
        self.root = root
        self.items = items

    def get_root(self):
        return self.root

    def get_items(self) -> list:
        return self.items

    def to_items(self) -> list:
        html_list_items = []
        for item in self.items:
            html_list_items.append(HtmlListItem(self.root, item))
        return html_list_items

    def __repr__(self):
        return f'<HtmlList: root: {HtmlNode(self.root).get_self_path()}, items: {len(self.items)}>'
