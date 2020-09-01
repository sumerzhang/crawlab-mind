from xml.etree.ElementTree import Element

EXCLUDE_TAGS = [
    'html',
    'head',
    'meta',
    'link',
    'style',
    'script',
    'noscript',
]


def is_invalid_tag(el: Element) -> bool:
    # excluded tag
    if el.tag in EXCLUDE_TAGS:
        return True

    # comment tag
    if is_comment_tag(el):
        return True

    return False


def is_comment_tag(el: Element) -> bool:
    return type(el.tag) != str
