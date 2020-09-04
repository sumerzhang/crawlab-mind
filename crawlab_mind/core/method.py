from crawlab_mind import ListSelectMethod
from crawlab_mind.entity.method import Method

LIST_SELECT_METHODS_DICT = {
    ListSelectMethod.MeanMaxTextLength: Method(ListSelectMethod.MeanMaxTextLength, 'max_text_length'),
    ListSelectMethod.MeanTextTagCount: Method(ListSelectMethod.MeanTextTagCount, 'text_tag_count'),
}
