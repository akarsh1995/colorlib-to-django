from .tag import TagEditor
from .utils import block_wrapper, static_css_href_convertor


class Header:
    css_hrefs = []
    common_css_hrefs: list = ['']

    def __init__(self, html_text):
        self.header = html_text
        self.tag_editor = TagEditor(html_text)
        self.set_header_attribs()

    def set_header_attribs(self):
        self.set_hrefs()

    def set_hrefs(self):
        self.css_hrefs = self.tag_editor.get_css_tags()

    def set_common_css_hrefs(self, common_css_hrefs):
        assert isinstance(common_css_hrefs, list), f'common_css_hrefs argument type {type(common_css_hrefs)} ' \
                                                   f'is not list.'
        if common_css_hrefs is not None:
            self.common_css_hrefs = common_css_hrefs

    def get_header_block(self):
        # headers
        # extra css
        return self._get_header_tags_block() + self._get_unique_css_block()

    def _get_header_tags_block(self):
        self._replace_header_css()
        return block_wrapper(self._get_replaced_html(), 'meta_headers')

    def _get_unique_css_block(self):
        return block_wrapper(self._get_unique_css(), 'extra_css')

    def _get_unique_css(self):
        uncommon_css = [href for href in self.css_hrefs if href not in self.common_css_hrefs]
        return static_css_href_convertor(uncommon_css)

    def _replace_header_css(self):
        self.tag_editor.replace_css_tags()

    def _get_replaced_html(self):
        return self.tag_editor.get_text()

    def __repr__(self):
        return self.get_header_block()
