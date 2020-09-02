from crawlab_mind.core.html_list_item import HtmlListItem
from crawlab_mind.core.html_node import HtmlNode


class HtmlList(object):
    def __init__(self, root, els):
        self.root = root
        self.els = els
        self.items = [HtmlListItem(root, el) for el in els]

    def get_root(self):
        return self.root

    def get_items(self) -> list:
        return self.items

    def get_mean_max_text_length(self) -> float:
        lengths = []
        for item in self.items:
            lengths.append(len(item.max_text))
        return sum(lengths) / len(lengths)

    def get_mean_text_tag_count(self) -> float:
        counts = []
        for item in self.items:
            counts.append(item.text_tag_count)
        return sum(counts) / len(counts)

    def __repr__(self):
        return f'<HtmlList: root: {HtmlNode(self.root).get_self_path()}, items: {len(self.items)}>'
