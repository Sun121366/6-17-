# 六班17组 唐文龙 DjangoBlog 博客系统作业

> **项目性质**：个人软件工程课程作业，仅用于课程学习、实践与考核，非商业用途。  
> **项目来源**：本项目基于开源项目 DjangoBlog 进行学习与二次实践，感谢原作者及开源社区的无私分享。  
> **说明**：由于个人能力有限，项目中可能存在不足或疏漏，欢迎老师和同学指正。

<!-- [TWL/唐文龙] TWL = 唐文龙，仅用于标识本人补充或修改的代码说明与功能注释。 -->
---

## 一、项目简介

本项目是一个基于 Python 和 Django 开发的个人博客系统，围绕文章发布、内容展示、用户管理、评论互动和后台管理等核心场景完成软件工程课程实践。

在原有开源项目的基础上，本项目结合课程需要进行学习和整理，并对项目结构、数据库配置、前端开发方式、插件机制和相关文档进行了补充与优化。项目采用前后端协同的开发模式：Django 负责业务逻辑、数据建模、模板渲染和后台管理，Vite 负责现代前端资源的构建与热更新。

## 二、主要功能

### 1. 文章与内容管理

- 支持文章和独立页面的创建、编辑、发布与草稿管理。
- 支持文章分类、标签、作者主页、文章归档和分页展示。
- 使用 Markdown 编辑器编写文章，支持代码语法高亮。
- 支持文章浏览量统计、侧边栏展示和文章排序。
- 提供搜索功能，默认使用 Whoosh，可通过环境变量切换 Elasticsearch。

### 2. 用户与账号管理

- 支持用户注册、登录、退出和密码找回流程。
- 支持用户名或邮箱登录。
- 提供昵称、个人资料和作者主页等扩展能力。
- 集成 OAuth 第三方登录框架，可按需配置 GitHub、Google、微博、QQ 等平台。
- 使用自定义用户模型 `accounts.BlogUser` 统一关联文章、评论等业务数据。

### 3. 评论与互动

- 支持文章评论、回复和嵌套评论展示。
- 支持评论审核配置。
- 支持 Emoji 评论反应和点赞统计。
- 评论内容支持 Markdown 渲染。

### 4. 后台与站点管理

- 使用 Django Admin 管理用户、文章、分类、标签、评论和站点配置。
- 支持站点名称、SEO、主题颜色、备案信息、页眉页脚等全局配置。
- 提供友情链接、侧边栏内容、站点地图和 RSS/Feed 等扩展功能。

### 5. 现代化前端

- 使用 Vite 进行前端构建和开发服务器管理。
- 使用 Tailwind CSS 完成响应式页面设计。
- 使用 Alpine.js 和 HTMX 提供轻量交互和局部刷新体验。
- 支持浅色/深色主题切换。
- 包含代码复制、图片灯箱、返回顶部、页面加载进度和评论组件等前端功能。

### 6. 插件与扩展

项目采用插件机制扩展博客功能，当前内置插件包括：

- `view_count`：文章浏览计数。
- `seo_optimizer`：SEO 元数据优化。
- `article_copyright`：自动添加文章版权声明。
- `article_recommendation`：文章推荐。
- `external_links`：外部链接处理。
- `image_lazy_loading`：图片懒加载与展示优化。
- `reading_time`：阅读时间估算。
- `cloudflare_cache`：Cloudflare 缓存配置扩展。

### 7. 性能与部署

- 默认使用本地内存缓存，可通过 `DJANGO_REDIS_URL` 切换到 Redis。
- 支持 Django Compressor 静态资源压缩。
- 提供 Docker、Docker Compose 和 Kubernetes 部署配置。
- 提供健康检查接口：`/health/`。
- 支持多语言设置，当前包含简体中文、繁体中文和英文。

## 三、技术栈

| 类别 | 技术/组件 | 当前项目版本或说明 |
| --- | --- | --- |
| 操作系统 | Windows 10 / Windows 11 | 推荐开发环境 |
| 编程语言 | Python | 建议 3.10 及以上，当前验证版本为 3.11.9 |
| Web 框架 | Django | 5.2.17 |
| 数据库 | MySQL | 8.0.11 及以上，当前项目使用 8.0 |
| 数据库驱动 | mysqlclient | 2.2.8 |
| 前端构建 | Vite | 6.4.3 |
| CSS | Tailwind CSS | 3.4.1 |
| 前端交互 | Alpine.js | 3.16.3 |
| 页面交互 | HTMX | 2.0.10 |
| 搜索 | Haystack + Whoosh | 默认使用 Whoosh，可配置 Elasticsearch |
| Markdown | django-mdeditor + Markdown + Pygments | 支持编辑与代码高亮 |
| 缓存 | LocalMem / Redis | 默认本地缓存，可选 Redis |
| 部署 | Docker / Docker Compose / Kubernetes | 项目内提供配置 |

## 四、目录结构

```text
6-17-/
├─ src/                        项目源码
│  ├─ accounts/               用户账号管理模块
│  ├─ blog/                   博客核心模块：文章、分类、标签、搜索等
│  ├─ comments/               评论、回复和评论反应模块
│  ├─ djangoblog/             Django 核心配置：settings.py、urls.py 等
│  ├─ deploy/                 部署相关配置
│  ├─ frontend/               Vite 前端工程：JS、CSS、组件和样式
│  ├─ locale/                 国际化与本地化翻译文件
│  ├─ logs/                   日志目录
│  ├─ oauth/                  第三方登录认证模块
│  ├─ plugins/                插件扩展目录
│  ├─ servermanager/          服务端管理相关功能
│  ├─ templates/              HTML 模板文件
│  ├─ manage.py               Django 管理入口
│  └─ requirements.txt        后端依赖清单
├─ doc/                        课程设计文档、架构图和数据模型说明
├─ readme.txt                  作业提交与验证说明
└─ README.md                   项目说明文档
```

## 五、运行环境

推荐使用以下环境：

- Windows 10 / Windows 11。
- Python 3.10 及以上，本项目验证使用 Python 3.11.9。
- MySQL 8.0.11 及以上，建议使用 `utf8mb4` 字符集。
- Node.js 18 及以上，前端使用 npm 安装依赖。
- 已安装 `pip`、`npm` 和 MySQL 命令行或图形化客户端。

## 六、本地运行步骤

### 1. 创建 MySQL 数据库

在 MySQL 中执行：

```sql
CREATE DATABASE djangoblog
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

### 2. 启动 Django 后端

打开第一个 PowerShell 终端：

```powershell
cd 'D:\软工大作业\6-17-\src'

python -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt

$env:DJANGO_MYSQL_DATABASE='djangoblog'
$env:DJANGO_MYSQL_USER='root'
$env:DJANGO_MYSQL_PASSWORD='你的MySQL密码'
$env:DJANGO_MYSQL_HOST='127.0.0.1'
$env:DJANGO_MYSQL_PORT='3306'

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

后端地址：

- 前台：http://127.0.0.1:8000/
- 后台：http://127.0.0.1:8000/admin/

### 3. 启动 Vite 前端

开发模式下，页面样式和交互资源来自 Vite，因此需要再打开第二个 PowerShell 终端：

```powershell
cd 'D:\软工大作业\6-17-\src\frontend'
npm ci
npm run dev
```

前端开发地址为 `http://127.0.0.1:5173/`。开发时请同时保持后端和前端两个终端运行，然后访问 `http://127.0.0.1:8000/`。

> 如果只启动 Django、不启动 Vite，页面可能因为缺少前端样式而出现排版异常。

### 4. 可选：生成测试数据

```powershell
cd 'D:\软工大作业\6-17-\src'
python manage.py create_testdata
```

## 七、数据库配置说明

`djangoblog/settings.py` 中的数据库配置优先读取环境变量：

| 环境变量 | 默认值 | 说明 |
| --- | --- | --- |
| `DJANGO_MYSQL_DATABASE` | `djangoblog` | 数据库名称 |
| `DJANGO_MYSQL_USER` | `root` | MySQL 用户名 |
| `DJANGO_MYSQL_PASSWORD` | `root` | MySQL 密码，正式使用时必须通过环境变量设置 |
| `DJANGO_MYSQL_HOST` | `127.0.0.1` | 数据库地址 |
| `DJANGO_MYSQL_PORT` | `3306` | 数据库端口 |

本项目不推荐把真实数据库密码直接提交到 Git 仓库。

## 八、生产构建方式

前端代码修改完成后，可以构建生产环境静态资源：

```powershell
cd 'D:\软工大作业\6-17-\src\frontend'
npm ci
npm run build
```

Vite 会将构建结果输出到 Django 的静态资源目录，并生成资源清单。随后在项目根目录执行：

```powershell
cd 'D:\软工大作业\6-17-\src'
python manage.py collectstatic --noinput
python manage.py check
```

## 九、常用检查命令

```powershell
cd 'D:\软工大作业\6-17-\src'

python manage.py check
python manage.py test
python manage.py runserver
```

前端构建验证：

```powershell
cd 'D:\软工大作业\6-17-\src\frontend'
npm run build
```

## 十、注意事项

- 开发环境下必须同时运行 Django 后端和 Vite 前端。
- 生产环境建议关闭 `DEBUG`，并使用合适的 WSGI/ASGI 服务器和反向代理。
- 邮件、OAuth、Redis、Elasticsearch、Cloudflare 和百度推送等功能需要单独配置对应环境变量或第三方平台参数。
- 数据库账号、密码、微信/邮件密钥等敏感信息不得提交到公开仓库。
- 页面样式异常时，优先检查 Vite 的 `5173` 端口和后端 `8000` 端口是否都在运行。

## 十一、致谢与许可

本项目基于优秀开源项目 **DjangoBlog** 学习与二次实践：

- 项目地址：https://github.com/liangliangyy/DjangoBlog
- 开源许可证：MIT License

再次感谢原作者及所有开源贡献者。本项目中的课程作业整理与学习实践内容仅用于个人课程学习和考核，不用于商业用途。

