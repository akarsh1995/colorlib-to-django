from .tag import TagEditor
from .utils import block_wrapper, static_script_src_convertor


class Body:
    scripts: list = []
    footer: str = ''
    nav: str = ''
    common_scripts: list = []

    def __init__(self, html_text):
        self.body = html_text
        self.tag_editor = TagEditor(html_text)
        self.set_body_attribs()

    def set_common_scripts(self, common_scripts):
        assert isinstance(common_scripts, list), f'common_css_hrefs argument type {type(common_scripts)} ' \
                                                 f'is not list.'
        if common_scripts is not None:
            self.common_scripts = common_scripts

    def set_body_attribs(self):
        self.set_nav()
        self.set_footer()
        self.set_scripts()

    def set_nav(self):
        self.nav = self.tag_editor.get_main_tag_content('nav', include_tags=True)

    def set_footer(self):
        self.footer = self.tag_editor.get_main_tag_content('footer', include_tags=True)

    def set_scripts(self):
        self.scripts = self.tag_editor.get_script_tags()

    def get_block_content(self):
        self._replace_navbar()
        self._replace_footer()
        self._replace_scripts()
        return (block_wrapper(self._get_replaced_html(), 'content')
                + self._get_unique_scripts_block())

    def _replace_scripts(self):
        self.tag_editor.replace_script_tags()

    def _replace_navbar(self):
        self.tag_editor.replace_main_tag('nav', "{% include 'navbar.html' %}")

    def _replace_footer(self):
        self.tag_editor.replace_main_tag('footer', "{% include 'footer.html' %}")

    def _get_unique_scripts_block(self):
        return block_wrapper(self._get_unique_scripts(), 'extra_js')

    def _get_unique_scripts(self):
        uncommon_scripts = [src for src in self.scripts if src not in self.common_scripts]
        return static_script_src_convertor(uncommon_scripts)

    def _get_replaced_html(self):
        return self.tag_editor.get_text()

    def __repr__(self):
        return self.get_block_content()
