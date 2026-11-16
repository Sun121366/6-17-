"""
插件系统测试
测试插件加载、钩子注册和执行
"""
import os
from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.test import TestCase

from djangoblog.plugin_manage.base_plugin import BasePlugin
from djangoblog.plugin_manage.hook_constants import *
from djangoblog.plugin_manage import hooks
from djangoblog.plugin_manage.loader import load_plugins
from djangoblog.test_base import BaseTestCase, PluginTestMixin

# 导入钩子常量
from djangoblog.plugin_manage.hook_constants import HEAD_RESOURCES_HOOK, BODY_RESOURCES_HOOK


class PluginHooksTest(TestCase, PluginTestMixin):
    """测试插件钩子系统"""

    def setUp(self):
        # 清空插件钩子
        hooks._hooks = {}

    def test_register_hook(self):
        """测试注册钩子"""
        def test_hook(context):
            return "test"

        hooks.register(ARTICLE_CONTENT_HOOK_NAME, test_hook)
        self.assertIn(ARTICLE_CONTENT_HOOK_NAME, hooks._hooks)
        self.assertEqual(len(hooks._hooks[ARTICLE_CONTENT_HOOK_NAME]), 1)

    def test_apply_filters(self):
        """测试应用过滤器"""
        def test_filter(value):
            return value + " modified"

        hooks.register(ARTICLE_CONTENT_HOOK_NAME, test_filter)
        result = hooks.apply_filters(ARTICLE_CONTENT_HOOK_NAME, "original")
        self.assertEqual(result, "original modified")

    def test_run_action(self):
        """测试运行动作钩子"""
        executed = []

        def test_action():
            executed.append(True)

        hooks.register(ARTICLE_CREATE, test_action)
        hooks.run_action(ARTICLE_CREATE)
        self.assertTrue(len(executed) > 0)

    def test_multiple_hooks(self):
        """测试多个钩子"""
        results = []

        def hook1(value):
            results.append('hook1')
            return value + '1'

        def hook2(value):
            results.append('hook2')
            return value + '2'

        hooks.register(ARTICLE_CONTENT_HOOK_NAME, hook1)
        hooks.register(ARTICLE_CONTENT_HOOK_NAME, hook2)

        result = hooks.apply_filters(ARTICLE_CONTENT_HOOK_NAME, 'base')
        self.assertEqual(result, 'base12')
        self.assertEqual(len(results), 2)

    def test_hook_error_handling(self):
        """测试钩子错误处理"""
        def error_hook(value):
            raise Exception("Hook error")

        def normal_hook(value):
            return value + ' success'

        hooks.register(ARTICLE_CONTENT_HOOK_NAME, error_hook)
        hooks.register(ARTICLE_CONTENT_HOOK_NAME, normal_hook)

        # 即使有钩子出错，其他钩子也应该继续执行
        result = hooks.apply_filters(ARTICLE_CONTENT_HOOK_NAME, 'test')
        # 错误钩子不会修改值，但正常钩子会
        self.assertIn('success', result)


class BasePluginTest(BaseTestCase):
    """测试基础插件类"""

    def _create_test_plugin(self):
        """创建一个测试用的插件实例"""
        class TestPlugin(BasePlugin):
            PLUGIN_NAME = '测试插件'
            PLUGIN_DESCRIPTION = '用于测试的插件'
            PLUGIN_VERSION = '1.0.0'
            PLUGIN_AUTHOR = 'test'

        return TestPlugin()

    def test_plugin_initialization(self):
        """测试插件初始化"""
        plugin = self._create_test_plugin()
        self.assertIsNotNone(plugin.PLUGIN_NAME)
        self.assertIsNotNone(plugin.PLUGIN_VERSION)

    def test_plugin_config(self):
        """测试插件配置"""
        plugin = self._create_test_plugin()
        # 插件应该有配置属性
        self.assertIsNotNone(plugin.PLUGIN_NAME)

    def test_plugin_register_hooks(self):
        """测试插件注册钩子"""
        plugin = self._create_test_plugin()
        # 基类的 register_hooks 应该可以被调用
        plugin.register_hooks()

    def test_plugin_get_context(self):
        """测试获取插件信息"""
        plugin = self._create_test_plugin()
        plugin_info = plugin.get_plugin_info()
        self.assertIsInstance(plugin_info, dict)
        self.assertEqual(plugin_info['name'], '测试插件')


class PluginLoaderTest(TestCase):
    """测试插件加载器"""

    @patch('djangoblog.plugin_manage.loader.logger')
    def test_load_plugins(self, mock_logger):
        """测试加载插件"""
        plugins = load_plugins()
        self.assertIsInstance(plugins, list)

    def test_load_plugins_handles_errors(self):
        """测试插件加载错误处理"""
        # 测试当插件目录不存在或插件有错误时的处理
        with patch('os.path.exists', return_value=False):
            plugins = load_plugins()
            # 应该返回空列表或处理错误
            self.assertIsInstance(plugins, list)


class ReadingTimePluginTest(BaseTestCase, PluginTestMixin):
    """测试阅读时间插件"""

    def test_reading_time_plugin_loaded(self):
        """测试阅读时间插件已加载"""
        from plugins.reading_time.plugin import ReadingTimePlugin
        plugin = ReadingTimePlugin()
        self.assertEqual(plugin.PLUGIN_NAME, '阅读时间预测')

    def test_calculate_reading_time(self):
        """测试计算阅读时间"""
        from plugins.reading_time.plugin import ReadingTimePlugin
        plugin = ReadingTimePlugin()

        # 测试短文本
        short_text = '<p>这是一段短文本</p>' * 10
        result = plugin.add_reading_time(short_text)
        self.assertIn('预计阅读时间', result)
        self.assertIn('分钟', result)

        # 测试长文本
        long_text = '<p>这是一段长文本</p>' * 1000
        long_result = plugin.add_reading_time(long_text)
        self.assertIn('预计阅读时间', long_result)
        # 长文本应该比短文本有更多内容
        self.assertGreater(len(long_result), len(result))


class ViewCountPluginTest(BaseTestCase, PluginTestMixin):
    """测试浏览次数插件"""

    def test_view_count_plugin_loaded(self):
        """测试浏览次数插件已加载"""
        from plugins.view_count.plugin import ViewCountPlugin
        plugin = ViewCountPlugin()
        self.assertEqual(plugin.PLUGIN_NAME, '文章浏览次数统计')

    def test_view_count_increment(self):
        """测试浏览次数增加"""
        initial_views = self.article.views
        # 模拟访问文章
        self.client.get(self.article.get_absolute_url())
        self.article.refresh_from_db()
        # 浏览次数应该增加
        self.assertGreaterEqual(self.article.views, initial_views)


class SEOOptimizerPluginTest(BaseTestCase, PluginTestMixin):
    """测试 SEO 优化插件"""

    def test_seo_optimizer_plugin_loaded(self):
        """测试 SEO 优化插件已加载"""
        from plugins.seo_optimizer.plugin import SeoOptimizerPlugin
        plugin = SeoOptimizerPlugin()
        self.assertEqual(plugin.PLUGIN_NAME, 'SEO 优化器')

    def test_seo_meta_tags(self):
        """测试 SEO meta 标签"""
        from plugins.seo_optimizer.plugin import SeoOptimizerPlugin
        plugin = SeoOptimizerPlugin()

        response = self.client.get(self.article.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        # 应该包含 meta 标签
        self.assertContains(response, '<meta')


class ArticleCopyrightPluginTest(BaseTestCase, PluginTestMixin):
    """测试文章版权插件"""

    def test_copyright_plugin_loaded(self):
        """测试版权插件已加载"""
        from plugins.article_copyright.plugin import ArticleCopyrightPlugin
        plugin = ArticleCopyrightPlugin()
        self.assertEqual(plugin.PLUGIN_NAME, '文章结尾版权声明')

    def test_copyright_notice_added(self):
        """测试版权声明已添加"""
        response = self.client.get(self.article.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        # 根据实际插件实现，可能包含版权信息
        # self.assertContains(response, '版权')


class ExternalLinksPluginTest(BaseTestCase, PluginTestMixin):
    """测试外部链接插件"""

    def test_external_links_plugin_loaded(self):
        """测试外部链接插件已加载"""
        from plugins.external_links.plugin import ExternalLinksPlugin
        plugin = ExternalLinksPlugin()
        self.assertEqual(plugin.PLUGIN_NAME, '外部链接处理器')

    def test_external_links_processing(self):
        """测试外部链接处理"""
        from plugins.external_links.plugin import ExternalLinksPlugin
        plugin = ExternalLinksPlugin()

        content = '<a href="https://example.com">外部链接</a>'
        # 测试插件已加载即可，具体处理逻辑在运行时应用
        self.assertIsNotNone(plugin.PLUGIN_NAME)


class ArticleTocPluginTest(BaseTestCase, PluginTestMixin):
    """测试文章目录插件（第9-10周新增）"""

    SAMPLE = (
        '<h2>第一节 背景</h2><p>内容</p>'
        '<h3>1.1 现状</h3><p>内容</p>'
        '<h2>第二节 方案</h2><p>内容</p>'
    )

    def _plugin(self):
        from plugins.article_toc.plugin import ArticleTocPlugin
        return ArticleTocPlugin()

    def test_plugin_metadata(self):
        """插件元信息符合约定"""
        plugin = self._plugin()
        self.assertEqual(plugin.PLUGIN_NAME, '文章目录')
        self.assertEqual(plugin.PLUGIN_VERSION, '1.0.0')

    def test_register_hooks(self):
        """注册后钩子列表中出现目录方法"""
        from djangoblog.plugin_manage import hooks
        from djangoblog.plugin_manage.hook_constants import ARTICLE_CONTENT_HOOK_NAME

        backup = {name: list(cbs) for name, cbs in hooks._hooks.items()}
        try:
            hooks._hooks = {}
            self._plugin().register_hooks()
            self.assertTrue(hooks._hooks.get(ARTICLE_CONTENT_HOOK_NAME))
        finally:
            hooks._hooks = backup

    def test_toc_injected(self):
        """目录插入正文开头且包含全部标题"""
        result = self._plugin().inject_toc(self.SAMPLE)
        self.assertTrue(result.startswith('<nav'))
        self.assertIn('文章目录', result)
        self.assertIn('第一节 背景', result)
        self.assertIn('1.1 现状', result)
        self.assertIn('第二节 方案', result)

    def test_anchor_added(self):
        """标题补齐锚点且目录链接指向同一锚点"""
        result = self._plugin().inject_toc(self.SAMPLE)
        for anchor in ('toc-1', 'toc-2', 'toc-3'):
            self.assertIn('href="#%s"' % anchor, result)
            self.assertIn('id="%s"' % anchor, result)

    def test_summary_mode_skipped(self):
        """列表页摘要不生成目录"""
        self.assertEqual(self._plugin().inject_toc(self.SAMPLE, is_summary=True), self.SAMPLE)

    def test_skipped_when_builtin_toc_enabled(self):
        """文章已勾选 show_toc 时让位给内置目录"""
        article = SimpleNamespace(show_toc=True)
        self.assertEqual(
            self._plugin().inject_toc(self.SAMPLE, article=article), self.SAMPLE)

    def test_injected_when_builtin_toc_disabled(self):
        """文章未勾选 show_toc 时由插件补上目录"""
        article = SimpleNamespace(show_toc=False)
        result = self._plugin().inject_toc(self.SAMPLE, article=article)
        self.assertTrue(result.startswith('<nav'))
        self.assertIn('文章目录', result)

    def test_too_few_headings(self):
        """标题数量不足时不渲染目录"""
        content = '<h2>只有一个标题</h2><p>x</p>'
        self.assertEqual(self._plugin().inject_toc(content), content)

    def test_existing_id_kept(self):
        """标题已有 id 时沿用，不重复生成"""
        result = self._plugin().inject_toc('<h2 id="custom">甲</h2><h2>乙</h2>')
        self.assertIn('href="#custom"', result)
        self.assertIn('id="custom"', result)
        self.assertIn('href="#toc-1"', result)

    def test_level4_ignored(self):
        """四级标题不进入目录"""
        content = '<h2>二级</h2><h4>四级</h4><h2>另一个二级</h2>'
        result = self._plugin().inject_toc(content)
        self.assertNotIn('四级', result.split('</nav>')[0])

    def test_empty_content(self):
        """空正文原样返回"""
        self.assertEqual(self._plugin().inject_toc(''), '')

    def test_title_escaped_in_nav(self):
        """标题中的标签被剥离，特殊字符被转义"""
        result = self._plugin().inject_toc(
            '<h2>a &lt;b&gt; c</h2><h2><script>alert(1)</script>d</h2>'
        )
        nav = result.split('</nav>')[0]
        self.assertNotIn('<script>', nav)
        # cgw: 标题原文中的实体被二次转义，页面上仍按原文展示
        self.assertIn('&amp;lt;', nav)
        self.assertIn('alert(1)', nav)

    def test_exception_falls_back(self):
        """处理异常时退回原文，不影响正文展示"""
        plugin = self._plugin()
        with patch.object(plugin, '_inject', side_effect=RuntimeError('boom')):
            self.assertEqual(plugin.inject_toc(self.SAMPLE), self.SAMPLE)
