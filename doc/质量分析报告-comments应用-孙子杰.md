# DjangoBlog 项目代码质量分析报告

## —— 以 comments（评论）应用为例

| 项目 | 内容 |
| --- | --- |
| 课程 | 软件工程（大作业第 7-8 周） |
| 项目名称 | 6班17组 DjangoBlog 博客系统 |
| 小组 | 软件6班 17组 |
| 分析人 | 孙子杰（组长） |
| 学号 | 2415304650 |
| 分析对象 | `src/comments`（评论应用） |
| 项目仓库 | https://github.com/Sun121366/6-17-.git |
| 分析日期 | 2026-11-09 |
| 文档版本 | v1.0 |
| 相关文档 | 《第7-8周组会纪要与工作计划》《Python 编码规范-第6班17组》 |

---

## 一、小组阶段工作总结与新两周计划（概要）

> 完整内容见《第7-8周组会纪要与工作计划》。

### 1.1 前一阶段（第 5-6 周）工作回顾

- **文档成果**：完成数据模型设计与中文注释、软件系统数据模型设计说明书（docx + pdf）、软件界面设计说明书、用例图/顺序图/架构流程图，以及第 5 周数据模型作业文档。
- **代码成果**：完成文章、分类、标签、评论、用户、OAuth、插件等模块的功能实现；前端完成 Tailwind 组件化改造（侧边栏热门文章金银铜配色、彩色标签云、明暗主题）。
- **运行验证**：本地 MySQL 完成迁移，站点在 `http://127.0.0.1:8000` 可运行，首页/文章详情/分类/标签/归档/搜索/登录注册/后台登录等页面均返回 200。
- **协作方式**：成员按 `<姓名缩写>_branch` 分支开发，组长负责合并到 `master`。

### 1.2 第 7-8 周任务分解

| 序号 | 任务 | 负责人 | 产出 |
| --- | --- | --- | --- |
| ① | 每人认领一个不重复的 app 进行代码精读与注释 | 全体成员（app 不可重复） | 带注释源码 |
| ② | 使用工具做代码质量评估与改进 | 全体成员 | 质量评估数据与改进代码 |
| ③ | 学习并总结 Python 编码规范 | 小组共同 | 小组编码规范文档 |
| ④ | 制定下一步系统优化计划 | 组长汇总 | 本报告第十章 |
| ⑤ | 质量分析报告 + 规范文档 + 带注释源码提交 `master` | 组长 | 仓库提交 |

**本次个人分工**：孙子杰负责 `comments`（评论）应用的精读、注释、质量分析、改进与报告撰写（app 认领表见组会纪要文档）。

---

## 二、分析对象与范围

### 2.1 为什么选择 comments 应用

- 评论是博客系统最核心的互动功能，业务链路完整：**提交 → 审核 → 展示 → 嵌套回复 → Emoji 反应 → 邮件通知**；
- 代码量适中（基线 1710 行、13 个 Python 文件），适合逐行精读；
- 兼具 **模型 / 视图 / 表单 / 模板标签 / 后台管理 / 工具函数** 六类典型文件，问题样本覆盖面广；
- 该模块此前存在明显的性能与健壮性隐患（N+1 查询、异常直接抛出等），改进空间明确。

### 2.2 分析范围

| 类别 | 文件 |
| --- | --- |
| 模型层 | `models.py`（Comment、CommentReaction） |
| 视图层 | `views.py`（CommentPostView、CommentReactionView） |
| 表单层 | `forms.py`（CommentForm） |
| 路由 | `urls.py` |
| 后台管理 | `admin.py` |
| 工具函数 | `utils.py`（评论邮件通知） |
| 模板标签 | `templatetags/comments_tags.py` |
| 应用配置/入口 | `apps.py`、`__init__.py`、`templatetags/__init__.py` |
| 测试 | `tests.py`、`test_views.py`、`test_comment_business_logic.py` |
| 排除 | `migrations/`（Django 自动生成，不参与人工质量评估） |

### 2.3 技术环境

- Python 3.14.7、Django 5.2.17、MySQL 8（数据库 `djangoblog`）
- 分析工具：`radon 6.0.1`、`pylint 4.1.3 + pylint-django`、`pycodestyle 2.15.0`、`coverage 7.16.0`
- 测试命令：`python manage.py test comments --noinput`

> **工具选型说明**：任务要求中提到的 SonarQube 插件、Gitee 平台质量分析工具在本机/本项目环境下不可用，因此采用功能等价的**本地开源工具链**（radon 计算复杂度与可维护指数、pylint 做静态缺陷检查、pycodestyle 做 PEP 8 合规检查），并在报告中完整给出命令与原始结论，保证结果可复现。

---

## 三、分析工具与执行命令

| 工具 | 分析内容 | 命令 |
| --- | --- | --- |
| pylint | 静态缺陷、命名、文档字符串、导入、异常等 | `python -m pylint comments --load-plugins=pylint_django --django-settings-module=djangoblog.settings --ignore=migrations --score=y` |
| radon cc | 圈复杂度（Cyclomatic Complexity） | `python -m radon cc comments -s -a` |
| radon mi | 可维护性指数（Maintainability Index） | `python -m radon mi comments -s` |
| radon raw | 代码行、注释率统计 | `python -m radon raw comments -s` |
| pycodestyle | PEP 8 风格合规 | `python -m pycodestyle comments --max-line-length=120 --statistics --exclude=migrations` |
| Django check | 框架级配置检查 | `python manage.py check` |
| Django test | 单元/集成测试 | `python manage.py test comments --noinput` |

---

## 四、基线质量指标（改进前）

### 4.1 总体指标

| 指标 | 改进前 | 说明 |
| --- | --- | --- |
| 代码规模（radon raw） | LOC 1710 / LLOC 700 / SLOC 1235 | 不含 migrations |
| 注释率 | C % L = 5%，C+M % L = 8% | 单行注释与多行文档字符串占比偏低 |
| 圈复杂度 | 平均 **A（1.57）**，共 90 个代码块 | 复杂度本身健康，无 D/E/F 级块 |
| 可维护性指数 MI | 全部 **A**，最低 `admin.py` 48.24、`test_comment_business_logic.py` 49.52、`utils.py` 62.74 | A 级但仍偏低 |
| pylint 评分 | **8.72 / 10** | 共 **72 条**告警 |
| pycodestyle | **2 处**（W291 行尾空格，`utils.py:26`、`utils.py:28`） | — |
| 测试 | **36 个用例全部通过**（约 60 秒） | 未覆盖 Emoji 反应接口 |

### 4.2 pylint 问题分布（改进前，共 72 条）

| 问题码 | 含义 | 数量 | 严重级别 |
| --- | --- | --- | --- |
| C0415 | import-outside-toplevel（函数内导入） | 16 | 中 |
| C0116 | missing-function-docstring（函数/方法缺文档字符串） | 12 | 中 |
| C0209 | consider-using-f-string（应使用 f-string） | 9 | 低 |
| C0114 | missing-module-docstring（模块缺文档字符串） | 8 | 中 |
| C0115 | missing-class-docstring（类缺文档字符串） | 5 | 中 |
| W1406 | unnecessary-dunder-call | 4 | 低 |
| W5150 | format-html-interpolation（format_html 应参数化插值） | 4 | 中（安全相关） |
| W0612 | unused-variable（未使用变量） | 3 | 低 |
| C0301 | line-too-long（行长超过 100） | 3 | 低 |
| W0613 | unused-argument（未使用参数） | 2 | 低 |
| W0611 | unused-import（未使用导入） | 2 | 低 |
| C0303 | trailing-whitespace（行尾空格） | 1 | 低 |
| W0718 | broad-exception-caught（捕获过宽泛异常） | 1 | 中 |
| W0614 | unused-wildcard-import | 1 | 中 |
| W0401 | wildcard-import（通配符导入） | 1 | 中 |

**问题结构结论**：基线问题以**文档字符串缺失（25 条）**和**函数内导入（16 条）**为主，其次是格式化写法与安全相关的 `format_html` 插值问题；说明代码"能跑"但**可读性、可维护性与规范性不足**。

---

## 五、问题清单（按文件定位）

| 编号 | 文件:行 | 问题码 | 问题描述 | 级别 | 改进措施 |
| --- | --- | --- | --- | --- | --- |
| 1 | `models.py:78` | C0415 | `Count` 在方法内导入 | 中 | 提升到模块顶部 |
| 2 | `models.py:57` | C0301 | 索引定义行超长（106 字符） | 低 | 拆行重排 |
| 3 | `views.py:51` | C0415 | `get_blog_setting` 在方法内导入 | 中 | 提升到模块顶部 |
| 4 | `views.py:64` | C0209 | 使用 `%` 拼接重定向 URL | 低 | 改 f-string |
| 5 | `views.py:48` | W0718/HIGH | `form_valid` 中 `raise ValidationError` 导致 **500** | **高** | 改为返回 403 响应 |
| 6 | `views.py:62` | — | `comment.save(True)` 位置参数语义不清 | 中 | 显式 `force_insert=True` |
| 7 | `views.py:58` | — | `Comment.objects.get(pk=...)` 父评论不存在时抛 500 | 中 | 改 `get_object_or_404` |
| 8 | `models.py:65-109` | 性能 | `get_reactions_summary` **N+1 查询**（1 + 2N 次） | **高** | 批量查询 + 内存分组 |
| 9 | `utils.py:26,28` | W291/C0303 | 行尾空格 | 低 | 清理空白 |
| 10 | `utils.py:21,26` | C0301 | 超长行 | 低 | 拆分字符串 |
| 11 | `utils.py:37` | W0718 | 裸 `except Exception` 且 `logger.error(e)` 无堆栈 | 中 | `logger.exception` 记录堆栈 |
| 12 | `utils.py:11` | C0116 | 缺函数文档字符串 | 中 | 补充 docstring |
| 13 | `admin.py:9,13,21,37,44,54,62,68` | C0114/5/6、W0613 | 模块/类/方法缺 docstring；action 未用参数 | 中 | 全量补齐 + `del` 显式丢弃 |
| 14 | `admin.py:39-72` | C0209/W5150/W1406 | `u''` 前缀、`%` 拼接 `format_html` | 中（安全） | 改参数化 `format_html` |
| 15 | `tests.py:7` | W0401/W0614 | 通配符导入 `from ... import *` | 中 | 改为显式导入 |
| 16 | `tests.py:17,108` | C0415 | 函数内导入 | 中 | 提升到模块顶部 |
| 17 | `tests.py:1,13,27,33` | C0114/5/6 | 缺模块/类/方法 docstring | 中 | 补齐 |
| 18 | `test_views.py:16-19,152-155,215-218` | C0415 | `setUp` 内 12 处导入 | 中 | 提升到模块顶部 |
| 19 | `test_views.py:9,125,137` | W0611/W0612 | 未使用导入与变量 | 低 | 清理 |
| 20 | `test_comment_business_logic.py:5,670,677` | W0611/W0612 | 未使用 `Client` 导入与 `reply_id` 变量 | 低 | 清理 |
| 21 | 全模块 | 覆盖率 | Emoji 反应接口**无任何测试** | **高** | 新增 6 个反应接口测试 |
| 22 | 全模块 | 注释率 | 模块级/函数级注释缺失（25 处 docstring 缺失） | 中 | 三层注释全覆盖 |

---

## 六、重点缺陷分析与改进

### 6.1 【高】`Comment.get_reactions_summary` 的 N+1 查询

**问题代码（改进前）**：

```python
reactions = CommentReaction.objects.filter(comment=self).values('reaction_type').annotate(count=Count('id'))
for reaction in reactions:
    emoji = reaction['reaction_type']
    reaction_users = CommentReaction.objects.filter(comment=self, reaction_type=emoji).select_related('user')[:10]
    user_names = [r.user.nickname or r.user.username for r in reaction_users]
    result[emoji] = {'count': reaction['count'], 'has_reacted': False, 'users': user_names}
    if user and user.is_authenticated:
        result[emoji]['has_reacted'] = CommentReaction.objects.filter(comment=self, user=user, reaction_type=emoji).exists()
```

**问题分析**：假设一条评论上有 N 种 Emoji 反应，则查询次数为 `1（聚合）+ N（用户列表）+ N（是否已点赞）= 1 + 2N`。本项目共定义 8 种 Emoji，即每次渲染最多 **17 次数据库查询**；评论列表页每条评论渲染一次，页面查询数会成倍放大。

**改进后代码**：

```python
reaction_counts = (
    CommentReaction.objects.filter(comment=self)
    .values('reaction_type').annotate(count=Count('id'))
)
if not reaction_counts:
    return {}

users_by_reaction = defaultdict(list)
for reaction in (CommentReaction.objects.filter(comment=self)
                 .select_related('user').order_by('id')):
    user_names = users_by_reaction[reaction.reaction_type]
    if len(user_names) < MAX_REACTION_USERS:
        user_names.append(reaction.user.nickname or reaction.user.username)

reacted_types = set()
if user is not None and getattr(user, 'is_authenticated', False):
    reacted_types = set(
        CommentReaction.objects.filter(comment=self, user=user)
        .values_list('reaction_type', flat=True)
    )
```

**改进效果**：查询次数从 `1 + 2N` 降为**固定 1～3 次**：

| 场景 | 改进前 | 改进后 |
| --- | --- | --- |
| 该评论无任何反应 | 1 次 | 1 次 |
| 有反应、未登录 | 1 + 2N 次（N=8 时 17 次） | 2 次 |
| 有反应、已登录 | 1 + 2N 次（N=8 时 17 次） | 3 次 |

返回结构（`count` / `has_reacted` / `users`）与旧实现保持一致，前端无需改动；并新增 6 个接口测试防止回归。

### 6.2 【高】文章关闭评论时抛出 `ValidationError` 导致 500

**问题代码**：

```python
if article.comment_status == 'c' or article.status == 'c':
    raise ValidationError("该文章评论已关闭.")
```

**问题分析**：`ValidationError` 是**表单/模型校验**异常，在视图中直接抛出不会被 Django 转换为 400，而是当作未捕获异常返回 **500**。对用户表现为"服务器错误"，对运维表现为无意义的错误日志，且前端拿不到任何可读提示。

**改进**：

```python
if article.comment_status == 'c' or article.status == 'c':
    return HttpResponseForbidden('该文章评论已关闭。')
```

**改进效果**：返回语义明确的 **403**，避免误报 500；同时把"文章状态/评论开关"的业务规则写入注释，便于后续维护。

### 6.3 【中】`comment.save(True)` 位置参数语义不清

**问题**：`Model.save()` 的第一个位置参数是 `force_insert`，`save(True)` 虽然能运行，但读者无法从字面判断含义，且一旦 Django 调整签名会静默出错。

**改进**：改为 `comment.save(force_insert=True)`；同时把 `form.save(False)` 改为语义更清晰的 `form.save(commit=False)`。

### 6.4 【中】邮件工具宽泛异常与日志缺堆栈

**问题代码**：

```python
except Exception as e:
    logger.error(e)
```

**问题分析**：捕获过宽泛（pylint W0718）且只打印异常字符串，丢失堆栈；两个 `send_email` 调用只有一个被 try 包裹，第一封邮件异常会中断整个评论提交流程。

**改进**：把两封邮件都纳入 try 保护，失败时 `logger.exception(...)` 记录完整堆栈；邮件属于外部依赖，失败不影响已保存的评论。

### 6.5 【中】注释率与文档字符串严重缺失

基线 25 处 docstring 缺失、注释率仅 5%。按任务要求，本次为 `comments` 应用补齐**三层注释**：

1. **模块级注释**：每个文件顶部用 `# szj:` 说明模块职责与精读要点，并配模块 docstring；
2. **类/函数/方法级**：所有 22 个类、79 个函数/方法 100% 补中文 docstring（含参数、返回值说明）；
3. **核心代码块/关键行**：业务规则（评论审核、嵌套回复、反应切换）、性能优化点、异常处理等关键位置逐段注释。

个人注释统一以姓名缩写打头：`# szj: ...`（孙子杰，szj）。

### 6.6 【中】安全类编码问题

- `admin.py` 使用 `%` 手工拼接 HTML 并放入 `format_html`（W5150），存在转义风险 → 改为**参数化 `format_html`**，由 Django 自动转义；
- 测试文件通配符导入 `from ... import *`（W0401）会污染命名空间、掩盖未使用导入 → 改为显式导入。

---

## 七、改进实施清单与复测结果

### 7.1 代码变更清单

| 文件 | 变更类型 | 主要改动 |
| --- | --- | --- |
| `models.py` | 重构 + 注释 | N+1 优化；模块级导入；Meta 重排；100% docstring；`# szj:` 块注释 |
| `views.py` | 修复 + 注释 | 500→403；`force_insert`；`get_object_or_404`；模块级导入；f-string；frozenset 常量 |
| `utils.py` | 修复 + 注释 | 行尾空格/超长行；两封邮件统一异常保护；`logger.exception` |
| `admin.py` | 重构 + 注释 | 抽取 `_admin_change_link`；参数化 `format_html`；补齐 docstring；去掉 `u''` |
| `forms.py` `apps.py` `urls.py` `__init__.py` `templatetags/*` | 注释 | 模块/类/函数 docstring；中文 verbose_name；块级说明 |
| `templatetags/comments_tags.py` | 性能 + 注释 | `parse_commenttree` 由递归查询改为"一次查询 + 内存建树" |
| `tests.py` `test_views.py` `test_comment_business_logic.py` | 清理 + 增测 | 显式导入、去未使用变量、补 docstring；**新增 6 个反应接口测试** |

### 7.2 复测结果对比

| 指标 | 改进前 | 改进后 | 变化 |
| --- | --- | --- | --- |
| pylint 评分 | 8.72 / 10 | **10.00 / 10** | ↑ 1.28 |
| pylint 告警数 | 72 条 | **0 条** | ↓ 72 |
| pycodestyle 问题 | 2 处 | **0 处** | ↓ 2 |
| 圈复杂度（平均） | A（1.57），90 块 | **A（1.53）**，102 块 | 保持 A 级 |
| 可维护性 MI（最低模块） | `admin.py` 48.24 | `admin.py` **100.00** | ↑ 51.76 |
| 可维护性 MI（`utils.py`） | 62.74 | **91.12** | ↑ 28.38 |
| 可维护性 MI（`views.py`） | 68.26 | **74.21** | ↑ 5.95 |
| 注释行 | 91 行（C % L = 5%） | **180 行（C % L = 9%）** | 注释率接近翻倍 |
| 注释+文档字符串占比 | 8% | **14%** | ↑ 6 个百分点 |
| 模块 docstring 覆盖 | 部分缺失 | **13 / 13（100%）** | 全覆盖 |
| 类 docstring 覆盖 | 5 处缺失 | **22 / 22（100%）** | 全覆盖 |
| 函数/方法 docstring 覆盖 | 12 处缺失 | **79 / 79（100%）** | 全覆盖 |
| `# szj:` 个人注释 | 0 | **98 行** | 满足命名要求 |
| 测试用例数 | 36 个 | **42 个** | ↑ 6（反应接口） |
| 测试结果 | 36/36 通过 | **42/42 通过** | 全部通过 |
| Django 系统检查 | 0 issues | **0 issues** | 无回归 |
| 反应摘要查询次数 | 1 + 2N（最多 17） | **1～3（固定）** | 与 Emoji 种类数解耦 |

### 7.3 回归验证

```
python manage.py check                          → System check identified no issues (0 silenced)
python manage.py test comments --noinput        → Ran 42 tests ... OK
python -m pylint comments ...                   → Your code has been rated at 10.00/10
python -m pycodestyle comments --max-line-length=120 → 0 处问题
python -m radon cc comments -a                  → Average complexity: A (1.53)
```

> 说明：测试环境为本地 MySQL 8 + Django 5.2.17；测试过程中日志中出现的 `CacheKeyWarning`（memcached 缓存键字符）为项目既有告警，不影响测试结果，已纳入下一步优化计划。

---

## 八、注释规范落实情况

| 层级 | 要求 | 落实方式 | 示例 |
| --- | --- | --- | --- |
| 模块级 | 说明模块功能 | 文件顶部 `# szj:` 注释 + 模块 docstring | `models.py` 顶部说明"评论与反应两张核心表" |
| 类级 | 说明职责 | 类 docstring | `CommentAdmin`："评论后台：列表展示、筛选、搜索与批量审核" |
| 函数/方法级 | 参数、返回值、行为 | 方法 docstring（含 `:param`/`:return`） | `get_reactions_summary` 注明返回结构与 user 参数含义 |
| 核心代码块/关键行 | 解释"为什么" | `# szj:` 块注释 | 业务规则 1-4、N+1 优化步骤、异常处理说明 |

个人注释标识规则：`# szj: 说明`（孙子杰）、`# twl: 说明`（唐文龙）等，与组会纪要中的缩写对照表一致；本次在 `comments` 应用内共新增 **98 行** `# szj:` 注释。

---

## 九、下一步系统优化计划

> 以下计划作为小组下一步（第 9 周及以后）系统优化的基础，与组会纪要中的"下一步系统优化计划要点"一致。

| 阶段 | 优化方向 | 具体措施 | 建议负责人 | 验收标准 |
| --- | --- | --- | --- | --- |
| 第一优先级（第 9 周） | **性能优化** | 1) 其余应用参照 comments 的 N+1 排查方法，对列表页/侧边栏查询做 `select_related`/`prefetch_related`；2) 评论树 `parse_commenttree` 已将查询降为 1 次，继续评估文章详情页整体查询数；3) 评估缓存策略（评论列表缓存键与失效时机） | 各 app 负责人 | 文章详情页查询数下降 ≥ 30%；无功能回归 |
| 第一优先级（第 9 周） | **测试覆盖提升** | 1) 以 comments 为模板补齐各 app 的视图/接口测试；2) 覆盖边界与权限场景；3) 接入 `coverage` 统计行覆盖率 | 全体成员 | comments 覆盖率 ≥ 80%，全项目关键业务全覆盖 |
| 第二优先级（第 10 周） | **编码规范落地** | 1) 按《Python 编码规范-第6班17组》统一改造；2) 全仓库执行 pylint/pycodestyle 检查，逐模块清零 C 类告警；3) 提交前自查清单制度化 | 组长 + 全体成员 | 各 app pylint ≥ 9.5，pycodestyle 0 问题 |
| 第二优先级（第 10 周） | **工程与仓库治理** | 1) 清理仓库中被跟踪的 `src/.venv`；2) 完善 `.gitignore`；3) 移除误提交的二进制压缩包；4) 修正 `readme.txt` 成员信息 | 组长 | 仓库不再跟踪虚拟环境与构建产物 |
| 第三优先级（第 11 周） | **CI 与自动化** | 1) 在 GitHub Actions 中增加 lint + test 工作流；2) 运行结果作为合并门禁 | 组长 | PR 自动跑 lint + test |
| 第三优先级（第 11 周） | **安全与配置** | 1) 敏感配置全部走环境变量；2) 关闭 DEBUG 的生产部署校验；3) 检查 CSRF/XSS/上传校验 | 全员 | 安全自查清单全部通过 |
| 持续 | **文档维护** | 各 app 注释与文档随代码同步更新；质量报告每两周复测一次 | 各 app 负责人 | 文档与代码版本一致 |

---

## 十、结论

1. **基线结论**：`comments` 应用功能完整、圈复杂度健康（平均 A 级），但存在**注释/docstring 缺失、函数内导入、格式化不规范**等可维护性问题，并存在 **1 处 N+1 性能缺陷、1 处会导致 500 的异常处理缺陷、1 处反应接口测试空白**等实际风险。
2. **改进结论**：本次共修复/优化 22 类问题，pylint 评分由 **8.72 提升至 10.00**，pycodestyle 归零，注释率接近翻倍，docstring 覆盖率达到 **100%**，并新增 6 个测试用例，**42/42 全部通过**，无功能回归。
3. **方法结论**：以"工具量化 → 定位问题 → 逐项改进 → 复测验证 → 回归测试"的闭环流程开展质量改进，方法可复制到其余应用，为小组下一步系统优化提供了可执行的模板。

---

## 附录 A：复现命令

```powershell
cd D:\DjangoBlog\src
$env:DJANGO_MYSQL_PASSWORD='root'
$env:DJANGO_SETTINGS_MODULE='djangoblog.settings'

# 静态检查
python -m pylint comments --load-plugins=pylint_django `
  --django-settings-module=djangoblog.settings --ignore=migrations --score=y
python -m pycodestyle comments --max-line-length=120 --statistics --exclude=migrations

# 复杂度与可维护性
python -m radon cc comments -s -a
python -m radon mi comments -s
python -m radon raw comments -s

# 框架检查与测试
python manage.py check
python manage.py test comments --noinput
```

## 附录 B：问题码说明（pylint）

| 代码 | 含义 |
| --- | --- |
| C0114 / C0115 / C0116 | 缺少模块 / 类 / 函数文档字符串 |
| C0415 | 在函数内部导入（import-outside-toplevel） |
| C0209 | 可用 f-string 替代的格式化 |
| C0301 / C0303 | 行过长 / 行尾空格 |
| W0611 / W0612 / W0613 | 未使用导入 / 变量 / 参数 |
| W0401 / W0614 | 通配符导入 / 通配符导入中未使用的名称 |
| W0718 | 捕获过于宽泛的异常 |
| W5150 | `format_html` 应使用参数化插值 |
| W1406 | 不必要的双下划线方法调用 |

## 附录 C：参考资料

1. PEP 8 — Style Guide for Python Code：https://peps.python.org/pep-0008/
2. Django 编码风格：https://docs.djangoproject.com/en/5.2/internals/contributing/writing-code/coding-style/
3. pylint 文档：https://pylint.readthedocs.io/
4. radon 文档：https://radon.readthedocs.io/
5. 小组文档：《Python 编码规范-第6班17组》《第7-8周组会纪要与工作计划》
