from .tag import TagEditor
from .utils import block_wrapper


class Header:
    css_hrefs = []

    def __init__(self, html_text, common_css):
        self.header = html_text
        self.tag_editor = TagEditor(html_text)

    def set_header_attribs(self):
        self.set_hrefs()

    def set_hrefs(self):
        self.tag_editor.get_css_tags()

    def get_header_block_content(self):
        self.tag_editor

    def _replace_header_css(self):
        self.tag_editor.replace_css_tags()

    def _get_replaced_html(self):
        return self.tag_editor.get_text()
