from crawlab_mind.constants.list import ListSelectMethod
from crawlab_mind.core.list_extractor import ListExtractor
from crawlab_mind.core.pagination_extractor import PaginationExtractor


def extract_lists(html_source_path, **kwargs) -> list:
    extractor = ListExtractor(html_source_path, **kwargs)
    return extractor.extract()


def extract_list(html_source_path, method=ListSelectMethod.MeanMaxTextLength, **kwargs):
    extractor = ListExtractor(html_source_path, **kwargs)
    return extractor.extract_best(method=method)


def extract_pagination(html_source_path, **kwargs):
    extractor = PaginationExtractor(html_source_path, **kwargs)
    return extractor.extract_best()


def extract_pagination_lists(html_source_path, **kwargs):
    extractor = PaginationExtractor(html_source_path, **kwargs)
    return extractor.extract()


if __name__ == '__main__':
    file_path = '/Users/marvzhang/projects/crawlab-team/crawlab-mind/tmp/autohome.html'
    # html_lists = extract_lists(file_path)
    # print(html_lists)
    # html_list = extract_list(file_path, method=ListSelectMethod.MeanTextTagCount)
    # print(html_list)
    # for item in html_list.items:
    #     print(item)
    html_lists = extract_pagination_lists(file_path)
    print(html_lists)
    # for html_list in html_lists:
    #     print(html_list)
    #     for item in html_list.items:
    #         print(item)
    html_list = extract_pagination(file_path)
    print(html_list)
    for item in html_list.all_items:
        print(item)
