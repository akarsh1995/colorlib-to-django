from html_components.utils import tag_wrapper, block_wrapper, static_script_src_convertor, static_css_href_convertor
from .common_finder import CommonMatcher


def get_empty_block(block_name):
    return block_wrapper('', block_name)


def get_empty_header_block():
    return get_empty_block('headers')


def extra_empty_css_block():
    return get_empty_block('extra_css')


def get_empty_js_block():
    return get_empty_block('extra_js')


def get_empty_content_block():
    return get_empty_block('content')


class BaseGenerator(CommonMatcher):
    html_text: str = ''

    def __init__(self, dir_reader_obj):
        super().__init__(dir_reader_obj)
        self.prepare_base_html()

    def get_html_text(self):
        return self.html_text

    def prepare_base_html(self):
        self.add_header()
        self.add_body()
        self.wrap_in_html_tag()
        self.add_doctype_html()

    def add_doctype_html(self):
        self.html_text = '<!DOCTYPE html>' + self.html_text

    def wrap_in_html_tag(self):
        self.html_text = tag_wrapper('html', self.html_text)

    def add_header(self):
        self.html_text += self.get_header_block()

    def add_body(self):
        self.html_text += self.get_body_block()

    def get_header_block(self):
        return tag_wrapper(
            'head',
            self.get_head_content()
        )

    def get_head_content(self):
        return get_empty_header_block() + static_css_href_convertor(self.get_common_css()) + extra_empty_css_block()

    def common_css(self):
        return static_css_href_convertor(self.get_common_css())

    def get_body_block(self):
        return tag_wrapper(
            'body',
            self.get_body_content()
        )

    def get_body_content(self):
        return get_empty_content_block() + static_script_src_convertor(self.get_common_scripts()) + get_empty_js_block()

    def write_base_html(self):
        self.dir_obj.to_dir.joinpath('base.html').write_text(self.get_html_text())


class HtmlModifier(CommonMatcher):

    def __init__(self, dir_reader_obj):
        super().__init__(dir_reader_obj)

    def write_modified_content(self):
        for html in self.html_objects:
            html.write_html(self.dir_obj.to_dir)
