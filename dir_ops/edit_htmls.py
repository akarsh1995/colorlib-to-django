from .common_finder import CommonMatcher


class BaseGenerator(CommonMatcher):
    def __init__(self, dir_reader_obj):
        super().__init__(dir_reader_obj)
        pass


class HtmlModifier(CommonMatcher):

    def __init__(self, dir_reader_obj):
        super().__init__(dir_reader_obj)
