from .tag import TagEditor
from .utils import block_wrapper


class Body:
    scripts: list = []
    footer: str = ''
    nav: str = ''

    def __init__(self, html_text, common_scripts):
        self.common_scripts = common_scripts
        self.body = html_text
        self.tag_editor = TagEditor(html_text)
        self.set_body_attribs()

    def set_body_attribs(self):
        self.set_nav()
        self.set_footer()
        self.set_scripts()

    def set_nav(self):
        self.nav = self.tag_editor.get_main_tag_content('nav')

    def set_footer(self):
        self.footer = self.tag_editor.get_main_tag_content('footer')

    def set_scripts(self):
        self.scripts = self.tag_editor.get_script_tags()

    def get_block_content(self):
        self._replace_navbar()
        self._replace_footer()
        self._replace_scripts()
        return (block_wrapper(self._get_replaced_html(), 'content')
                + block_wrapper(self._get_unique_scripts_block(), 'extra_js'))

    def _replace_scripts(self):
        self.tag_editor.replace_script_tags()

    def _replace_navbar(self):
        self.tag_editor.replace_main_tag('nav', "{% include 'navbar.html' %}")

    def _replace_footer(self):
        self.tag_editor.replace_main_tag('footer', "{% include 'footer.html' %}")

    def _get_unique_scripts_block(self):
        return '\n'.join(self._get_unique_scripts())

    def _get_unique_scripts(self):
        return ["""<script src="{{% static '{0}' %}}"></script>""".format(script)
                for script in self.scripts if script not in self.common_scripts]

    def _get_replaced_html(self):
        return self.tag_editor.get_text()
