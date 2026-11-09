# szj: ===== comments 应用 · 评论树模板标签（第 7-8 周大作业精读与注释：孙子杰）=====
# szj: 模板用 parse_commenttree 把“扁平评论列表”整理成某条评论的全部后代（深度优先），
# szj: 用 show_comment_item 渲染单条评论并标注层级（决定缩进与样式）。
# szj: 本次质量改进：parse_commenttree 原实现每层递归都执行一次数据库查询（N+1），
# szj: 现改为一次性取出全部可见评论、在内存中按 parent_comment_id 建树，查询次数从 O(N) 降到 1。
"""评论模板标签。

提供两个自定义标签：
- ``parse_commenttree``：从整篇文章的评论列表中解析某条评论的全部后代评论；
- ``show_comment_item``：inclusion_tag，渲染单条评论并传入层级 depth。
"""

from django import template

register = template.Library()


@register.simple_tag
def parse_commenttree(commentlist, comment):
    """获得当前评论的所有子评论（深度优先顺序，含多级嵌套）。

    用法::

        {% parse_commenttree article_comments comment as childcomments %}
        {% for child in childcomments %}...{% endfor %}

    :param commentlist: 文章可见评论的 QuerySet（通常来自 Article.comment_list()）
    :param comment: 需要展开子树的父评论对象
    :return: 该评论所有后代评论组成的列表（按原始 QuerySet 顺序）
    """
    # szj: 关键优化：原实现为每个父节点单独 filter(parent_comment=c)，评论多时查询次数随层数增长；
    # szj: 这里先一次性把可见评论按 parent_comment_id 分桶，再在内存中做深度优先遍历。
    children_map = {}
    for item in commentlist.filter(is_enable=True):
        children_map.setdefault(item.parent_comment_id, []).append(item)

    datas = []

    def parse(parent):
        """深度优先收集 parent 的所有后代评论。"""
        for child in children_map.get(parent.id, []):
            datas.append(child)
            parse(child)

    parse(comment)
    return datas


@register.inclusion_tag('comments/tags/comment_item.html')
def show_comment_item(comment, ischild):
    """渲染单条评论（inclusion_tag）。

    :param comment: 评论对象
    :param ischild: 是否为子评论（True 时模板缩进更深）
    :return: 渲染上下文，depth 供模板决定层级样式
    """
    # szj: 子评论与顶层评论使用不同的缩进层级，depth 由 comment_item.html 消费。
    depth = 1 if ischild else 2
    return {
        'comment_item': comment,
        'depth': depth
    }
