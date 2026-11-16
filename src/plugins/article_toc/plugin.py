"""文章目录（TOC）插件。

cgw: 第9-10周新增插件。解析正文中的二级、三级标题，为缺失锚点的标题补上
id，并在正文开头插入目录；文章列表页的摘要不生成目录。标题数量过少时
不渲染，避免短文章出现无意义的目录块。
"""

import html
import logging
import re

from djangoblog.plugin_manage import hooks
from djangoblog.plugin_manage.base_plugin import BasePlugin
from djangoblog.plugin_manage.hook_constants import ARTICLE_CONTENT_HOOK_NAME

logger = logging.getLogger(__name__)

# cgw: 匹配二级、三级标题，属性串与标题内文分别捕获
HEADING_PATTERN = re.compile(r'<h([23])([^>]*)>(.*?)</h\1>', re.IGNORECASE | re.DOTALL)
# cgw: 剥离标题内部的标签，取纯文本用于目录展示
TAG_PATTERN = re.compile(r'<[^>]+>')
# cgw: 标题若已带 id（例如编辑器生成），直接沿用，不重复生成
ID_PATTERN = re.compile(r'''id\s*=\s*["']([^"']+)["']''', re.IGNORECASE)

# cgw: 少于该标题数量时认为目录无意义，不渲染
TOC_MIN_HEADINGS = 2


class ArticleTocPlugin(BasePlugin):
    """根据正文标题生成文章目录的插件。"""

    PLUGIN_NAME = '文章目录'
    PLUGIN_DESCRIPTION = '根据正文中的二级、三级标题生成目录并插入正文开头。'
    PLUGIN_VERSION = '1.0.0'
    PLUGIN_AUTHOR = '程光文'

    def register_hooks(self):
        """把目录生成挂到文章正文过滤钩子上。"""
        hooks.register(ARTICLE_CONTENT_HOOK_NAME, self.inject_toc)

    def inject_toc(self, content, *args, **kwargs):
        """在正文前插入目录。

        :param content: 已渲染为 HTML 的正文
        :param kwargs: 包含 ``is_summary``，列表页摘要模式直接跳过
        :return: 插入目录后的正文
        """
        if not content:
            return content
        if kwargs.get('is_summary'):
            return content
        try:
            return self._inject(content)
        except Exception as exc:
            # cgw: 目录属于增强功能，生成失败时退回原文，不影响正文展示
            logger.error('生成文章目录失败：%s', exc)
            return content

    def _inject(self, content):
        """扫描标题、补锚点并拼接目录。"""
        headings = []
        used_anchors = set()
        state = {'counter': 0}

        def replace_heading(match):
            """为单个标题补 id 并记录目录条目。"""
            level = match.group(1)
            attrs = match.group(2) or ''
            inner = match.group(3)
            text = TAG_PATTERN.sub('', inner).strip()
            if not text:
                return match.group(0)
            found = ID_PATTERN.search(attrs)
            if found:
                anchor = found.group(1)
            else:
                anchor = self._next_anchor(state, used_anchors)
                attrs = '%s id="%s"' % (attrs, anchor)
            used_anchors.add(anchor)
            headings.append((level, anchor, text))
            return '<h%s%s>%s</h%s>' % (level, attrs, inner, level)

        new_content = HEADING_PATTERN.sub(replace_heading, content)
        if len(headings) < TOC_MIN_HEADINGS:
            return content
        return self._render_nav(headings) + new_content

    @staticmethod
    def _next_anchor(state, used_anchors):
        """生成不与既有锚点冲突的序号锚点。"""
        while True:
            state['counter'] += 1
            anchor = 'toc-%d' % state['counter']
            if anchor not in used_anchors:
                return anchor

    @staticmethod
    def _render_nav(headings):
        """拼装目录 HTML，层级用左内边距区分。"""
        items = []
        for level, anchor, text in headings:
            indent = 'pl-0' if level == '2' else 'pl-4'
            items.append(
                '<li class="toc-item %s">'
                '<a class="toc-link text-muted-foreground hover:text-primary" href="#%s">%s</a>'
                '</li>' % (indent, html.escape(anchor), html.escape(text))
            )
        return (
            '<nav class="toc mb-6 rounded-xl border border-border bg-card px-4 py-3" aria-label="文章目录">'
            '<p class="toc-title mb-2 text-sm font-semibold text-foreground">文章目录</p>'
            '<ul class="toc-list space-y-1 text-sm">%s</ul>'
            '</nav>' % ''.join(items)
        )


plugin = ArticleTocPlugin()
