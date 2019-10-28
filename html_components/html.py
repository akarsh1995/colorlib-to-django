from pathlib import Path

from .body import Body
from .head import Header
from .tag import TagEditor


class Html:

    def __init__(self, html_file_path):
        self.dir_path = Path(html_file_path)
        self.html_content = self._read_html()
        self.tag_editor = TagEditor(self.html_content)

    def _read_html(self) -> str:
        """

        :return: html string
        """
        return self.dir_path.read_text()

    def get_headers(self) -> Header:
        return Header(self.tag_editor.get_main_tag_content('head'))

    def get_body(self) -> Body:
        return Body(self.tag_editor.get_main_tag_content('body'))
