"""自定义过滤器"""


def get_datatime(content):
    content = str(content)
    result = content[:-7]
    return result


def get_title(title):
    if len(title) > 10:
        title = title[:10] + '...'
    return title