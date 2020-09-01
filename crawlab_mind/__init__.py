from crawlab_mind.core.list_extractor import ListExtractor


def extract_lists(html_source_path) -> list:
    list_extractor = ListExtractor(html_source_path)
    return list_extractor.extract()


def extract_list(html_source_path):
    lists = extract_lists(html_source_path)
    if len(lists) > 0:
        return lists[0]
    return None


if __name__ == '__main__':
    html_lists = extract_lists('/Users/marvzhang/projects/crawlab-team/crawlab-mind/tmp/wenshu.html')
    for html_list in html_lists:
        print('====================================')
        print(html_list)
        for item in html_list.to_items():
            print(item)
