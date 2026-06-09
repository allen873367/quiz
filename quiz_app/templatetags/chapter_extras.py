import re
from django import template

register = template.Library()


@register.filter
def chapter_topic(value):
    """
    從「第N章　Topic」中提取 Topic 名稱。
    例：『第11章　圖形結構』→『圖形結構』
         『第7章　樹狀結構』→『樹狀結構』
    """
    if not value:
        return value
    m = re.search(r'第\d+章\s*(.*)', value)
    return m.group(1) if m else value
