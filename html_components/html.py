from pathlib import Path

from .body import Body
from .head import Header
from .tag import TagEditor


class Html:

    def __init__(self, html_file_path: Path):
        self.html_file_path = html_file_path
        self.html_content = self._read_html()
        self.tag_editor = TagEditor(self.html_content)
        self.head = self._get_headers()
        self.body = self._get_body()

    def _read_html(self) -> str:
        """

        :return: html string
        """
        return self.html_file_path.read_text()

    def _get_headers(self) -> Header:
        return Header(self.tag_editor.get_main_tag_content('head', include_tags=False))

    def _get_body(self) -> Body:
        return Body(self.tag_editor.get_main_tag_content('body', include_tags=False))

    def get_modified_html(self):
        return self.head.get_header_block() + self.body.get_block_content()

    def write_html(self, dir_path: Path):
        dir_path.joinpath(self.html_file_path.name).write_text(self.get_modified_html())

    def __repr__(self):
        return self.head.__repr__() + self.body.__repr__()
