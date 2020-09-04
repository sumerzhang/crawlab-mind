import re

from crawlab_mind import ListExtractor
from crawlab_mind.core.html_list import HtmlList
from crawlab_mind.core.html_list_item import HtmlListItem


class PaginationExtractor(ListExtractor):
    def __init__(self, html_source_path, min_children_count=1, max_sub_level=2, min_list_item_count=4, **kwargs):
        super().__init__(html_source_path, min_children_count=min_children_count, max_sub_level=max_sub_level,
                         min_list_item_count=min_list_item_count, **kwargs)
        self.regex_int = re.compile(r'^\d+$')

    def extract_custom(self, html_lists) -> list:
        best_html_list = None
        best_value = 0
        for html_list in html_lists:
            value = self.get_continuous_item_count(html_list)
            condition = value > best_value
            if condition:
                best_html_list = html_list
                best_value = value
        return best_html_list

    def extract_best(self, **kwargs):
        html_lists = self.extract()
        return self.extract_custom(html_lists)

    def get_continuous_item_count(self, html_list: HtmlList) -> int:
        count = 0
        for i in range(len(html_list.all_items)):
            if self.is_continuous(html_list, i):
                count += 1
        return count

    def is_continuous(self, html_list: HtmlList, index: int) -> bool:
        if index <= 0 or (len(html_list.all_items) - 1) <= index:
            return False

        item = html_list.all_items[index]
        prev_item = html_list.all_items[index - 1]
        next_item = html_list.all_items[index + 1]

        # if none of the items is integer, return false
        if not self.is_int_item(item) or not self.is_int_item(prev_item) or not self.is_int_item(next_item):
            return False

        # if 2 times item numeric value equal the sum of previous item and next item numeric values, return true,
        # and vice versa
        return self.get_item_int(item) * 2 == (self.get_item_int(prev_item) + self.get_item_int(next_item))

    def is_int_item(self, item: HtmlListItem) -> bool:
        item_text = ''.join(item.texts)
        return self.regex_int.match(item_text) is not None

    @staticmethod
    def get_item_int(item: HtmlListItem) -> int:
        item_text = ''.join(item.texts)
        return int(item_text)
