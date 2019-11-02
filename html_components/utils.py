def block_wrapper(html_inside_block, block_name):
    return f'''{{% block {block_name} %}}
    {html_inside_block}
{{% endblock %}}\n'''


def tag_wrapper(tag_name, text, **kwargs):
    if kwargs:
        attributes = ' ' + ' '.join([f'{k}="{v}"' for k, v in kwargs.items()])
    else:
        attributes = ''
    return '<{0}{2}>\n{1}\n</{0}>\n'.format(tag_name, text, attributes)


def static_script_src_convertor(links):
    return ''.join(["""<script src="{{% static '{0}' %}}"></script>\n""".format(link)
                      for link in links])


def static_css_href_convertor(hrefs):
    return ''.join(["""<link rel="stylesheet" href="{{% static '{0}' %}}">\n""".format(href)
            for href in hrefs])

