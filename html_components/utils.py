def block_wrapper(html_inside_block, block_name):
    return f'''{{% block {block_name} %}}
    {html_inside_block}
{{% endblock %}}\n'''
