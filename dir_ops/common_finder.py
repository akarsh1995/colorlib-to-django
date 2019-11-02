from functools import reduce

from .dir_read import DirReader


class CommonMatcher:
    def __init__(self, dir_reader_obj: DirReader):
        self.html_objects = dir_reader_obj.html_objects
        self.dir_obj = dir_reader_obj
        self.replace_common_css_scripts()

    def get_common_css(self):
        css = [html_object.head.css_hrefs for html_object in self.html_objects]
        return reduce(lambda x, y: list(set(x).intersection(set(y))), css)

    def get_common_scripts(self):
        scripts = [html_object.body.scripts for html_object in self.html_objects]
        return reduce(lambda x, y: list(set(x).intersection(set(y))), scripts)

    def replace_common_css_scripts(self):
        for html_obj in self.html_objects:
            html_obj.body.set_common_scripts(self.get_common_scripts())
            html_obj.head.set_common_css_hrefs(self.get_common_css())
