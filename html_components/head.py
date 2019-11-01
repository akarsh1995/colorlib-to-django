from .tag import TagEditor
from .utils import block_wrapper


class Header:
    css_hrefs = []

    def __init__(self, html_text, common_css_hrefs=None):
        if common_css_hrefs is None:
            self.common_css_hrefs = ['']
        else:
            assert isinstance(common_css_hrefs, list), f'common_css_hrefs argument type {type(common_css_hrefs)} ' \
                                                       f'is not list.'
        self.header = html_text
        self.tag_editor = TagEditor(html_text)
        self.set_header_attribs()

    def set_header_attribs(self):
        self.set_hrefs()

    def set_hrefs(self):
        self.css_hrefs = self.tag_editor.get_css_tags()

    def get_header_block(self):
        # headers
        # extra css
        return self._get_header_tags_block() + self._get_unique_css_block()

    def _get_header_tags_block(self):
        self._replace_header_css()
        return block_wrapper(self._get_replaced_html(), 'meta_headers')

    def _get_unique_css_block(self):
        return block_wrapper('\n'.join(self._get_unique_css()), 'extra_css')

    def _get_unique_css(self):
        return ["""<link rel="stylesheet" href="{{% static '{0}' %}}">""".format(css)
                for css in self.css_hrefs if css not in self.common_css_hrefs]

    def _replace_header_css(self):
        self.tag_editor.replace_css_tags()

    def _get_replaced_html(self):
        return self.tag_editor.get_text()

    def __repr__(self):
        return self.get_header_block()
