"""djangoblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.urls import re_path
from haystack.views import search_view_factory
from django.http import JsonResponse
import time

from blog.views import EsSearchView
from djangoblog.admin_site import admin_site
from djangoblog.elasticsearch_backend import ElasticSearchModelSearchForm
from djangoblog.feeds import DjangoBlogFeed
from djangoblog.sitemap import ArticleSiteMap, CategorySiteMap, StaticViewSitemap, TagSiteMap, UserSiteMap

sitemaps = {

    'blog': ArticleSiteMap,
    'Category': CategorySiteMap,
    'Tag': TagSiteMap,
    'User': UserSiteMap,
    'static': StaticViewSitemap
}

# 统一错误页处理入口，由 blog 应用提供 404、500 和 403 页面。
handler404 = 'blog.views.page_not_found_view'
handler500 = 'blog.views.server_error_view'
handle403 = 'blog.views.permission_denied_view'


# 健康检查接口：仅返回服务状态和当前时间，便于部署平台探测进程。
def health_check(request):
    """
    健康检查接口
    简单返回服务健康状态
    """
    return JsonResponse({
        'status': 'healthy',
        'timestamp': time.time()
    })

# 非本地化路由：国际化和健康检查接口不经过语言前缀。
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('health/', health_check, name='health_check'),
]
# 业务路由：后台、博客、评论、账号、OAuth、站点地图和搜索均在此汇总。
urlpatterns += i18n_patterns(
    re_path(r'^admin/', admin_site.urls),
    re_path(r'', include('blog.urls', namespace='blog')),
    re_path(r'mdeditor/', include('mdeditor.urls')),
    re_path(r'', include('comments.urls', namespace='comment')),
    re_path(r'', include('accounts.urls', namespace='account')),
    re_path(r'', include('oauth.urls', namespace='oauth')),
    re_path(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
            name='django.contrib.sitemaps.views.sitemap'),
    re_path(r'^feed/$', DjangoBlogFeed()),
    re_path(r'^rss/$', DjangoBlogFeed()),
    re_path('^search', search_view_factory(view_class=EsSearchView, form_class=ElasticSearchModelSearchForm),
            name='search'),
    re_path(r'', include('servermanager.urls', namespace='servermanager'))
    , prefix_default_language=False) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
