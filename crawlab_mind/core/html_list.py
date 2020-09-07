from crawlab_mind.core.html_base import HtmlBase
from crawlab_mind.core.html_list_item import HtmlListItem
from crawlab_mind.core.html_node import HtmlNode
from crawlab_mind.utils import is_invalid_tag, get_list_select_method


class HtmlList(HtmlBase):
    def __init__(self, root, els):
        self.root = root
        self.els = els
        self.items = [HtmlListItem(root, el) for el in els]
        self.all_items = self.get_all_items()

    def get_root(self):
        return self.root

    def get_items(self) -> list:
        return self.items

    def get_all_items(self) -> list:
        return [HtmlListItem(self.root, el) for el in self.root.getchildren() if not is_invalid_tag(el)]

    def get_score(self, method) -> float:
        method_obj = get_list_select_method(method)
        return self.get_mean_value(self.items, method_obj.item_attr)

    def __repr__(self):
        return f'<HtmlList: root: {HtmlNode(self.root).get_self_notation()}, items: {len(self.items)}>'
