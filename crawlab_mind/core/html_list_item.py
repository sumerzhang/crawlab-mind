from lxml.html import Element

from crawlab_mind.core.html_node import HtmlNode


class HtmlListItem(object):
    def __init__(self, root, el):
        self.root = root
        self.el = el
        self.node = HtmlNode(el)
        self.links = self.get_links(el)
        self.images = self.get_images(el)
        self.texts = self.get_texts(el)
        self.max_text = self.get_max_text(el)
        self.max_text_length = self.get_max_text_length(el)
        self.text_tag_count = self.get_text_tag_count(el)
        self.link_count = self.get_link_count(el)

    @staticmethod
    def get_links(el: Element) -> list:
        links = []
        for a in el.iter('a'):
            if a.attrib.get('href') is None:
                continue
            if a.attrib.get('href').startswith('javascript'):
                continue
            links.append(a.attrib.get('href'))
        return list(set(links))

    @staticmethod
    def get_images(el: Element) -> list:
        images = []
        for img in el.iter('img'):
            if img.attrib.get('src') is None:
                continue
            images.append(img.attrib.get('src'))
        return list(set(images))

    @staticmethod
    def get_texts(el: Element) -> list:
        texts = []
        for text in el.itertext():
            if text.strip() == '':
                continue
            texts.append(text.strip())
        return texts

    @staticmethod
    def get_max_text(el) -> str:
        max_text = ''
        for text in el.itertext():
            if len(text.strip()) > len(max_text):
                max_text = text.strip()
        return max_text

    def get_max_text_length(self, el) -> int:
        return len(self.get_max_text(el))

    def get_text_tag_count(self, el) -> int:
        return len(self.get_texts(el))

    def get_link_count(self, el: Element) -> int:
        return len(self.get_links(el))

    def to_dict(self):
        return dict(
            texts=self.texts,
            links=self.links,
            images=self.images,
        )

    def __repr__(self):
        return f'<texts: {"; ".join(self.texts)}\nlinks: {"; ".join(self.links)}\nimages: {"; ".join(self.images)}>'
