from crawlab_mind.constants.list import ListSelectMethod
from crawlab_mind.core.list_extractor import ListExtractor


def extract_lists(html_source_path) -> list:
    list_extractor = ListExtractor(html_source_path)
    return list_extractor.extract()


def extract_list(html_source_path, method=ListSelectMethod.MeanMaxTextLength):
    list_extractor = ListExtractor(html_source_path)
    return list_extractor.extract_best(method=method)


if __name__ == '__main__':
    file_path = '/Users/marvzhang/projects/crawlab-team/crawlab-mind/tmp/1688.html'
    html_lists = extract_lists(file_path)
    print(html_lists)
    html_list = extract_list(file_path, method=ListSelectMethod.MeanTextTagCount)
    print(html_list)
    for item in html_list.items:
        print(item)

