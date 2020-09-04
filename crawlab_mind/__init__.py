from crawlab_mind.constants.list import ListSelectMethod
from crawlab_mind.core.list_extractor import ListExtractor
from crawlab_mind.core.pagination_extractor import PaginationExtractor


def extract_lists(html_source_path, **kwargs) -> list:
    extractor = ListExtractor(html_source_path, **kwargs)
    return extractor.extract()


def extract_list(html_source_path, method=ListSelectMethod.MeanMaxTextLength, multi_list=False, **kwargs):
    extractor = ListExtractor(html_source_path, **kwargs)
    if multi_list:
        return extractor.extract_items(method=method)
    else:
        return extractor.extract_best(method=method)


def extract_list_items(html_source_path, method=ListSelectMethod.MeanTextTagCount, **kwargs):
    return extract_list(html_source_path, method, multi_list=True, **kwargs)


def extract_pagination(html_source_path, **kwargs):
    extractor = PaginationExtractor(html_source_path, **kwargs)
    return extractor.extract_best()


def extract_pagination_lists(html_source_path, **kwargs):
    extractor = PaginationExtractor(html_source_path, **kwargs)
    return extractor.extract()


def test_extract_best_list(file_path):
    html_lists = extract_lists(file_path)
    print(html_lists)
    html_list = extract_list(file_path, method=ListSelectMethod.MeanMaxTextLength)
    print(html_list)
    for item in html_list.items:
        print(item)


def test_extract_best_pagination(file_path):
    html_list = extract_pagination(file_path)
    print(html_list)
    for item in html_list.all_items:
        print(item)


def test_extract_multi_list_items(file_path):
    items = extract_list_items(file_path, method=ListSelectMethod.MeanTextTagCount)
    print(len(items))
    for item in items:
        print(item)


if __name__ == '__main__':
    file_path = '/Users/marvzhang/projects/crawlab-team/crawlab-mind/tmp/baidu.html'
    test_extract_best_list(file_path)
    test_extract_best_pagination(file_path)
    # test_extract_multi_list_items(file_path)
