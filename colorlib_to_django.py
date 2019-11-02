from dir_ops.dir_read import DirReader
from dir_ops.edit_htmls import BaseGenerator, HtmlModifier


class ColorLib:
    def __init__(self, dir: str):
        d = DirReader(dir)
        self.b = BaseGenerator(d)
        self.h = HtmlModifier(d)

    def get_django_ready_template(self):
        self.b.write_base_html()
        self.h.write_modified_content()
