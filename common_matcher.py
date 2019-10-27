import pathlib
import re
import shutil
from distutils.dir_util import copy_tree
from functools import reduce


class TemplateDirRead:
    def __init__(self, template_dir):
        self.template_dir = pathlib.Path(template_dir)
        self.h_f_paths = self.template_dir.glob('*html')

    def get_file_names_and_paths(self):
        for file_path in self.h_f_paths:
            with file_path.open('r') as f:
                yield file_path.name, f.read()


def intersection(set1: set, set2: set):
    return set1.intersection(set2)


class CommonMatcher:
    css_pattern = r'(?:href=|url|import).*[\'\"]([^(http:)].*css)[\'\"]'
    js_pattern = r'(?:src=|url|import).*[\'\"]([^(http:)].*js)[\'\"]'
    replace_pattern_css = """<link rel="stylesheet" href="{{% static '{0}' %}}">"""
    replace_pattern_js = """<script src="{{% static '{0}' %}}"></script>"""
    found_patterns = {}
    common_patterns = {}

    def __init__(self, html_file_names_and_paths):
        self.html_file_paths = html_file_names_and_paths
        self.find_patterns()
        self.find_common_ones()

    def find_patterns(self):
        for file_name, text in self.html_file_paths:
            self.found_patterns[file_name] = {
                'css': set(self.find_css_patterns(text)),
                'js': set(self.find_js_patterns(text))
            }

    def find_js_patterns(self, text: str):
        return re.findall(self.js_pattern, text)

    def find_css_patterns(self, text: str):
        return re.findall(self.css_pattern, text)

    def find_common_ones(self):
        k, v = reduce(lambda x, y: ('common', {
            'css': intersection(x[1]['css'], y[1]['css']),
            'js': intersection(x[1]['js'], y[1]['js'])}), self.found_patterns.items())
        self.common_patterns['css'] = v['css']
        self.common_patterns['js'] = v['js']

    def get_common_tags(self):
        return list(self._get_common_css_tags()) + list(self._get_common_js_tags())

    def get_common_css_tags(self):
        return '\n'.join([self.replace_pattern_css.format(href) for href in self._get_common_css_tags()])

    def _get_common_css_tags(self):
        return self.common_patterns['css']

    def get_common_js_tags(self):
        return '\n'.join([self.replace_pattern_js.format(href) for href in self._get_common_js_tags()])

    def _get_common_js_tags(self):
        return self.common_patterns['js']


class Replacements:
    new_file_text = ''

    head_tag_pattern = r'(?<=<head>)(.|\n)*(?=</head>)'
    nav_pattern = r'(<nav (?:.|\n)+/nav>)'  # group 1
    body_pattern = r'(?<=<body>)(.|\n)*(?=</body>)'
    js_tag_pattern = r'<script src.+</script>'
    css_tag_pattern = r'<link.+\.css.+>'

    _block_extra_css: str
    _block_headers: str
    _block_content: str
    _block_extra_js: str

    def __init__(self, html_file_path: pathlib.Path):
        self.file_text = html_file_path.open().read()
        self.file_path = html_file_path

        self._block_headers = re.search(self.head_tag_pattern, self.file_text).group(0).strip()
        self._block_extra_css = '\n'.join(re.findall(self.css_tag_pattern, self._block_headers)).strip()
        self._block_content = re.search(self.body_pattern, self.file_text).group(0).strip()
        self._block_extra_js = self._get_script_elements().strip()

    def prep_html(self):
        self._add_extends_from_base()
        self._add_load_static_tag()
        self._add_block_headers()
        self._add_block_extra_css()
        self._add_block_content()
        self._add_block_extra_js()

    def replace_common_elems_from_new_text(self, common_elems):
        pattern = r'(.+(?:{}).+\n)'.format('|'.join(common_elems))
        self.new_file_text = re.subn(pattern, '', self.new_file_text)[0]

    def _add_block_headers(self):
        self._block_headers = re.subn(self.css_tag_pattern, '', self._block_headers)[0].strip()
        formatter = '{{% block headers %}}\n{}\n{{% endblock %}}\n'
        self.new_file_text += formatter.format(self._block_headers)

    def _add_load_static_tag(self):
        static_tag = '{% load static %}\n'
        self.new_file_text = f'{static_tag}{self.new_file_text}'

    def _add_extends_from_base(self):
        extends_tag = "{{% extends '{}' %}}\n".format('base.html')
        self.new_file_text = f'{extends_tag}{self.new_file_text}'

    def _add_block_extra_css(self):
        formatter = '''{{% block extra_css %}}\n{}\n{{% endblock %}}\n'''
        self.new_file_text += formatter.format(self._block_extra_css)

    def _add_block_content(self):
        self._remove_script_tags_from_content()
        formatter = '''{{% block content %}}\n{}\n{{% endblock %}}\n'''
        self.new_file_text += formatter.format(self._block_content)

    def _remove_script_tags_from_content(self):
        self._block_content = re.subn(self.js_tag_pattern, '', self._block_content)[0]

    def _add_block_extra_js(self):
        formatter = '''{{% block extra_js %}}\n{}\n{{% endblock %}}\n'''
        self.new_file_text += formatter.format(self._block_extra_js)

    def _get_script_elements(self):
        return '\n'.join(re.findall(self.js_tag_pattern, self.file_text))

    def _replace_navbar(self):
        # new file navbar
        # and replace with include tag in files
        replacement = '''{% include 'navbar.html' %}'''
        self.file_text = re.subn(self.nav_pattern, replacement, self.file_text)[0]

    def write_html(self):
        self.file_path.write_text(self.new_file_text)


class PrepDjangoTemplate:
    replace_pattern_image = r'<img.*?src=\"(.*?)\"[^\>]+>'
    nav_pattern = r'(<nav (?:.|\n)+/nav>)'  # group 1
    block_extra_js_format = '{{% block extra_js %}}{}{{% endblock %}}'
    block_extra_css_format = '{{% block extra_css %}}{}{{% endblock %}}'

    def __init__(self, template_dir: str):
        self.read_dir_obj = TemplateDirRead(template_dir=template_dir)
        self.to_dir: pathlib.Path = self.read_dir_obj.template_dir.parent.joinpath(
            f'{self.read_dir_obj.template_dir.name}_django')
        if self.to_dir.exists():
            shutil.rmtree(self.to_dir)
        self.common_matcher = CommonMatcher(self.read_dir_obj.get_file_names_and_paths())
        self.base_html = pathlib.Path('base.html').open('r').read()

    def prep_django_ready_template(self):
        self.copy_directory()
        self.make_replacements()
        self.write_base_template()

    def make_replacements(self):
        for file in self.to_dir.glob('*html'):
            r = Replacements(file)
            r.prep_html()
            r.replace_common_elems_from_new_text(self.common_matcher.get_common_tags())
            r.write_html()

    def write_base_template(self):
        self._prepare_base_template()
        self.to_dir.joinpath('base.html').write_text(self.base_html)

    def _prepare_base_template(self):
        self._add_common_css_in_base()
        self._add_common_js_in_base()

    def _add_common_js_in_base(self):
        self.base_html = self.base_html.replace('{{ common_js }}', self.common_matcher.get_common_js_tags())

    def _add_common_css_in_base(self):
        self.base_html = self.base_html.replace('{{ common_css }}', self.common_matcher.get_common_css_tags())

    def copy_directory(self):
        copy_tree(str(self.read_dir_obj.template_dir), str(self.to_dir))