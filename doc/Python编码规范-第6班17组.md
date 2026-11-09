# 软件6班17组《Python 编码规范》

## 1. 文档信息

### 1.1 基本信息

| 项目 | 内容 |
| --- | --- |
| 文档名称 | 《Python 编码规范》 |
| 所属课程作业 | 软件工程大作业（第 7—8 周任务(2)） |
| 小组名称 | 软件 6 班 17 组 |
| 项目名称 | DjangoBlog 博客系统（基于开源 DjangoBlog 二次开发） |
| 文档版本 | v1.0 |
| 编写日期 | 2026-11-09 |
| 文档状态 | 已发布，小组内部执行 |
| 编程语言 | Python 3.10 及以上（项目 README 记录的验证环境为 Python 3.11.9） |
| 框架版本 | Django 5.2（`src/requirements.txt` 锁定为 Django 5.2.17） |
| 数据库与前端 | MySQL 8.0、Vite 6、Tailwind CSS 3、Alpine.js、HTMX |
| 适用范围 | 仓库 `src/` 下小组自研与二次开发的 Python 代码，包括 `accounts`、`blog`、`comments`、`djangoblog`、`oauth`、`servermanager`、`plugins` 等应用，以及 `doc/` 下的辅助 Python 脚本 |
| 不适用范围 | 第三方依赖包、Django 框架内置源码、自动生成的迁移文件（`src/**/migrations/*.py` 只约束生成方式，不做逐行格式检查） |
| 维护方式 | 由小组文档负责人维护，经小组内部评审后升版；规范条文变更需在小组群内公示 |

### 1.2 小组成员

| 序号 | 姓名 | 学号 | 姓名缩写 | 注释署名格式 |
| --- | --- | --- | --- | --- |
| 1 | 程光文 | 2415304649 | cgw | `# cgw: 说明内容` |
| 2 | 唐文龙 | 2415304646 | twl | `# twl: 说明内容` |
| 3 | 何动 | 2415304647 | hd | `# hd: 说明内容` |
| 4 | 吴政 | 2415304648 | wz | `# wz: 说明内容` |
| 5 | 唐磊 | 2415304651 | tl | `# tl: 说明内容` |
| 6 | 孙子杰 | 2415304650 | szj | `# szj: 说明内容` |

> 姓名缩写用于第 5 章规定的个人注释署名，全组统一使用小写字母，同一缩写在全组内唯一。上表顺序不影响任务分工。

### 1.3 版本修订记录

| 版本 | 日期 | 修订人 | 修订内容 |
| --- | --- | --- | --- |
| v1.0 | 2026-11-09 | 6 班 17 组全体 | 首次发布：确定文档信息、总则、命名、排版、注释与文档字符串、Django 专项、安全、测试、Git 提交、工具与检查清单等规范内容 |

### 1.4 文档约定

1. 本文档中 **"必须 / 禁止"** 表示强制条款，违反即需在提交前整改；**"应 / 推荐"** 表示推荐条款，允许在说明理由后例外；**"可以"** 表示可选做法。
2. 代码示例使用 `python` 代码块；模板示例使用 `html` 代码块；命令示例使用 `powershell` 代码块。示例中的 `……` 表示省略的上下文代码。
3. 示例中的 `<缩写>` 指 1.2 节表中的姓名缩写，例如 `# szj: 说明`、`# twl: 说明`。
4. 项目路径约定：仓库根目录为 `D:\DjangoBlog`，Django 工程目录为 `D:\DjangoBlog\src`；文中的相对路径如 `blog/models.py` 均相对 `src/` 目录。
5. 本文档中的格式检查、静态检查与复杂度命令已在 `D:\DjangoBlog` 目录下实际执行验证，工具版本与基线结果见第 10 章；`manage.py` 系统检查与测试命令来自项目 README，需在数据库配置可用后执行。

---

## 2. 总则

### 2.1 制定依据

本规范以 **PEP 8《Style Guide for Python Code》** 和 **PEP 257《Docstring Conventions》** 为基础，参考 **Django 5.2 官方编码风格（Coding style）**，并结合本项目二次开发的实际情况制定：

- 项目基于开源项目 DjangoBlog（MIT License）二次开发，存量代码包含多种历史风格，规范需要兼顾"统一新代码"与"不破坏存量功能"；
- 项目是软件工程课程大作业，代码需要被教师和小组成员阅读、评审，注释与文档字符串的质量直接影响作业评分；
- 项目使用 Django 5.2 + MySQL + Vite，涉及模型、视图、模板、迁移、环境变量配置等 Django 特有场景，需要专项条款。

### 2.2 规范级别

| 级别 | 含义 | 典型条款 | 违反处理 |
| --- | --- | --- | --- |
| 必须 | 小组硬性约定，无正当理由不得违反 | 注释署名、禁止裸 `except`、禁止通配符导入、迁移文件不手改、敏感信息不入仓 | 提交前必须整改，评审不通过 |
| 推荐 | 提升可读性与可维护性的最佳实践 | 行宽 ≤ 120、外键写 `related_name`、视图优先类视图 | 原则上遵守，例外需在提交说明中注明原因 |
| 参考 | 交给 IDE 或格式化工具自动处理的细节 | 续行对齐、注释标点、空行数量 | 不作为单独退回理由 |

### 2.3 适用范围

| 范围 | 具体对象 | 执行要求 |
| --- | --- | --- |
| 业务应用代码 | `accounts/`、`blog/`、`comments/`、`oauth/`、`servermanager/`、`plugins/` 下的 Python 文件 | 全量遵守本规范 |
| 工程配置代码 | `djangoblog/settings.py`、`urls.py`、`wsgi.py`、`base_views.py`、`utils.py` 等 | 全量遵守，settings 另见第 6.6 节 |
| 模板与静态资源 | `templates/**/*.html`、`frontend/` 下的 JS/CSS | 命名与模板标签遵守第 3、6.4 节；Python 规范不约束 JS/CSS 格式 |
| 测试代码 | `src/**/test_*.py` 与 `tests.py` | 遵守第 8 章，命名与注释要求与业务代码一致 |
| 辅助脚本 | `doc/diagrams/` 下的 Python 绘图脚本等 | 遵守命名、注释与排版要求 |
| 迁移文件 | `src/**/migrations/*.py` | 禁止手改；格式问题不纳入检查范围（由 Django 自动生成） |
| 第三方代码 | `venv/`、`node_modules/` 及依赖包 | 不适用，也不得修改 |

### 2.4 执行方式

本规范采用"个人自查 + 工具检查 + 交叉评审"三级执行方式：

| 环节 | 执行人 | 主要动作 | 产出 |
| --- | --- | --- | --- |
| 个人提交前自查 | 代码作者 | 按第 10.7 节检查清单逐项核对；运行格式与测试命令 | 自查通过的本地提交 |
| 工具检查 | 代码作者 / 轮值检查人 | 运行 `pycodestyle`、`pylint`、`radon` 与 `python manage.py check` | 工具输出与整改记录 |
| 小组交叉评审 | 至少 1 名其他组员 | 检查命名、注释署名、Django 专项条款与安全条款；抽查测试用例 | 评审意见，合并前关闭 |
| 阶段性复查 | 文档负责人 | 每两周抽查一次规范执行情况，更新本文档 | 规范执行情况记录 |

### 2.5 新代码与存量代码的处理原则

1. 本规范**强制约束新增代码和本次修改涉及的代码**；对未被修改的存量代码，不要求一次性全量重排，避免产生大量与功能无关的改动。
2. 修改某个文件时，应顺带修复该文件中**明显且低风险**的规范问题（如缺少模块 docstring、行尾空白、个人注释未署名），但不做跨文件的大范围格式化。
3. 存量代码中与规范不一致的历史命名（如 URL name `detailbyid`、`postcomment`）保持兼容，不为了改名而大规模改动路由和模板；新增代码必须按本规范命名。
4. 所有例外情况应在提交说明中写明原因，必要时同步更新本文档。

---

## 3. 命名规范

### 3.1 通用命名规则

命名总体要求：使用有意义的英文单词，禁止使用无意义缩写和拼音（业务专有名词除外）；避免与 Python 关键字、内置函数重名；同一含义在全项目中用同一个词表达（例如统一用 `article` 而不是混用 `post`、`essay`）。

| 对象 | 命名风格 | 规则说明 | 正例 | 反例 |
| --- | --- | --- | --- | --- |
| 模块 / 包 | 全小写 + 下划线 | 简短名词或名词短语，能表达模块职责；包名不加前缀 | `blog/`、`comments/`、`user_login_backend.py`、`context_processors.py` | `BlogModels.py`、`myModule.py`、`utils2.py` |
| 类 | 大驼峰（PascalCase） | 名词或名词短语；视图类以 `View` 结尾；表单类以 `Form` 结尾；异常类以 `Error` 结尾 | `ArticleDetailView`、`CommentForm`、`CommentReaction`、`BlogSettings` | `article_detail_view`、`article`、`commentform` |
| 函数 / 方法 | 全小写 + 下划线（snake_case） | 动词或动宾短语，能看出行为；查询方法可用 `get_` / `list_` 前缀 | `get_absolute_url`、`form_valid`、`get_reactions_summary`、`clean_cache_view` | `GetURL`、`getURL`、`doIt` |
| 变量 | 全小写 + 下划线 | 名词或名词短语；循环变量用有意义的短名 | `parent_comment`、`reaction_type`、`page_number` | `pc`、`ReactionType`、`a1` |
| 常量 | 全大写 + 下划线 | 模块级常量，或类内常量；`TextChoices` 成员用全大写 | `PAGINATE_BY`、`SESSION_COOKIE_AGE`、`ARTICLE_COMMENTS`、`HOUR_10` | `paginateBy`、`articleComments`、`hour10` |
| 布尔量 / 布尔字段 | `is_` / `has_` / `can_` / `show_` / `need_` 等前缀 | 名称应能读成"是否……"；不推荐用 `flag`、`status` 这类含糊词表示布尔 | `is_enable`、`show_toc`、`has_reacted`、`comment_need_review`、`created` | `enable`、`flag`、`bool1` |
| 私有成员 | 单下划线前缀 | 仅模块/类内部使用；双下划线名称改写只用于确需避免子类冲突的场景 | `_convert_markdown()`、`_es_config`、`_parse_category()` | `__helper()` 滥用、`privateMethod()` |
| 测试方法 | `test_` 前缀 + 行为 + 条件 | 见第 8.2 节 | `test_article_created_as_draft_by_default` | `test1`、`test_it` |

### 3.2 Django 模型与字段命名

| 位置 | 命名要求 | 项目正例 | 反例 |
| --- | --- | --- | --- |
| 模型类名 | 单数大驼峰，能对应一张业务表 | `Article`、`Category`、`Comment`、`CommentReaction` | `Articles`、`article_table` |
| 模型字段 | 全小写 + 下划线；外键字段名用关联对象名，不额外加 `_id` 后缀 | `pub_time`、`parent_comment`、`creation_time`、`reaction_type` | `PubTime`、`author_id`（字段定义时） |
| 外键 `related_name` | 用复数或语义化名称，避免默认的 `xxx_set`；新增外键必须显式指定 | `CommentReaction.comment` 使用 `related_name='reactions'` | `related_name='+'` 随意禁用反向查询 |
| 枚举 / 选项 | 用 `TextChoices` 或模块级常量元组，成员全大写；同一模型内保持一种写法 | 项目 `LinkShowType(models.TextChoices)`；`Article.STATUS_CHOICES` 元组常量 | 散落在方法内的魔法字符串 `'p'`、`'d'` |
| 反向关系 | 模板和视图中优先用 `related_name` 访问，如 `comment.reactions.all()` | `comment_set` 为 Django 默认反向名，已存在可保留 | 新代码继续依赖默认名导致语义不清 |

### 3.3 URL 与模板命名

| 对象 | 命名要求 | 项目示例 | 说明 |
| --- | --- | --- | --- |
| URL name | 小写 + 下划线，语义化；新增用"资源_动作"风格 | 存量：`index`、`detailbyid`、`postcomment`、`comment_react`；新增：`article_detail`、`comment_create` | 存量名保持兼容，不重命名；新增名不得使用 `test`、`url1` 等占位名 |
| 应用 namespace | 与 `app_name` 含义一致，全小写 | `blog`、`comments`、`accounts`、`oauth`、`servermanager` | 根 `urls.py` 的 `include(..., namespace=...)` 与各应用 `app_name` 见 6.3 节 |
| 模板文件 | 全小写 + 下划线，按应用分目录 | `blog/article_detail.html`、`account/login.html`、`comments/tags/post_comment.html`、`share_layout/nav.html` | 不要用 `ArticleDetail.html`；通用模板放 `templates/share_layout/` |
| 模板标签模块 | 全小写 + 下划线，放在应用 `templatetags/` 目录 | `blog/templatetags/blog_tags.py`、`blog_tags.py` 中的 `register = template.Library()` | 一个应用一个主标签模块，避免碎片化 |
| 缓存键 | 模块级常量集中定义，统一前缀 | `djangoblog/constants.py` 中的 `CacheKey.ARTICLE_COMMENTS` | 禁止在业务代码里手写字符串缓存键 |

### 3.4 命名补充约定

1. 常用缩写只允许 `id`、`url`、`api`、`html`、`json`、`db`、`pk`、`seo`、`csrf`、`orm` 等通用写法；禁止自造缩写（如 `usr`、`mgr`、`artcl`）。
2. 类名、函数名、变量名不得使用中文；中文只用于注释、docstring、`verbose_name` 等面向用户或读者的文本。
3. 避免单字母变量名 `l`、`I`、`O`（易与数字 `1`、`0` 混淆）；循环索引可用 `i`、`j`，但业务循环优先用有意义的元素名。
4. 命名一旦发布到小组主干，不得随意修改；确需修改时必须同步更新所有引用、URL 与模板，并在提交说明中注明影响范围。

---

## 4. 排版规范

### 4.1 缩进与行宽

| 项目 | 要求 | 说明 |
| --- | --- | --- |
| 缩进 | 4 个空格，禁止 Tab | 与 Django 官方风格一致；编辑器统一设置"Tab 转 4 空格" |
| 续行缩进 | 与开括号对齐，或统一额外缩进 4 空格 | 同一文件内保持一种续行风格 |
| 代码行宽 | **≤ 120 字符** | 见下方说明；超长时用括号换行，禁止用反斜杠硬续行（`with`、`assert` 等语法必须续行的情况除外） |
| 注释与 docstring 行宽 | 建议 ≤ 100 字符 | 中文按一个汉字约等于两个西文字符的显示宽度估算，避免阅读时横向滚动 |
| 文件末尾 | 保留且仅保留 1 个换行符 | 避免 `W292 no newline at end of file` |
| 行尾 | 不得有空白字符 | 避免 `W291`、`W293` 告警，减少无意义 diff |

**为什么本项目取 120 字符而不是 PEP 8 的 79 字符：**

1. 现代开发环境普遍使用宽屏显示器，79 字符限制会导致 Django 的 URL 模式、`verbose_name=_('...')`、f-string 日志等代码被过度拆行，反而降低可读性；
2. Django 官方编码风格明确允许放宽行宽（当前官方代码按 `black` 的 88 字符执行，历史上长期使用 119 字符），本项目取整为 120，与 Django 生态常见配置（`flake8 max-line-length=119`）接近；
3. 对本项目存量代码全量统计（152 个 `.py` 文件、18122 行），以 120 为上限时非迁移代码仅 14 行超限、最长 126 字符；若改用 79 字符，超限行数会大幅增加，与"新代码统一、存量不制造无关改动"的原则冲突；
4. 120 字符仍能保证在 1080P 分辨率下并排 diff 对比时无需横向滚动，是可读性与迁移成本之间的平衡点。

### 4.2 空行

| 场景 | 空行数 | 示例 |
| --- | --- | --- |
| 模块级函数、类之间 | 2 个空行 | `blog/models.py` 中 `class Article` 与 `class Category` 之间 |
| 类内方法之间 | 1 个空行 | `Article.get_absolute_url` 与 `Article.get_category_tree` 之间 |
| 函数内部逻辑块之间 | 0—1 个空行，按语义分段 | 按"校验 / 组装 / 保存 / 返回"分段 |
| `class Meta` 与字段定义之间 | 1 个空行 | 字段定义结束、`class Meta` 之前空一行 |
| 文件末尾 | 1 个换行符 | 不是 2 个空行，也不是没有换行 |
| 连续空行 | 禁止 3 个及以上 | 避免 `E303 too many blank lines` |

### 4.3 括号、逗号与引号

| 场景 | 正例 | 反例 |
| --- | --- | --- |
| 函数调用 / 参数 | `get_object_or_404(Article, pk=article_id)` | `get_object_or_404 ( Article , pk = article_id )` |
| 多行调用 | 每行一个参数、行尾逗号（magic trailing comma）、右括号独占一行 | 参数挤在一行超长、右括号跟在最后一个参数后 |
| 关键字参数 | `max_length=200`（等号两侧无空格） | `max_length = 200` |
| 默认参数 / 类型注解 | `def get_markdown(value: str = '') -> str:` | `def get_markdown(value:str='')->str:` |
| 列表 / 字典 | `{'name': 'blog', 'status': 'p'}` | `{ 'name':'blog','status':'p' }` |
| 字符串引号 | 同一文件保持一致；本项目新增代码统一用单引号 `'...'`；字符串内含单引号时改用双引号 | 同一文件混用 `'a'` 与 `"b"`；无必要地三层嵌套转义 |
| docstring 引号 | 统一用三双引号 `"""..."""` | 单引号 docstring `'''...'''` 与双引号混用 |
| 运算符 | `a + b`、`x == y`、`i += 1` | `a+b`、`x==y`、`i+=1` |

### 4.4 import 分组顺序

本项目 import 按四组排列，组内按模块名的字母顺序排列，组与组之间空 1 行，最后一组 import 与下面的模块级代码之间空 2 行：

1. 标准库（`os`、`logging`、`re`、`sys`）
2. 第三方库（`mdeditor`、`uuslug`、`bleach`、`haystack` 等）
3. Django 框架（`django.conf`、`django.db`、`django.urls` 等）
4. 本项目模块（`djangoblog.*`、`blog.*`、`comments.*`、`accounts.*`）

【正例】

```python
"""博客核心数据模型。

本模块集中定义文章、分类、标签、友情链接、侧边栏和网站配置等模型。
"""

import logging
import re

from mdeditor.fields import MDTextField
from uuslug import slugify

from django.conf import settings
from django.db import models
from django.urls import reverse

from djangoblog.constants import CacheKey
from djangoblog.utils import cache_decorator

logger = logging.getLogger(__name__)
```

【反例】

```python
import os, sys, re                      # 一行导入多个模块，且顺序混乱
from django.db.models import *          # 禁止通配符导入
import blog.models                      # 与本项目 import 混在 Django 组中
from . import views                     # 相对导入与绝对导入混用且未分组
```

**硬性规定：**

1. 禁止 `from xxx import *`（通配符导入），必须显式列出被导入对象；确需大量导入时使用 `import module`；
2. 禁止在函数体内重复导入可在模块顶层安全导入的模块；仅用于解决循环导入的局部导入必须加注释说明原因；
3. 禁止保留未使用的 import；删除代码时同步删除对应 import；
4. 同一文件内不得混用相对导入和绝对导入，本项目统一使用绝对导入（`from blog.models import Article`）。

### 4.5 其他排版约定

1. 模块级代码（常量、类、函数）按"常量 → 类 → 函数"顺序组织；类内顺序按 Django 官方建议：字段 → 自定义管理器 → `class Meta` → `__str__` 等魔法方法 → `save()` → `get_absolute_url()` → 自定义方法。
2. 禁止在 `if`、`for`、`while`、`try` 等语句的同一行书写多条语句（如 `if x: y = 1`）。
3. 禁止使用 `l = 1` 这类易混淆变量名；禁止赋值给 `id`、`type`、`list`、`dict` 等内置名（Django 模型字段 `type` 属于存量例外，新增字段避免）。
4. 所有 `.py` 文件使用 UTF-8 编码，默认使用 LF 或 CRLF 均可，但同一文件内保持一致；文件首部不需要写 `# encoding: utf-8`。
5. 简单脚本入口使用 `if __name__ == '__main__':` 保护；Django 管理命令使用 `BaseCommand` 子类，不写成脚本。

---

## 5. 注释与文档字符串规范（重点）

注释与文档字符串是本项目课程作业的硬性要求，也是小组协作中最容易失控的部分。本项目在开源 DjangoBlog 基础上进行了大量中文注释与业务说明补充，第 5 章对"谁写的、写在哪、写什么、怎么写"作出统一规定，所有组员必须执行。

### 5.1 注释总体原则

| 编号 | 原则 | 具体要求 |
| --- | --- | --- |
| 1 | 注释解释"为什么"，不是翻译"是什么" | 代码本身能看懂的不写注释；注释说明设计原因、业务规则、边界条件、性能或安全考虑 |
| 2 | 注释使用中文 | 语句通顺，使用中文标点；专业术语、类名、字段名保留英文，如"通过 `select_related` 预加载作者" |
| 3 | 注释与代码同步更新 | 修改逻辑必须同步修改注释；不能让注释与代码矛盾，"注释比代码旧"视为缺陷 |
| 4 | 公开内容必须有文档字符串 | 模块、类、公开函数/方法、视图类、模板标签、管理命令必须有 docstring |
| 5 | 注释要具体 | 写清条件、单位、默认值、副作用、失败时的行为，不写"处理数据""初始化"这类空话 |
| 6 | 不保留废弃代码 | 被注释掉的旧代码、调试输出、临时 print 不得提交，用 Git 历史找回 |
| 7 | 注释不含敏感信息 | 禁止在注释中写数据库密码、密钥、Token、手机号等 |
| 8 | 注释不能代替清晰命名 | 优先通过命名表达意图；命名已清晰时不再重复注释 |
| 9 | 个人注释必须署名 | 按 5.2 节规定以姓名缩写打头，便于课程检查和责任追溯 |

### 5.2 个人注释署名约定（小组硬性要求）

本项目所有由小组成员新增的说明性 Python 注释，**必须以"姓名缩写 + 半角冒号 + 一个空格"打头**，格式为：

```python
# <缩写>: <说明内容>
```

其中 `<缩写>` 取自 1.2 节的姓名缩写表，全部小写；冒号使用半角 `:`；冒号后必须空一格。例如孙子杰的注释写作 `# szj: 说明`，唐文龙的注释写作 `# twl: 说明`，程光文的注释写作 `# cgw: 说明`。示例：

```python
# szj: 评论关闭时禁止继续提交，防止绕过前端隐藏按钮。
# twl: 数据库连接信息优先从环境变量读取，仓库中不保存真实密码。
# cgw: 该查询命中 article 表组合索引 idx_type_status_pub。
```

**署名规则明细：**

| 编号 | 规则 | 说明与示例 |
| --- | --- | --- |
| 1 | 个人新增的模块说明、块注释、行内注释、TODO/FIXME 都必须署名 | `# hd: 兼容旧数据中缺失 slug 的记录，缺省值由模型层补齐。` |
| 2 | 模块级个人署名注释放在模块 docstring 之后 | 见 5.3 节正例；不要在模块 docstring 第一行之前插入长篇个人说明 |
| 3 | 行内注释同样署名，且注释前至少空 2 个空格 | `if article.comment_status == 'c':  # wz: 评论关闭时拒绝提交` |
| 4 | 多行块注释只在首行署名，续行用同缩进的 `#` 说明 | 见 5.6 节正例 |
| 5 | 修改他人注释时不改写原署名；如需更正，另起一行以本人缩写说明原因和日期 | `# twl: 2026-11-09 修订：审核开关默认值已改为关闭。` |
| 6 | TODO / FIXME 统一格式 | `# TODO(szj): 待补充评论表情的缓存失效逻辑，计划 2026-11-20 前完成。` |
| 7 | 不得冒用他人缩写，不得写"组员""作者"等匿名署名 | 课程检查时按缩写核对到人；缩写表见 1.2 节 |
| 8 | 直接继承自开源项目的英文注释保持原样 | 不强制改写，但新增的中文说明仍须署名；不把他人注释改写成自己署名 |
| 9 | 模板与前端注释可选署名 | 模板：`{# szj: 评论关闭时隐藏评论框 #}`；JS/CSS 注释可参考同一规则 |

> 说明：项目存量代码中已有的 `[TWL/唐文龙]` 形式署名属于早期写法，保持兼容、不做批量改写；新增注释统一采用本节规定的 `# <缩写>: ` 形式，保证全组格式一致。

### 5.3 模块级注释与文档字符串

**要求：**

1. 每个 `.py` 文件**必须**包含模块 docstring，且必须是文件的第一条语句（前面可以有注释和 shebang，但 docstring 必须是第一个语句，保证 `模块.__doc__` 可用）。
2. 模块 docstring 至少说明三项内容：模块职责（这个文件解决什么问题）、主要内容（核心类 / 函数 / 视图）、依赖与注意事项（依赖哪些应用、是否有副作用、被谁使用）。
3. 纯包目录的 `__init__.py` 可以只写一行说明；空文件也建议保留一行职责说明。
4. 个人对模块做整体整理时，在模块 docstring 之后增加一行署名说明，格式为 `# <缩写>: <整理内容与日期>`。
5. 模块中如有重要的全局常量、缓存策略、注册副作用（如 `template.Library()`、Haystack 索引），应在 docstring 或相邻注释中说明。

【正例】`blog/models.py` 风格（模块职责 + 个人整理说明 + 导入分组）：

```python
"""博客核心数据模型。

本模块集中定义文章、分类、标签、友情链接、侧边栏和网站配置等模型。
模型之间的外键和多对多关系由 Django ORM 映射到 MySQL 数据表及关联表。
模型方法的返回值与缓存行为见各类 docstring；本模块不处理 HTTP 请求。
"""

# twl: 本模块中新增的中文模型说明与业务注释由唐文龙于 2026-10-07 补充整理。

import logging

from django.conf import settings
from django.db import models

from djangoblog.constants import CacheKey

logger = logging.getLogger(__name__)
```

【反例】缺少模块 docstring、注释无信息量、职责不清：

```python
# 模型相关的东西
import logging

from django.db import models


class Article(models.Model):
    # 标题
    title = models.CharField(max_length=200)
    ...
```

存在的问题：没有模块 docstring，阅读者无法快速判断文件职责；`# 标题` 属于对代码的重复翻译，没有说明约束条件（如唯一性、长度依据）。

### 5.4 类级文档字符串

**要求：**

1. 所有类（模型、视图、表单、模板标签辅助类、异常类等）**必须**有类 docstring。
2. 类 docstring 采用"一行概述 + 空行 + 详细说明"的 PEP 257 结构：第一行说明类是什么，空一行后说明职责、字段关系、使用约束、线程/缓存等注意事项。
3. 模型类重点说明**关联关系与业务含义**（外键指向、是否允许为空、级联删除影响）；视图类重点说明**URL、权限、请求方法、失败处理**；表单类说明字段来源与校验重点；抽象基类说明子类必须实现什么。
4. 类内方法数量较多时，可在 docstring 末尾用 `Attributes:` 列出关键字段；不为每个显然的字段重复写注释。

【正例】模型类（对应项目中 `Comment` 模型的职责说明）：

```python
class Comment(models.Model):
    """文章评论模型。

    author 指向评论用户，article 指向被评论文章；parent_comment 通过自关联
    表达回复关系，为空表示顶层评论。is_enable 表示评论是否通过审核并展示，
    由站点配置 BlogSettings.comment_need_review 决定默认值。

    Attributes:
        body: 评论正文，最大长度 300。
        is_enable: 是否已通过审核，默认 False。
    """

    body = models.TextField('正文', max_length=300)
    ...
```

【正例】视图类（说明访问方式、权限与依赖，便于评审）：

```python
class CommentPostView(AuthenticatedFormView):
    """文章评论提交视图。

    URL: article/<article_id>/postcomment
    权限: 必须登录（AuthenticatedFormView 已统一处理登录跳转和 CSRF 保护）。
    成功: 保存评论后重定向到文章详情页的评论区锚点。
    """

    form_class = CommentForm
    template_name = 'blog/article_detail.html'
    ...
```

【反例】类 docstring 缺失或用无信息量注释代替：

```python
class Comment(models.Model):
    # 评论模型
    body = models.TextField('正文', max_length=300)
```

### 5.5 函数与方法文档字符串

**要求：**

1. 所有公开函数、公开方法、视图类钩子（`form_valid`、`form_invalid`、`get_context_data`、`dispatch`）、模板标签函数、管理命令的 `handle()` 必须有 docstring。
2. 简单函数（一眼可懂的 getter、`__str__`）可用一行 docstring；复杂函数按需包含 `Args`、`Returns`、`Raises` 三段，说明参数含义、返回结构、可能抛出的异常。
3. docstring 说明"行为与约束"，不逐行复述代码；涉及查询次数、缓存、副作用时必须写明。
4. Django 视图方法的 docstring 要写清业务职责和失败分支，而不是重复"Django 默认行为"之类的框架知识。
5. 测试方法的 docstring 写"该用例验证什么预期行为"，见第 8 章。

【正例】公开业务方法（含返回结构说明，对应项目中评论反应统计方法）：

```python
def get_reactions_summary(self, user=None):
    """汇总当前评论的 Emoji 反应统计。

    Args:
        user: 当前登录用户；未登录时传 None，用于判断该用户是否已反应。

    Returns:
        dict: 以 Emoji 字符为键，值为包含 count 和 has_reacted 的统计字典。
    """
    reactions = CommentReaction.objects.filter(
        comment=self,
    ).values('reaction_type').annotate(count=Count('id'))

    result = {}
    for reaction in reactions:
        emoji = reaction['reaction_type']
        result[emoji] = {
            'count': reaction['count'],
            'has_reacted': False,
        }
    return result
```

【正例】视图钩子（说明业务职责与失败分支）：

```python
def form_valid(self, form):
    """校验业务条件、补全评论关联信息并保存，成功后跳转到评论区。

    评论开关为关闭状态时，通过 form.add_error() 写入表单错误并返回
    form_invalid，不抛出未处理异常。
    """
    article = get_object_or_404(Article, pk=self.kwargs['article_id'])
    ...
```

【反例】无 docstring、返回结构靠猜、参数含义不明：

```python
def get_reactions_summary(self, user=None):
    reactions = CommentReaction.objects.filter(comment=self)
    result = {}
    ...
    return result
```

问题：调用方不知道 `result` 的键和值结构，也不知道 `user` 参数的作用；后续修改极易破坏调用方。

### 5.6 核心代码块与关键行注释

**必须写注释的核心代码场景：**

| 场景 | 注释应说明什么 | 项目中的典型位置 |
| --- | --- | --- |
| 复杂 ORM 查询与性能优化 | 为什么这样过滤、为什么预加载、预期查询次数 | `ArticleDetailView.get_context_data` 的 `select_related` / `prefetch_related` |
| 业务状态判断与权限控制 | 条件含义、拒绝原因、避免的绕过方式 | `CommentPostView.form_valid` 的评论开关判断 |
| 缓存读写与失效 | 缓存键含义、过期时间、何时失效 | `Article.comment_list`、`djangoblog/constants.py` 中 `CacheKey` 的使用处 |
| 异常兜底 | 为什么捕获、捕获后返回什么、是否记录日志 | 模板标签的格式化失败处理、外部接口调用 |
| 安全过滤 | 白名单 / 转义依据、为什么不能信任输入 | `djangoblog/utils.py` 的 `sanitize_html` |
| 兼容性处理与临时方案 | 兼容哪个版本 / 数据、何时可以删除 | 旧数据迁移、第三方接口兼容 |

**块注释写法：** 注释写在被说明代码的上方，缩进与代码一致；多行块注释只在首行署名，续行用同缩进的 `#`。

【正例】块注释说明性能优化原因：

```python
# szj: 先一次性预加载作者和子评论作者，避免模板渲染时逐条查询（N+1）。
parent_comments = Comment.objects.filter(
    article=self.object,
    parent_comment=None,
    is_enable=True,
).select_related('author').prefetch_related(
    'comment_set__author',
).order_by('-id')
```

【正例】关键行内注释：注释与代码之间至少 2 个空格，只补充一个关键信息，不写长句：

```python
if not settings.comment_need_review:
    # twl: 站点未开启评论审核时，评论保存后直接通过审核。
    comment.is_enable = True

comment.save()  # szj: 保存后 form_valid 返回重定向，不在此处渲染模板。
```

【反例】注释翻译代码、无署名、并掩盖 N+1 问题：

```python
# 把查询结果放到 comments 里
comments = Comment.objects.filter(article=article)

# 循环
for comment in comments:
    # 获取作者昵称
    print(comment.author.nickname)
```

【反例】注释与代码矛盾（比没有注释更危险）：

```python
# szj: 评论默认直接展示（审核已开启）
comment.is_enable = False
```

> 注释与代码矛盾时，阅读者会优先相信注释，导致排查方向错误；一旦修改逻辑，必须同步检查相邻注释。

### 5.7 文档字符串标准模板

新增公开函数时可复制以下模板并按需删减段落；简单函数只保留第一行即可。

```python
def function_name(param1, param2=None):
    """一句话说明函数作用。

    Args:
        param1: 参数含义、取值范围或格式要求。
        param2: 参数含义；默认 None 表示什么行为。

    Returns:
        返回值的类型与含义；无返回值时写 None。

    Raises:
        ValueError: 什么条件下会抛出该异常。
    """
```

### 5.8 注释与文档字符串检查表

| 编号 | 检查项 | 通过标准 |
| --- | --- | --- |
| 1 | 模块 docstring | 每个 `.py` 文件首条语句为模块 docstring，说明职责、主要内容和依赖 |
| 2 | 类 docstring | 所有类都有 docstring；模型说明关联关系，视图说明 URL、权限、失败处理 |
| 3 | 函数 docstring | 公开函数/方法、视图钩子、模板标签、管理命令均有 docstring；复杂函数有 Args/Returns/Raises |
| 4 | 个人注释署名 | 所有个人新增注释以 `# <缩写>: ` 打头，缩写在 1.2 节表内，冒号半角、后接一个空格 |
| 5 | 注释语言 | 注释与 docstring 为中文；术语与代码标识符保留英文 |
| 6 | 注释内容 | 解释为什么与约束条件，不重复翻译代码，不写"处理数据"等空话 |
| 7 | 同步性 | 修改代码时同步更新注释，无过期、矛盾注释 |
| 8 | 核心逻辑 | 复杂查询、权限判断、缓存、异常兜底、安全过滤处均有注释 |
| 9 | 废弃内容 | 无被注释掉的旧代码、调试 print、临时 TODO 残留（TODO 必须带署名与期限） |
| 10 | 敏感信息 | 注释中不含密码、密钥、Token、个人信息 |
| 11 | 行内注释 | 与代码至少间隔 2 个空格，内容简短，不写长段落 |
| 12 | 文档字符串格式 | 三双引号；首行一句话；类 docstring 与详细说明之间空行；无多余空行和空白字符 |

---

## 6. Django 专项规范

本章针对 Django 5.2 项目中的模型、视图、路由、模板标签、迁移、配置、查询与异常处理提出专项要求。项目使用自定义用户模型 `accounts.BlogUser`，模型之间关联较多（文章、分类、标签、评论、表情反应），以下条款须与第 3、5 章配合执行。

### 6.1 模型规范

| 编号 | 规范项 | 级别 | 要求 | 项目示例 |
| --- | --- | --- | --- | --- |
| 1 | 字段命名 | 必须 | 全小写 + 下划线，不用驼峰，不额外加 `_id` 后缀 | `pub_time`、`parent_comment`、`creation_time` |
| 2 | `verbose_name` | 必须 | 使用 `django.utils.translation.gettext_lazy` 的 `_()` 包裹，后台与表单展示中文；新增模型和新增字段必须提供 | `title = models.CharField(_('title'), max_length=200)` |
| 3 | 选项 / 枚举 | 必须 | 使用 `TextChoices` 或模块级常量元组，禁止在业务代码中散落 `'p'`、`'d'` 等魔法值 | `LinkShowType(models.TextChoices)`、`Article.STATUS_CHOICES` |
| 4 | 外键 | 必须 | 显式写 `on_delete`；新增业务外键必须写语义化 `related_name`，便于反向查询 | `CommentReaction.comment` 使用 `related_name='reactions'` |
| 5 | `class Meta` | 必须 | 定义 `verbose_name` 与 `verbose_name_plural`；有列表展示的模型应定义稳定的 `ordering` | `Article.Meta` 的 `ordering = ['-article_order', '-pub_time']` |
| 6 | 索引 | 推荐 | 高频过滤/排序字段建组合索引，命名 `idx_<字段缩写>`；不为低选择性字段单独建索引 | `idx_type_status_pub`、`idx_status_views`、`idx_enable_id` |
| 7 | 单例配置 | 必须 | 只能存在一条记录的配置模型，在 `clean()` 中校验并抛出 `ValidationError` | `BlogSettings.clean()` |
| 8 | `__str__` | 必须 | 返回可读文本，便于后台与日志排查 | `Article.__str__` 返回 `self.title` |
| 9 | 模型方法 | 必须 | 业务方法写 docstring；跨表跳转 URL 使用 `reverse()`，不硬编码路径 | `Article.get_absolute_url()`、`Comment.get_reactions_summary()` |
| 10 | 迁移 | 必须 | 字段变更通过 `makemigrations` / `migrate` 完成，不手改迁移文件 | 见 6.5 节 |
| 11 | 抽象基类 | 推荐 | 公共字段抽到抽象基类，抽象方法用 `@abstractmethod` 声明，并写子类义务 | `blog.models.BaseModel` |

【正例】外键、`verbose_name`、唯一约束与索引：

```python
class CommentReaction(models.Model):
    """评论的 Emoji 反应（点赞）。"""

    comment = models.ForeignKey(
        Comment,
        verbose_name=_('comment'),
        on_delete=models.CASCADE,
        related_name='reactions',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('user'),
        on_delete=models.CASCADE,
    )
    reaction_type = models.CharField(
        _('reaction type'),
        max_length=10,
        choices=REACTION_CHOICES,
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('comment reaction')
        verbose_name_plural = _('comment reactions')
        # szj: 同一用户对同一评论的同一种反应只能记录一次。
        unique_together = ['comment', 'user', 'reaction_type']
        indexes = [
            models.Index(
                fields=['comment', 'reaction_type'],
                name='idx_comment_reaction',
            ),
        ]
```

【反例】外键缺少 `verbose_name`、`related_name`，布尔字段没有中文说明，后台和模板语义不清：

```python
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    is_enable = models.BooleanField(default=False)
    ...
```

问题：后台显示英文字段名，`verbose_name` 缺失影响国际化；没有 `related_name` 时反向关系只能使用默认的 `comment_set`，语义不明确且难以重构；`is_enable` 缺少说明，阅读者不知道"启用"指什么。

### 6.2 视图规范

| 编号 | 场景 | 首选做法 | 说明 |
| --- | --- | --- | --- |
| 1 | 列表 / 详情页 | `ListView`、`DetailView` | 项目已有 `IndexView`、`ArticleDetailView`，复用分页与上下文机制 |
| 2 | 表单提交 | `FormView` 及项目基类 | 项目 `djangoblog/base_views.py` 提供 `SecureFormView`、`AuthenticatedFormView`、`LoginFormView`，统一处理 CSRF、登录跳转和缓存控制 |
| 3 | 简单 JSON 接口 | `View` 或函数视图 | `CommentReactionView` 用 `View` 实现 GET/POST 并返回 `JsonResponse` |
| 4 | 权限校验 | 基类或 `method_decorator(login_required)` | 不在视图里手写 session 判断；未登录跳转由 `LOGIN_URL` 统一控制 |
| 5 | 视图函数参数 | 第一个参数命名为 `request` | Django 官方风格要求，禁止用 `req`、`r` |
| 6 | 职责划分 | 视图负责"编排"，业务逻辑放模型方法或服务函数 | `form_valid` 只做业务校验、补全关联、保存、重定向 |
| 7 | 异常与返回值 | 使用 `get_object_or_404`；JSON 接口返回明确状态码 | 项目 `CommentReactionView` 返回 401（未登录）、400（非法 reaction 类型） |
| 8 | 类视图 docstring | 说明 URL、权限、请求方法、失败处理 | 见 5.4 节 |

**`form_valid` 职责约定：** 只允许完成以下四步——(1) 校验业务条件（不满足时调用 `form.add_error()` 写入表单错误并返回 `form_invalid`，不得抛出未处理异常）；(2) 补全表单未包含的关联对象字段；(3) 保存对象；(4) 返回重定向。禁止在 `form_valid` 中渲染模板、拼接大段 HTML 或执行与本次提交无关的批量写操作。

【正例】类视图 + 基类统一权限 + `form_valid` 职责清晰：

```python
class CommentPostView(AuthenticatedFormView):
    """文章评论提交视图。

    URL: article/<article_id>/postcomment
    权限: 必须登录；CSRF 保护由基类统一添加。
    成功: 保存评论后重定向到文章详情页评论区锚点。
    """

    form_class = CommentForm
    template_name = 'blog/article_detail.html'

    def form_valid(self, form):
        """校验评论开关、补全评论关联信息并保存。"""
        article = get_object_or_404(Article, pk=self.kwargs['article_id'])
        # szj: 评论关闭时直接拒绝，避免绕过前端隐藏按钮重复提交。
        if article.comment_status == 'c':
            form.add_error(None, '该文章评论已关闭.')
            return self.form_invalid(form)

        comment = form.save(commit=False)
        comment.article = article
        comment.author = self.request.user
        comment.save()
        return redirect(f'{article.get_absolute_url()}#div-comment-{comment.pk}')
```

【反例】函数视图：没有登录校验、没有表单校验、没有异常处理、直接信任 `POST` 数据：

```python
def post_comment(request, article_id):
    article = Article.objects.get(id=article_id)
    Comment.objects.create(
        article=article,
        body=request.POST['body'],
    )
    return HttpResponse('ok')
```

问题：任何人可直接 POST 评论；`Article.objects.get` 在文章不存在时抛 500；`request.POST['body']` 缺键时抛异常；没有使用 Django 表单导致长度、审核、安全校验全部缺失。

### 6.3 URL 命名与 namespace

**要求：**

1. 每个应用的 `urls.py` 必须定义 `app_name`；根路由 `djangoblog/urls.py` 通过 `include(..., namespace=...)` 显式注册应用命名空间。
2. 视图中跳转、模型 `get_absolute_url()` 必须使用 `reverse('namespace:name', ...)`；模板中必须使用 `{% url 'namespace:name' ... %}`，禁止硬编码 URL 字符串。
3. URL name 使用小写 + 下划线，语义清晰；新增 URL 采用"资源_动作"或"资源_详情"风格，如 `article_detail`、`comment_create`；存量 `detailbyid`、`postcomment` 保持兼容，不做全项目重命名。
4. 路径参数使用 `<int:...>`、`<slug:...>` 等类型转换器，不用正则实现类型校验。
5. 各应用 `app_name` 与根路由 `namespace` 的命名应保持一致；项目存量中 `comments/urls.py` 的 `app_name = 'comments'` 与根路由 `include(..., namespace='comment')` 不一致属于历史情况，新增应用不得再混用，存量不做批量改动。

| 应用 | `app_name` | 根路由 namespace | 典型 URL name | 使用示例 |
| --- | --- | --- | --- | --- |
| blog | `blog` | `blog` | `index`、`detailbyid`、`category_detail`、`tag_detail` | `reverse('blog:detailbyid', kwargs={...})` |
| comments | `comments` | `comment` | `postcomment`、`comment_react` | `{% url 'comments:postcomment' article.pk %}` |
| accounts | `accounts` | `account` | `login`、`register`、`logout`、`forget_password` | `{% url 'account:login' %}` |
| oauth | `oauth` | `oauth` | `oauthlogin`、`bindsuccess`、`email_confirm` | `{% url 'oauth:bindsuccess' oauth_user.id %}` |

【正例】模型通过 `reverse` 生成 URL，模板通过 `{% url %}` 解析：

```python
def get_absolute_url(self):
    """返回文章详情页的相对 URL。"""
    return reverse('blog:detailbyid', kwargs={
        'article_id': self.id,
        'year': self.creation_time.year,
        'month': self.creation_time.month,
        'day': self.creation_time.day,
    })
```

```html
<form action="{% url 'comments:postcomment' article.pk %}" method="post">
  {% csrf_token %}
  ...
</form>
```

【反例】硬编码路径：路由调整或启用国际化前缀后立即失效，且无法被 Django URL 检查发现：

```python
def get_absolute_url(self):
    return f'/article/{self.creation_time.year}/{self.creation_time.month}/' \
           f'{self.creation_time.day}/{self.id}.html'
```

### 6.4 模板标签规范

| 编号 | 要求 | 说明 |
| --- | --- | --- |
| 1 | 标签 / 过滤器放在应用 `templatetags/` 目录下，模块名小写下划线 | 项目 `blog/templatetags/blog_tags.py`、`vite_tags.py`；模块内 `register = template.Library()` |
| 2 | 所有标签函数、过滤器函数必须有 docstring，说明参数、返回值与是否输出 HTML | 见 5.5 节 |
| 3 | 输出 HTML 时必须经过安全过滤，`mark_safe` 只能用于已确认安全的字符串 | 项目 `djangoblog/utils.py` 的 `sanitize_html` 使用 bleach 白名单过滤，是唯一允许的安全兜底 |
| 4 | 标签函数内避免无缓存的高频查询 | 项目 `cache_decorator`、`CacheTimeout`、`CacheKey` 可复用；查询较重的标签应加缓存 |
| 5 | 模板中 `{% load %}` 放在顶部，多个库按字母序排列 | 与 Django 官方模板风格一致 |
| 6 | 模板标签只负责展示数据 | 不在标签中修改数据库；除记录日志外不产生其他副作用，写操作放视图或模型方法 |

【正例】过滤器：docstring 完整，HTML 输出前经过白名单过滤：

```python
@register.filter()
def custom_markdown(content):
    """把 Markdown 文本渲染为可安全输出的 HTML。

    Args:
        content: 文章或评论的 Markdown 源文本。

    Returns:
        SafeString: 经 Markdown 渲染与 bleach 白名单过滤后的 HTML。
    """
    html_content = CommonMarkdown.get_markdown(content)
    safe_html = sanitize_html(html_content)
    return mark_safe(safe_html)
```

【反例】把用户输入直接标记为安全，存在存储型 XSS 风险：

```python
@register.filter()
def custom_markdown(content):
    return mark_safe(content)
```

### 6.5 迁移文件规范

| 编号 | 要求 | 说明 |
| --- | --- | --- |
| 1 | 禁止手工修改 `migrations/*.py` | 迁移文件由 Django 根据模型自动生成，手改会导致"模型状态 / 迁移状态 / 数据库结构"三者不一致 |
| 2 | 模型变更后必须生成并提交迁移文件 | `python manage.py makemigrations <app>`，迁移文件与模型修改放在同一次提交中 |
| 3 | 禁止删除已被其他组员拉取或已部署的迁移文件 | 需要回退时新增反向迁移，删除历史迁移会破坏数据库一致性 |
| 4 | 数据迁移使用 `RunPython` 并提供反向函数 | 便于回滚；数据迁移中不写业务无关的复杂逻辑 |
| 5 | 合并冲突时重新生成迁移，不手工合并迁移文件 | 冲突解决后执行 `makemigrations` 生成新迁移并检查 `migrate` 结果 |
| 6 | 迁移文件名保持 Django 自动生成格式 | 项目 `blog/migrations/` 下已有 0001—0008 号迁移文件，命名与 Django 自动生成格式一致 |

常用命令（在 `D:\DjangoBlog\src` 目录下执行）：

```powershell
python manage.py makemigrations blog comments
python manage.py migrate
python manage.py check
```

### 6.6 settings 与环境变量规范

| 编号 | 要求 | 说明 |
| --- | --- | --- |
| 1 | 敏感配置从环境变量读取，禁止真实值进入仓库 | `SECRET_KEY`、数据库密码、邮箱密码、OAuth Secret、Elasticsearch 凭据、Redis 地址等 |
| 2 | 环境变量统一使用 `DJANGO_` 前缀 + 模块 + 配置名 | 项目已有 `DJANGO_MYSQL_*`、`DJANGO_EMAIL_*`、`DJANGO_REDIS_URL`、`DJANGO_ELASTICSEARCH_HOST`，新增配置沿用 |
| 3 | 布尔型环境变量统一用 `env_to_bool` 转换 | 项目 `djangoblog/settings.py` 已提供 `env_to_bool`（仅字符串 `'True'` 视为真）；新增布尔配置统一调用，不各写一套判断 |
| 4 | 新增配置必须加分组注释和默认值说明 | 配置块前用 `# ===== 配置名 =====` 注释，敏感项不提供真实默认值 |
| 5 | 部署相关环境变量同步更新 README | 项目 README 已列出 MySQL 环境变量表，新增变量必须同步文档 |
| 6 | 模块顶层避免直接读取具体 settings 值 | 使用 `django.conf.settings` 延迟访问；需要默认值时在函数内读取，避免配置加载顺序问题 |
| 7 | 不在代码中关闭安全中间件 | 不注释 `CsrfViewMiddleware`、`SecurityMiddleware`、`XFrameOptionsMiddleware` 等安全配置 |

【正例】统一 helper + 环境变量读取 + 无真实密钥默认值：

```python
def env_to_bool(env, default):
    """把环境变量字符串转换为布尔值，未设置时返回默认值。"""
    str_val = os.environ.get(env)
    return default if str_val is None else str_val == 'True'


# twl: 数据库连接信息优先从环境变量读取，仓库中不保存真实密码。
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DJANGO_MYSQL_DATABASE') or 'djangoblog',
        'USER': os.environ.get('DJANGO_MYSQL_USER') or 'root',
        'PASSWORD': os.environ.get('DJANGO_MYSQL_PASSWORD') or '',
        'HOST': os.environ.get('DJANGO_MYSQL_HOST') or '127.0.0.1',
        'PORT': int(os.environ.get('DJANGO_MYSQL_PORT') or 3306),
        'OPTIONS': {'charset': 'utf8mb4'},
    },
}
```

【反例】把真实密钥、密码写死在配置中并提交到仓库：

```python
SECRET_KEY = 'django-insecure-xxxx'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'PASSWORD': 'root123456',
    },
}
```

### 6.7 避免 N+1 查询

| 关系类型 | 推荐方法 | 说明 |
| --- | --- | --- |
| 外键、一对一 | `select_related()` | 生成 JOIN，一次查询取回关联对象 |
| 一对多、多对多 | `prefetch_related()` | 分两次查询后在 Python 侧关联，避免逐条查询 |
| 只取部分字段 | `values()` / `values_list()` / `only()` | 谨慎使用；后续访问未加载字段会重新查库 |
| 列表页 | 分页 + 组合索引 + 缓存 | 与 6.1 节索引配合，避免全表扫描 |
| 高频相同查询 | 项目 `cache_decorator` + `CacheKey` | 缓存键必须集中定义，过期时间使用 `CacheTimeout` 常量 |

**要求：**

1. 在模板或循环中访问关联对象前，必须评估查询次数；列表、详情、侧边栏等展示型查询应使用 `select_related` / `prefetch_related`。
2. 禁止在循环体内直接访问未预加载的外键（典型 N+1）；必须逐条处理时，确认数据量很小并在注释中说明。
3. 性能优化代码必须写注释，说明优化原因与预期查询次数（见 5.6 节）。
4. 验证查询次数可在 `DEBUG=True` 下用 `django.db.connection.queries` 对比执行前后条数，确认不随数据量增长。

【正例】预加载作者与子评论作者，避免模板渲染时逐条查询：

```python
# szj: 预加载作者和子评论作者，避免模板渲染时逐条查询（N+1）。
parent_comments = Comment.objects.filter(
    article=self.object,
    parent_comment=None,
    is_enable=True,
).select_related('author').prefetch_related(
    'comment_set__author',
).order_by('-id')
```

【反例】循环内访问外键，评论越多查询次数越多：

```python
comments = Comment.objects.filter(article=article, is_enable=True)
author_names = []
for comment in comments:
    # 每条评论都会额外查询一次 author 表
    author_names.append(comment.author.nickname)
```

### 6.8 异常处理与日志规范

| 编号 | 要求 | 说明 |
| --- | --- | --- |
| 1 | 禁止裸 `except:` | 裸 `except` 会吞掉 `SystemExit`、`KeyboardInterrupt` 等异常；项目存量代码全量扫描仍存在此类问题，新增代码禁止，涉及修改时应改正 |
| 2 | 捕获具体异常 | 优先捕获 `DoesNotExist`、`ValidationError`、`ValueError` 等具体异常 |
| 3 | 不得静默吞异常 | 捕获后必须记录日志并返回明确结果，禁止 `except: pass` |
| 4 | 记录堆栈 | 异常日志使用 `logger.exception(...)` 或 `logger.error(..., exc_info=True)`，保留堆栈 |
| 5 | 日志格式化 | 使用 `%s` 占位符延迟格式化，禁止 f-string 拼接日志消息 |
| 6 | 日志分级 | 调试用 `debug`，正常业务里程碑用 `info`，可恢复异常用 `warning`，失败用 `error`，系统级故障用 `critical` |
| 7 | 多写操作事务 | 涉及多条写入的业务使用 `transaction.atomic()`，异常回滚并记录；项目 `oauth/views.py` 已使用该方式 |
| 8 | 用户信息保护 | 返回给用户的错误信息不暴露堆栈、SQL、配置路径；日志不记录密码、Token、完整手机号 |
| 9 | logger 命名 | 模块级 `logger = logging.getLogger(__name__)`，不硬编码字符串 logger 名 |

【正例】捕获具体异常、记录 warning、返回明确结果：

```python
import logging

logger = logging.getLogger(__name__)


def get_enabled_comment(comment_id):
    """获取已审核评论；不存在或未审核时返回 None。"""
    try:
        return Comment.objects.get(pk=comment_id, is_enable=True)
    except Comment.DoesNotExist:
        # szj: 评论不存在属于可预期分支，记录 warning 后按业务返回 None。
        logger.warning('comment not found or disabled: id=%s', comment_id)
        return None
```

【正例】批量写入使用事务，失败时回滚并记录异常堆栈：

```python
from django.db import transaction


def create_comments(article, comments_data):
    """批量创建评论；任一条失败时整体回滚。"""
    try:
        with transaction.atomic():
            for item in comments_data:
                Comment.objects.create(article=article, **item)
    except Exception:
        # wz: 数据校验或数据库异常时整批回滚，记录堆栈后向上抛出业务异常。
        logger.exception('failed to create comments for article id=%s', article.id)
        raise
```

【反例】裸 `except` + 静默忽略 + 日志丢失堆栈：

```python
try:
    comment = Comment.objects.get(pk=comment_id)
except:
    pass
```

```python
try:
    comment = Comment.objects.get(pk=comment_id)
except Exception as e:
    logger.error(e)  # 丢失堆栈，无法定位具体出错位置
```

---

## 7. 安全规范

本项目部署在公网可访问的环境中，包含用户注册登录、评论提交、后台管理、第三方登录等敏感功能。安全条款为**强制条款**，任何情况下不得以"课程作业"为由降低安全标准。

### 7.1 CSRF 防护

| 编号 | 要求 | 项目落点 |
| --- | --- | --- |
| 1 | 所有会修改数据的表单（POST）必须包含 `{% csrf_token %}` | 项目 `account/login.html`、`account/registration_form.html`、`comments/tags/post_comment.html` 等模板均已使用 |
| 2 | 不得注释或关闭 `CsrfViewMiddleware` | `djangoblog/settings.py` 的 `MIDDLEWARE` 中已启用，禁止删除 |
| 3 | 表单类视图统一继承项目基类，由基类添加 `csrf_protect` | `djangoblog/base_views.py` 的 `SecureFormView`、`AuthenticatedFormView`、`LoginFormView` 均已用 `method_decorator` 添加 |
| 4 | HTMX / AJAX 请求必须携带 CSRF Token | 项目评论模板的 HTMX 表单同样渲染 `{% csrf_token %}`；自定义请求从 Cookie 读取 `csrftoken` 并写入请求头 |
| 5 | 第三方回调等特殊接口如需豁免，必须验签并在注释中说明原因 | 例如微信公众号机器人回调需按平台规则验签；不得为了"方便调试"使用无验证的 `@csrf_exempt` |

【正例】表单包含 CSRF Token，提交到命名 URL：

```html
<form action="{% url 'comments:postcomment' article.pk %}" method="post">
  {% csrf_token %}
  <textarea name="body" maxlength="300"></textarea>
  <button type="submit">发表评论</button>
</form>
```

【反例】无验证豁免 CSRF，任何人都能伪造评论提交：

```python
@csrf_exempt
def comment_react(request, comment_id):
    # 未做任何签名或来源校验
    ...
```

### 7.2 XSS 输出转义

| 编号 | 要求 | 说明 |
| --- | --- | --- |
| 1 | 模板默认自动转义，禁止对用户可控内容使用 `\|safe` 或 `mark_safe` | Django 模板会自动转义 `<`、`>`、`&`、引号等字符 |
| 2 | 富文本必须先渲染再过滤，使用 `sanitize_html` 白名单 | 项目 `djangoblog/utils.py` 使用 bleach 设置标签、属性、协议白名单，是 XSS 兜底 |
| 3 | 允许 `mark_safe` 的场景仅限：管理员配置的可信内容、经 Markdown 渲染和 `sanitize_html` 过滤后的内容 | 项目中 `GLOBAL_HEADER\|safe`、`ANALYTICS_CODE\|safe` 属于后台管理员配置的可信内容 |
| 4 | JSON 接口返回数据而不是拼接 HTML | `CommentReactionView` 使用 `JsonResponse` 返回统计结果 |
| 5 | 评论内容开启审核时，未审核内容不得输出到页面 | `BlogSettings.comment_need_review` 与 `Comment.is_enable` 共同控制 |

【正例】用户评论文本经 Markdown 渲染 + 白名单过滤后再输出：

```python
def render_comment_html(body):
    """把评论 Markdown 渲染为白名单过滤后的 HTML。

    Args:
        body: 用户提交的评论 Markdown 原文。

    Returns:
        str: 可安全输出的 HTML；不允许的标签已被移除。
    """
    html_content = CommonMarkdown.get_markdown(body)
    return sanitize_html(html_content)
```

【反例】直接把用户输入标记为安全，存在存储型 XSS 风险：

```python
# 反例：用户可提交 <script>alert(1)</script>，后台打开审核页面即被攻击
return mark_safe(request.POST.get('body', ''))
```

### 7.3 ORM 防注入

| 编号 | 要求 | 说明 |
| --- | --- | --- |
| 1 | 所有数据库查询通过 Django ORM 完成 | 项目全量检索未发现 `.raw()`、`.extra()`、`connection.cursor()` 的使用，新增代码继续保持该做法 |
| 2 | 用户输入只能作为查询参数，不得拼接进 SQL、表名、字段名 | 使用 `filter(title__icontains=keyword)` 这类参数化写法 |
| 3 | 排序字段、展示字段等动态字段名必须使用白名单映射 | 例如 `ORDER_FIELDS = {'new': '-pub_time', 'hot': '-views'}`，从请求参数映射到固定字段 |
| 4 | 确需原生 SQL 时必须使用参数化查询，并注释说明原因 | `Model.objects.raw('... WHERE id = %s', [article_id])`，禁止用 `%`、`format`、f-string 拼 SQL |
| 5 | 不在日志中输出完整 SQL 参数中的敏感内容 | 查询参数可能包含手机号、邮箱等个人信息 |

【正例】使用参数化查询：

```python
keyword = request.GET.get('q', '').strip()
articles = Article.objects.filter(
    title__icontains=keyword,
    status='p',
).select_related('author')[:20]
```

【反例】把用户输入拼进 SQL，可被注入恶意语句：

```python
keyword = request.GET.get('q', '')
articles = Article.objects.raw(
    'SELECT * FROM blog_article WHERE title = "%s"' % keyword
)
```

### 7.4 敏感信息不入库、不入仓

| 编号 | 敏感项 | 正确存放方式 | 禁止做法 |
| --- | --- | --- | --- |
| 1 | `SECRET_KEY` | 部署环境变量 `DJANGO_SECRET_KEY` | 仓库中保留真实密钥；把开发密钥提交到公开仓库 |
| 2 | 数据库账号密码 | `DJANGO_MYSQL_USER` / `DJANGO_MYSQL_PASSWORD` 等环境变量 | 写死在 `settings.py`；把真实密码写入 README 或文档 |
| 3 | 邮箱授权码 / 密码 | `DJANGO_EMAIL_USER` / `DJANGO_EMAIL_PASSWORD` | 明文写进配置或测试用例 |
| 4 | OAuth、微信、Elasticsearch、Redis 凭据 | 各自环境变量，见 README 配置说明 | 提交到 Git；截图时未打码 |
| 5 | 用户密码 | Django 认证系统自动哈希存储 | 自建明文密码字段；日志打印密码 / Token |
| 6 | 本地环境文件 | 本地 `.env` 等文件加入忽略列表，不提交 | 把 `.env`、`logs/`、`uploads/`、本地数据库文件提交到仓库 |

**要求：**

1. 提交前检查 `git status` 与暂存区内容，确认没有 `.venv`、`__pycache__`、`logs/`、`uploads/`、本地数据库文件、真实凭据文件；项目 `src/.gitignore` 已有的忽略规则不得删除。
2. 数据库层面不得新增明文密码、明文密钥字段；确需存储第三方 Token 时必须说明加密或过期策略。
3. 课程报告、答辩 PPT、截图中的密码、Token、个人信息必须打码。
4. 若已误提交密钥，必须立即更换密钥，而不是仅在后续提交中删除文件（Git 历史仍可恢复）。

### 7.5 权限与越权防护

| 编号 | 场景 | 要求 |
| --- | --- | --- |
| 1 | 需要登录的操作 | 使用 `AuthenticatedFormView` 或 `login_required`；未登录返回 302 跳转登录页，不得直接执行写操作 |
| 2 | 对象级权限 | 修改 / 删除文章、评论前校验对象归属（如 `article.author == request.user`），越权时返回 404 而非 403，避免泄露资源存在性 |
| 3 | 后台管理 | 通过 Django Admin 权限体系控制；不在前台视图里用 `is_staff` 手写判断替代 Admin 权限 |
| 4 | 不信任前端 | 前端隐藏按钮只是体验优化，后端必须再次校验权限与业务状态（如评论开关） |
| 5 | 敏感操作审计 | 删除文章、批量操作等敏感操作记录日志（操作人、对象、时间） |

【正例】对象级权限校验，越权返回 404：

```python
from django.http import Http404


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    """文章编辑视图：只允许作者本人编辑自己的文章。"""

    model = Article
    fields = ['title', 'body', 'category', 'tags']

    def get_object(self, queryset=None):
        article = super().get_object(queryset)
        if article.author_id != self.request.user.id:
            # cgw: 越权时返回 404，避免暴露他人文章是否存在。
            raise Http404('article not found')
        return article
```

【反例】只在模板中隐藏按钮，后端无任何校验，可通过直接调用接口越权操作：

```python
def delete_article(request, article_id):
    Article.objects.filter(pk=article_id).delete()  # 任何登录用户都能删除任意文章
    return JsonResponse({'success': True})
```

### 7.6 安全检查表

| 编号 | 检查项 | 通过标准 |
| --- | --- | --- |
| 1 | CSRF | 所有 POST 表单含 `{% csrf_token %}`；未关闭 CSRF 中间件；豁免接口有验签说明 |
| 2 | XSS | 用户可控内容不使用 `\|safe` / `mark_safe`；富文本经过 `sanitize_html` 白名单过滤 |
| 3 | SQL 注入 | 查询全部通过 ORM 参数化完成；无字符串拼接 SQL；动态字段名走白名单 |
| 4 | 敏感信息 | 无真实密钥、密码、Token 进入代码或仓库；日志不打印敏感信息 |
| 5 | 权限 | 写操作有登录校验；对象级操作校验归属；前端隐藏不等于后端校验 |
| 6 | 文件上传 | 上传文件校验类型、大小、文件名，禁止上传可执行脚本到可访问目录 |
| 7 | 依赖安全 | 不随意升级/降级依赖；新增第三方包须在小组内说明用途并记录到 `requirements.txt` |

---

## 8. 测试规范

### 8.1 测试文件组织

| 编号 | 要求 | 说明 |
| --- | --- | --- |
| 1 | 测试文件命名为 `test_*.py`，放在被测应用目录下 | 项目已有 `blog/test_views.py`、`comments/test_comment_business_logic.py`、`accounts/test_user_business_logic.py` 等 |
| 2 | 按被测对象拆分文件，不要把所有用例堆在一个文件 | 视图、模型业务、模板标签、中间件、管理后台分别建文件 |
| 3 | 测试类继承 `django.test.TestCase`（或项目 `djangoblog/test_base.py` 中的基类） | `TestCase` 使用事务回滚，保证用例之间数据隔离 |
| 4 | 存量 `tests.py` 可保留，新增用例写入 `test_*.py` | 避免多人同时修改同一文件产生冲突 |
| 5 | 测试文件不需要被 `INSTALLED_APPS` 注册 | Django 测试运行器会自动发现 `test*.py` |

项目现有测试文件（节选）及覆盖方向：

| 测试文件 | 覆盖方向 |
| --- | --- |
| `blog/test_article_business_logic.py` | 文章业务逻辑测试（状态转换、权限与评论控制等） |
| `blog/test_views.py` | 博客视图测试 |
| `blog/test_templatetags.py` | 自定义模板标签与过滤器测试 |
| `blog/test_middleware.py` | 博客中间件测试 |
| `blog/test_context_processors.py` | 上下文处理器测试 |
| `comments/test_comment_business_logic.py` | 评论业务逻辑测试（审核、嵌套回复、表情反应等） |
| `comments/test_views.py` | 评论视图测试 |
| `accounts/test_user_business_logic.py` | 用户业务逻辑测试 |
| `djangoblog/test_plugins.py` | 插件加载与钩子测试 |
| `oauth/test_oauth_business_logic.py` | 第三方登录业务逻辑测试 |

### 8.2 测试用例命名

| 对象 | 命名规则 | 正例 | 反例 |
| --- | --- | --- | --- |
| 测试文件 | `test_<被测模块>.py` | `test_comment_business_logic.py` | `test.py`、`my_test.py` |
| 测试类 | `<被测对象>Test` | `ArticleLifecycleTest`、`CommentReviewTest` | `Test1`、`MyTests` |
| 测试方法 | `test_<行为>_<条件>` | `test_article_created_as_draft_by_default`、`test_article_draft_to_published_transition` | `test1`、`test_it`、`test_ok` |
| 测试 docstring | 一行说明验证的预期行为 | `"""开启评论审核时，新评论默认不展示。"""` | 无 docstring 或写"测试一下" |

**要求：** 一个测试方法聚焦一个行为；断言要明确（`assertEqual`、`assertFalse`、`assertRaises` 等）；不使用无断言的"冒烟测试"代替业务测试。

### 8.3 测试覆盖范围与优先级

| 优先级 | 覆盖对象 | 最低要求 |
| --- | --- | --- |
| P0（必须覆盖） | 核心业务：文章状态与发布、评论审核开关、评论开关、用户注册登录、权限控制 | 成功路径 + 失败路径都要有用例；权限相关必须覆盖未登录、非作者、无权限三种情况 |
| P1（必须覆盖） | 视图与表单：表单校验失败、非法参数、对象不存在、重复提交、评论反应切换 | 每个新增视图至少一个正常用例和一个异常用例 |
| P2（推荐覆盖） | 模板标签、上下文处理器、中间件、管理后台、插件钩子 | 新增或修改对应功能时补充用例 |
| P3（可选覆盖） | 邮件、OAuth、第三方接口 | 使用 mock 隔离外部服务，不依赖真实网络 |

**覆盖率目标（推荐）：** 使用项目依赖中的 `coverage` 统计，`blog`、`comments`、`accounts` 三个核心应用的新增代码行覆盖率建议不低于 60%；覆盖率是质量目标，不是唯一标准，关键业务分支必须显式覆盖。

### 8.4 测试运行命令

在 `D:\DjangoBlog\src` 目录下执行：

```powershell
cd D:\DjangoBlog\src

# 运行全部测试
python manage.py test

# 只运行指定应用或指定测试文件
python manage.py test blog comments accounts
python manage.py test blog.test_article_business_logic

# 统计覆盖率（coverage 已列入 requirements.txt）
coverage run manage.py test
coverage report -m
```

> 运行测试前需保证数据库配置可用（按 README 设置 `DJANGO_MYSQL_*` 环境变量）；Django 测试使用独立的测试数据库，不会污染开发库。邮件、OAuth 等外部服务相关测试必须使用 mock，不得在测试中发送真实邮件。

### 8.5 测试代码风格

| 编号 | 要求 |
| --- | --- |
| 1 | 测试代码同样遵守第 3、4、5 章：命名、4 空格缩进、中文注释与署名 |
| 2 | 测试数据在 `setUp()` 中创建，使用 `create_user`、`objects.create` 明确字段，不依赖数据库中已有数据 |
| 3 | 用例之间不得有顺序依赖，不共享可变状态；需要多个用户时分别创建普通用户、作者、管理员 |
| 4 | 断言明确：布尔值用 `assertTrue` / `assertFalse`，对象计数用 `assertEqual`，异常用 `assertRaises` |
| 5 | 不使用 Python 内置 `assert` 语句（`python -O` 下会被移除），使用 `TestCase` 提供的断言方法 |
| 6 | 外部服务（邮件、OAuth、搜索）使用 mock 或测试替身，避免测试依赖网络和第三方账号 |

【正例】测试类、方法命名与 docstring 规范：

```python
class CommentReviewTest(TestCase):
    """评论审核业务测试。"""

    def setUp(self):
        """准备文章、作者与评论审核配置。"""
        self.author = BlogUser.objects.create_user(
            username='author', password='test-password')
        self.article = Article.objects.create(
            title='测试文章', body='正文', author=self.author,
            category=Category.objects.create(name='测试分类'),
        )

    def test_comment_pending_when_review_enabled(self):
        """开启评论审核时，新评论默认不展示。"""
        BlogSettings.objects.create(comment_need_review=True)
        ...
        self.assertFalse(comment.is_enable)
```

【反例】命名无意义、使用内置断言、无 docstring：

```python
def test1(self):
    a = Article.objects.create(title='x', body='y')
    assert a.status == 'd'
```

---

## 9. Git 提交规范

### 9.1 分支命名

| 分支类型 | 命名规则 | 示例 | 说明 |
| --- | --- | --- | --- |
| 个人开发分支 | `<姓名缩写>_branch` | `szj_branch`、`twl_branch`、`cgw_branch` | 每人从最新主干拉出，用于日常开发；缩写取自 1.2 节表 |
| 主干分支 | 沿用仓库现有主干名（`main` 或 `master`） | 以仓库实际配置为准 | 禁止直接向主干提交未经评审的代码 |
| 临时实验分支 | `<姓名缩写>_exp_<主题>` | `hd_exp_comment_cache` | 探索性改动使用，实验结束后删除，不合并到主干 |

**要求：**

1. 分支名全小写，只用字母、数字和下划线，不使用中文、空格和 `#`；
2. 一个分支围绕一个任务，完成评审合并后删除，不在同一分支长期堆积无关改动；
3. 合并前先同步主干并解决冲突，冲突解决后必须重新运行相关测试；
4. 不强制推送（`git push --force`）他人分支和主干分支。

流程示例（组员在各自分支执行）：

```powershell
cd D:\DjangoBlog
git switch -c szj_branch
git add src/comments/models.py src/comments/test_comment_business_logic.py
git commit -m "feat(comments): 新增评论表情反应统计接口"
git push -u origin szj_branch
```

### 9.2 commit message 约定

**格式：** `<类型>(<范围>): <中文说明>`

| 类型 | 含义 | 使用场景 |
| --- | --- | --- |
| `feat` | 新功能 | 新增视图、模型字段、接口、模板标签等 |
| `fix` | 缺陷修复 | 修复功能错误、空指针、状态判断错误等 |
| `docs` | 文档变更 | README、设计文档、本规范等 |
| `refactor` | 重构 | 不改变外部行为的代码结构调整、性能优化 |
| `test` | 测试 | 新增或修改测试用例、测试配置 |

**要求：**

1. 类型必须使用上表中的小写英文前缀；范围使用应用名或模块名（如 `blog`、`comments`、`settings`、`doc`）；
2. 说明使用中文，动词开头，简明描述"做了什么"，一般不超过 50 个字符；
3. 一次提交只做一件事：不把格式化、改名、功能修复、文档更新混在同一次提交中；
4. 正文（可选）说明"为什么改"和影响范围；涉及数据库迁移、接口变更必须写明；
5. 不使用 `update`、`fix bug`、`修改一下`、`提交` 等无信息量的说明。

| 正例 | 反例 |
| --- | --- |
| `feat(blog): 新增文章默认排序索引` | `update` |
| `fix(comments): 修复审核关闭时新评论不可见` | `修复bug` |
| `docs(doc): 补充 Python 编码规范文档` | `add doc` |
| `refactor(blog): 抽取文章详情查询的预加载逻辑` | `重构代码` |
| `test(comments): 补充评论审核业务测试` | `test` |

> 以上为格式示例，不代表仓库历史提交记录。

### 9.3 提交内容与提交前检查

| 编号 | 要求 | 说明 |
| --- | --- | --- |
| 1 | 提交前运行 `python manage.py check` 与相关测试 | 确保 Django 配置、模型与测试通过 |
| 2 | 模型变更与迁移文件必须在同一次提交中 | 避免他人拉取后无法运行 `migrate` |
| 3 | 不提交 `.venv`、`__pycache__`、`*.pyc`、`logs/`、`uploads/`、本地数据库文件 | 项目 `src/.gitignore` 已覆盖的规则不得删除或绕过 |
| 4 | 不提交真实密钥、密码、Token 与个人隐私数据 | 见 7.4 节 |
| 5 | 不提交被注释掉的旧代码、调试 `print`、临时测试文件 | 用 Git 历史或分支保存临时内容 |
| 6 | 提交粒度适中：一个功能点或一个缺陷一次提交 | 便于评审、回溯与回滚 |

### 9.4 评审与合并流程

| 步骤 | 动作 | 负责人 |
| --- | --- | --- |
| 1 | 在个人分支完成任务并自查（第 10.7 节清单） | 代码作者 |
| 2 | 运行 `python manage.py check` 与相关测试，确认全部通过 | 代码作者 |
| 3 | 发起合并请求或在小组内发出评审说明（改动范围、验证方式） | 代码作者 |
| 4 | 至少 1 名其他组员评审：检查命名、注释署名、Django 专项、安全条款 | 评审人 |
| 5 | 按评审意见修改并重新自测 | 代码作者 |
| 6 | 合并到主干，删除已完成分支，同步更新文档 | 代码作者 / 文档负责人 |

---

## 10. 工具与检查清单

### 10.1 工具准备

本项目使用三个轻量工具辅助检查：`pycodestyle`（PEP 8 格式）、`pylint`（静态检查）、`radon`（复杂度与可维护性）。三者均未写入 `src/requirements.txt`，属于开发辅助工具，需在本地 Python 环境安装：

```powershell
cd D:\DjangoBlog
python -m pip install radon pylint pycodestyle

# 确认工具可用及版本
python -m radon --version
python -m pylint --version
python -m pycodestyle --version
```

版本记录：本文档编写时在 `D:\DjangoBlog` 目录下实际执行过 10.2—10.4 节的格式检查、静态检查与复杂度命令，环境为 Python 3.14.7、radon 6.0.1、pylint 4.1.3、pycodestyle 2.15.0。10.5 节的 `manage.py` 系统检查与测试命令来自项目 README，需在数据库配置可用后执行；不同组员环境的工具版本可能不同，以实际输出为准。

### 10.2 pycodestyle：PEP 8 格式检查

```powershell
cd D:\DjangoBlog

# 全量扫描：排除迁移文件、虚拟环境、前端依赖，输出按规则汇总统计
python -m pycodestyle --max-line-length=120 --exclude=migrations,.venv,node_modules --statistics src

# 提交前只检查本次修改的文件（将文件列表替换为实际改动文件）
python -m pycodestyle --max-line-length=120 src\comments\views.py src\comments\models.py
```

**说明与阈值：**

1. 行宽参数必须与第 4.1 节一致，固定使用 `--max-line-length=120`；排除项必须包含 `migrations`（自动生成）、`.venv`、`node_modules`，避免统计失真。
2. 达标线：**本次新增或修改的文件 0 告警**；全量扫描结果作为存量基线，不作为个人退回依据，但不得使告警总数增加。
3. 存量基线：编写本文档时全量扫描仍检出历史遗留问题，主要包括 `E501`（超长行 14 处，最长 126 字符）、`W293`（空白行含空格 115 处）、`W291`（行尾空白 10 处）、`E722`（裸 except 7 处）、`E302`（函数/类之间空行不足 9 处）等。这些属于二次开发前的存量代码，按 2.5 节原则逐步整改，新增代码不得再引入同类问题。
4. 常见问题处理：`E501` 用括号换行；`W291` / `W293` 删除多余空白；`E722` 捕获具体异常（见 6.8 节）；`W292` 在文件末尾补一个换行。

### 10.3 pylint：静态检查

```powershell
cd D:\DjangoBlog

# 检查两个核心业务应用（提交前可替换为本次修改的应用）
python -m pylint --max-line-length=120 --disable=E1101,R0903 src\blog src\comments
```

**说明与阈值：**

1. `E1101`（no-member）在未安装 `pylint-django` 插件时会把 Django 模型的 `objects` 等动态属性误报为错误，因此命令中统一禁用；如组员环境已安装 `pylint-django`，可改为 `--load-plugins=pylint_django` 并去掉该禁用项。
2. `R0903`（too-few-public-methods）对 Django 配置类、常量类、简单视图属于误报，统一禁用。
3. 达标线：**本次新增或修改的模块评分不低于 8.0/10，且不新增 `E` 级问题**；存量模块以"评分不劣化"为原则。
4. 存量基线：编写本文档时对 `src\blog` 与 `src\comments` 执行上述命令，评分为 8.35/10。该分数仅作为存量基线参考，不代表规范达标结论；评审时应重点关注本次改动新增的告警。
5. 对 `unused-import`、`bare-except`、`broad-exception-caught`、`duplicate-code` 等提示必须逐条确认：能修复的修复，确认属于误报的需在评审记录中说明。

### 10.4 radon：复杂度与可维护性检查

```powershell
cd D:\DjangoBlog

# 圈复杂度：-s 显示每个代码块的复杂度，-a 输出平均值
python -m radon cc -s -a --exclude .venv,node_modules src

# 可维护性指数（MI）
python -m radon mi -s --exclude .venv,node_modules src
```

**说明与阈值：**

1. `radon cc` 等级含义：A（1—5）、B（6—10）为可接受；C（11—20）需要关注；D 及以上（21 以上）必须拆分或重构。
2. 达标线：**新增或修改的函数/方法复杂度不超过 10（A/B 级）**；复杂度处于 C 级（11—20）需在评审中说明理由，D 级及以上必须拆分。
3. `radon mi` 达标线：新增模块 MI 应达到 A 级；存量模块不低于 B 级；C 级模块列入下阶段重构清单。
4. 存量基线：编写本文档时 `radon cc` 共分析 1061 个代码块，平均复杂度为 A 级（2.17）；`radon mi` 对 152 个 Python 文件的结果为 A 级 150 个、B 级 1 个、C 级 1 个。新增代码不得低于该基线水平。

### 10.5 Django 系统检查与测试

```powershell
cd D:\DjangoBlog\src

# Django 配置与模型系统检查
python manage.py check

# 运行测试（详见第 8 章）
python manage.py test
```

**阈值：** `python manage.py check` 必须无 `ERROR`（`WARNING` 需记录并评估）；`python manage.py test` 必须全部通过，核心业务用例不得跳过或删除。

### 10.6 工具检查项汇总

| 检查项 | 工具 / 命令 | 达标线 | 执行时机 |
| --- | --- | --- | --- |
| PEP 8 格式 | `pycodestyle --max-line-length=120 ...` | 新增/修改文件 0 告警；全量不新增 | 每次提交前 |
| 静态检查 | `pylint --max-line-length=120 --disable=E1101,R0903 ...` | 新增/修改模块 ≥ 8.0/10，无新增 E 级问题 | 每个功能完成后 |
| 圈复杂度 | `radon cc -s -a ...` | 新增函数 ≤ 10；C 级需说明，D 级必须拆分 | 每个功能完成后 |
| 可维护性 | `radon mi -s ...` | 新增模块 A 级，存量不低于 B 级 | 每周复查 |
| Django 检查 | `python manage.py check` | 0 errors | 每次提交前 |
| 单元测试 | `python manage.py test` | 全部通过 | 每次提交前 |

### 10.7 提交前自查清单

| 序号 | 检查项 | 依据章节 | 完成 |
| --- | --- | --- | --- |
| 1 | 改动范围与任务一致，没有无关文件、临时文件的改动 | 2.5 | ☐ |
| 2 | 模块、类、函数、变量、常量命名符合规范 | 3 | ☐ |
| 3 | 使用 4 空格缩进，无 Tab；单行不超过 120 字符 | 4.1 | ☐ |
| 4 | 无行尾空白；文件末尾保留一个换行；无连续 3 个以上空行 | 4.1、4.2 | ☐ |
| 5 | import 已按标准库 / 第三方 / Django / 本项目分组，无通配符导入、无未使用导入 | 4.4 | ☐ |
| 6 | 文件有模块 docstring，说明职责、主要内容和依赖 | 5.3 | ☐ |
| 7 | 新增/修改的类有类 docstring，模型说明关联关系、视图说明权限与失败处理 | 5.4 | ☐ |
| 8 | 公开函数/方法、视图钩子、模板标签有 docstring，复杂函数含 Args/Returns/Raises | 5.5 | ☐ |
| 9 | 复杂查询、权限判断、缓存、异常、安全逻辑有注释；个人注释以 `# <缩写>: ` 打头 | 5.2、5.6 | ☐ |
| 10 | 注释为中文、与代码一致；无被注释掉的废弃代码和调试输出 | 5.1、5.8 | ☐ |
| 11 | 模型字段有 `verbose_name`；新增外键有 `related_name`；`Meta` 与索引符合要求 | 6.1 | ☐ |
| 12 | 视图使用类视图或项目基类；`form_valid` 职责清晰；权限校验完整 | 6.2、7.5 | ☐ |
| 13 | URL 使用 `reverse()` / `{% url %}`，无硬编码路径 | 6.3 | ☐ |
| 14 | 迁移文件由 `makemigrations` 生成，未手工修改 | 6.5 | ☐ |
| 15 | 敏感配置使用环境变量，代码与仓库中无真实密钥、密码 | 6.6、7.4 | ☐ |
| 16 | 列表/详情查询已避免 N+1，必要处使用 `select_related` / `prefetch_related` | 6.7 | ☐ |
| 17 | 无裸 `except`；异常有日志且保留堆栈；日志使用 `%s` 占位符 | 6.8 | ☐ |
| 18 | CSRF、XSS、SQL 注入、越权、敏感信息五项安全要求已核对 | 7.6 | ☐ |
| 19 | 新增/修改行为有测试用例，命名符合 `test_<行为>_<条件>`，测试全部通过 | 8 | ☐ |
| 20 | `pycodestyle`、`pylint`、`radon`、`python manage.py check` 已执行并达标 | 10.6 | ☐ |
| 21 | commit message 使用 `feat/fix/docs/refactor/test` 前缀并附中文说明 | 9.2 | ☐ |
| 22 | 未提交 `.venv`、`logs/`、`uploads/`、本地数据库、真实凭据等敏感或临时文件 | 9.3 | ☐ |

---

## 11. 参考

| 序号 | 参考资料 | 链接 | 在本规范中的用途 |
| --- | --- | --- | --- |
| 1 | PEP 8 — Style Guide for Python Code（官方） | https://peps.python.org/pep-0008/ | 命名、缩进、空行、import、行宽等基础风格依据 |
| 2 | PEP 8 中文翻译（社区维护） | https://pep8.cn/ | 中文阅读与组内培训；如链接无法访问，以英文原文为准 |
| 3 | PEP 257 — Docstring Conventions（官方） | https://peps.python.org/pep-0257/ | 模块、类、函数 docstring 的结构与写法依据 |
| 4 | Django 5.2 Coding style（官方英文） | https://docs.djangoproject.com/en/5.2/internals/contributing/writing-code/coding-style/ | Django 项目的视图、模型、模板、import 风格依据 |
| 5 | Django 5.2 编码风格（官方中文） | https://docs.djangoproject.com/zh-hans/5.2/internals/contributing/writing-code/coding-style/ | 中文阅读版本 |
| 6 | Django 5.2 官方文档（模型、查询、测试、安全等主题） | https://docs.djangoproject.com/en/5.2/ | 第 6、7、8 章条款的框架依据 |
| 7 | 项目 README.md | `README.md` | 项目环境、运行方式、环境变量与常用检查命令 |
| 8 | 项目依赖清单 | `src/requirements.txt` | Python / Django / coverage 等版本与工具依赖依据 |
| 9 | 项目源码 | `src/` 目录 | 第 3—8 章中所有项目示例与现状说明的来源 |
| 10 | 小组《第五周作业：数据模型与 Django 架构设计》 | `doc/第五周作业_数据模型与Django架构设计.md` | 数据模型与架构背景，与本规范配套使用 |

**说明：**

1. 本规范与 PEP 8 的差异以本规范为准，主要是行宽上限取 120 字符（PEP 8 建议 79 字符）、import 分组中单独划分 Django 组（便于本项目维护），差异原因已在第 4 章说明；
2. 引用链接均为公开官方文档或社区维护文档，若链接失效，可在组内说明后替换为等价资料；
3. 本规范自 2026-11-09 起在小组内执行，后续如有修订，由文档负责人更新本文档并记录版本修订表。

