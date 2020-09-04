from crawlab_mind.core.html_list_item import HtmlListItem
from crawlab_mind.core.html_node import HtmlNode
from crawlab_mind.utils import is_invalid_tag


class HtmlList(object):
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

    def _get_mean_value(self, item_attr) -> float:
        values = []
        for item in self.items:
            values.append(getattr(item, item_attr))
        return sum(values) / len(values)

    def get_mean_max_text_length(self) -> float:
        return self._get_mean_value('max_text')

    def get_mean_text_tag_count(self) -> float:
        return self._get_mean_value('text_tag_count')

    @property
    def mean_max_text_length(self) -> float:
        return self.get_mean_max_text_length()

    @property
    def mean_text_tag_count(self) -> float:
        return self.get_mean_text_tag_count()

    def __repr__(self):
        return f'<HtmlList: root: {HtmlNode(self.root).get_self_path()}, items: {len(self.items)}>'
