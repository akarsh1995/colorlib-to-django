import re


class TagEditor:
    main_tag_pattern = r'(<{0}>((?:.|\n)*?)</{0}>)'
    js_script_tag_pattern = r'(<script src=\"(.+)\".+/script>)'
    css_pattern = r'(<link.*?(?:href=|url|import).*[\'\"]([^(http:)].*css)[\'\"]>)'

    def __init__(self, text: str):
        self._text = text

    def get_main_tag_content(self, tag):
        pattern = self.main_tag_pattern.format(tag)
        return re.search(pattern, self._text).group(0)

    def get_script_tags(self, only_src=True):
        return self._get_tags(self.js_script_tag_pattern, only_src)

    def get_css_tags(self, only_href=True):
        return self._get_tags(self.css_pattern, only_href)

    def _get_tags(self, pattern, only_link=True):
        result = map(lambda match: match.group(2 if only_link else 1),
                     re.finditer(pattern, self._text))
        return list(result)

    def replace_css_tags(self, replacement=''):
        self._replace_text(self.css_pattern, replacement)

    def replace_script_tags(self, replacement=''):
        self._replace_text(self.js_script_tag_pattern, replacement)

    def replace_main_tag(self, tag, replacement=''):
        self._replace_text(self.main_tag_pattern.format(tag), replacement)

    def _replace_text(self, pattern, replacement):
        self._text = re.subn(pattern, replacement, self._text)[0]

    def get_text(self):
        return self._text
