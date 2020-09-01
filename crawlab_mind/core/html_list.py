class HtmlList(object):
    def __init__(self, root, items):
        self.root = root
        self.items = items

    def get_root(self):
        return self.root

    def get_items(self) -> list:
        return self.items
