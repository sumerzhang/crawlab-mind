from lxml.html import Element

from crawlab_mind.utils import is_invalid_tag


class HtmlNode(object):
    def __init__(self, el, root=None, max_sub_level=5):
        # current lxml element
        self.el = el

        # root lxml element of current element
        self.root = root

        # set root element to self if no root element is passed
        if root is None:
            self.root = el

        # parameters
        self.max_sub_level = max_sub_level

    def get_path(self) -> str:
        """
        Get the relative path representation of current element from root element.
        It is similar to css selector.
        For example, ul.list>li.item>a.title
        """
        paths = []
        el = self.el
        paths.append(self.get_self_notation(el))
        while self.root != el:
            el = el.getparent()
            paths.insert(0, self.get_self_notation(el))
        return '>'.join(paths)

    def get_self_notation(self, el: Element = None) -> str:
        """
        Get self notation (representation), which constitute the path of the element.
        """
        if el is None:
            el = self.el
        if el.attrib.get('class') is None:
            return el.tag
        return f'{el.tag}.{el.attrib.get("class").strip().replace(" ", "_")}'

    def get_children(self, el=None):
        """
        Get child elements (non-recursive)
        """
        if el is None:
            el = self.el
        for sub_el in el.getchildren():
            if is_invalid_tag(sub_el):
                continue
            yield sub_el

    def get_notations(self, el=None, root=None, level=0):
        """
        Get all notations of the given lxml element and root element.
        :param el: current lxml element
        :param root: root lxml element
        :param level: current level of current lxml element
        """
        if el is None:
            el = self.el
        if root is None:
            root = self.el
        if level >= self.max_sub_level:
            return []
        node = HtmlNode(el, root)
        yield node.get_path()
        for sub_el in self.get_children(el):
            for attr in self.get_notations(sub_el, root, level + 1):
                yield attr

    def get_all_children_count(self) -> int:
        """
        Get all children count (recursive).
        """
        return len([_ for _ in self.get_notations()])

    def get_inner_text(self) -> str:
        """
        Get inner text of current element.
        """
        return ''.join(self.el.itertext())

    @property
    def notations(self) -> list:
        """
        Get a list of notations of all (sub-)elements of current element.
        """
        return [attr for attr in self.get_notations()]

    @property
    def notations_text(self) -> str:
        """
        Get the text concatenated from notations of current element.
        """
        return ' '.join(self.notations)

    @property
    def self_notation(self) -> str:
        """
        Self notation
        """
        return self.get_self_notation()

    @property
    def children_count(self) -> int:
        """
        Children count
        """
        return self.get_all_children_count()

    @property
    def text(self) -> str:
        """
        Inner text
        """
        return self.get_inner_text()

    @property
    def inner_text(self) -> str:
        """
        Inner text
        """
        return self.get_inner_text()
