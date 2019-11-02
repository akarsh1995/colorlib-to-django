import shutil
from distutils.dir_util import copy_tree
from pathlib import Path

from html_components.html import Html


class DirReader:

    def __init__(self, template_dir: str):
        assert Path(template_dir).exists(), 'Directory does not exists'
        self.template_dir = Path(template_dir)
        self.to_dir = self.template_dir.parent.joinpath(f'{self.template_dir.name}_modified')
        if self.to_dir.exists():
            shutil.rmtree(self.to_dir)
        self.html_objects = self.get_html_files()
        self.make_copy_of_dir()

    def get_html_files(self):
        return [Html(path) for path in self.template_dir.glob('*html')]

    def make_copy_of_dir(self):
        copy_tree(str(self.template_dir), str(self.to_dir))
