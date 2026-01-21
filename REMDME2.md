# Python包分类及安装命令

## 一、包分类及作用说明

| 类别                   | 包含的包                                                                                                                                                                                                            | 主要作用                                                         |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| **Web框架与服务器**    | fastapi, uvicorn, gunicorn, starlette, fastapi-cli, fastapi-cloud-cli, fastapi-limiter, fastar, sse-starlette, watchfiles, websockets, httptools, h11                                                               | FastAPI框架及其相关组件、ASGI/WSGI服务器、WebSocket支持、热重载  |
| **数据库与ORM**        | SQLAlchemy, alembic, databases, asyncpg, psycopg, aiomysql, aiosqlite, PyMySQL, aiomysql                                                                                                                            | 数据库ORM、迁移工具、多种数据库驱动（PostgreSQL、MySQL、SQLite） |
| **异步任务与消息队列** | celery, amqp, billiard, kombu, vine, redis, APScheduler, croniter                                                                                                                                                   | 分布式任务队列、消息代理、定时任务调度                           |
| **异步与并发**         | greenlet, anyio, sniffio, asyncio相关库                                                                                                                                                                             | 异步编程支持、协程、事件循环                                     |
| **HTTP客户端**         | httpx, httpcore, requests, urllib3, requests-toolbelt, httpx-sse                                                                                                                                                    | HTTP客户端（同步/异步）、SSE支持                                 |
| **数据验证与配置**     | pydantic, pydantic-core, pydantic-settings, pydantic-extra-types, pydantic-validation-decorator, email-validator, annotated-types, typing-inspection, typing_extensions                                             | 数据验证、配置管理、类型注解                                     |
| **模板与渲染**         | Jinja2, Mako, MarkupSafe                                                                                                                                                                                            | 模板引擎、安全渲染                                               |
| **安全与认证**         | bcrypt, cryptography, itsdangerous, PyJWT, python-jose, passlib, certifi, ecdsa, rsa, pyasn1, cffi, pycparser                                                                                                       | 密码哈希、加密解密、JWT认证、SSL证书                             |
| **文件与多媒体**       | aiofiles, pillow, openpyxl, et_xmlfile, xxhash, zstandard, win32_setctime                                                                                                                                           | 异步文件操作、图像处理、Excel操作、压缩解压                      |
| **数据处理与分析**     | pandas, numpy, python-dateutil, pytz, tzdata, tzlocal                                                                                                                                                               | 数据分析、科学计算、时间日期处理                                 |
| **日志与监控**         | loguru, sentry-sdk, psutil                                                                                                                                                                                          | 日志记录、错误监控、系统监控                                     |
| **命令行工具**         | typer, click, click-didyoumean, click-plugins, click-repl, colorama, prompt_toolkit, pygments, rich, rich-toolkit, shellingham, tqdm, wcwidth                                                                       | CLI应用开发、终端美化、进度条、补全                              |
| **开发工具与测试**     | pytest, iniconfig, pluggy, ruff, annotated-doc, docstring_parser, jsonpatch, jsonpointer, jsonschema, jsonschema-specifications, referencing, rpds-py, rignore, distro                                              | 测试框架、代码格式化、文档解析、JSON处理                         |
| **AI与大模型**         | anthropic, openai, langchain, langchain-anthropic, langchain-core, langchain-mcp-adapters, langchain-openai, langgraph, langgraph-checkpoint, langgraph-prebuilt, langgraph-sdk, langsmith, mcp, tiktoken, tenacity | 大模型API、LangChain框架、AI应用开发、token计算                  |
| **序列化与解析**       | orjson, ormsgpack, ujson, json相关库, markdown-it-py, mdurl, PyYAML, jiter                                                                                                                                          | JSON序列化、MessagePack、Markdown解析、YAML解析                  |
| **网络与协议**         | httpx-sse, websockets, httpcore, h11, idna, charset-normalizer, dnspython                                                                                                                                           | WebSocket、SSE、HTTP协议、编码处理                               |
| **工具与工具包**       | user-agents, ua-parser, ua-parser-builtins, uuid_utils, python-dotenv, six, regex, packaging, pywin32                                                                                                               | User-Agent解析、UUID生成、环境变量、正则表达式                   |
| **其他依赖**           | tenacity, tqdm, colorama, wcwidth, sniffio, anyio                                                                                                                                                                   | 重试机制、进度条、跨平台支持                                     |

## 二、分类安装命令（不带版本号）

```bash
# 1. Web框架与服务器
pip install fastapi uvicorn gunicorn starlette fastapi-cli fastapi-cloud-cli fastapi-limiter fastar sse-starlette watchfiles websockets httptools h11

# 2. 数据库与ORM
pip install SQLAlchemy alembic databases asyncpg psycopg aiomysql aiosqlite PyMySQL aiomysql

# 3. 异步任务与消息队列
pip install celery amqp billiard kombu vine redis APScheduler croniter

# 4. 异步与并发
pip install greenlet anyio sniffio

# 5. HTTP客户端
pip install httpx httpcore requests urllib3 requests-toolbelt httpx-sse

# 6. 数据验证与配置
pip install pydantic pydantic-core pydantic-settings pydantic-extra-types pydantic-validation-decorator email-validator annotated-types typing-inspection typing_extensions

# 7. 模板与渲染
pip install Jinja2 Mako MarkupSafe

# 8. 安全与认证
pip install bcrypt cryptography itsdangerous PyJWT python-jose passlib certifi ecdsa rsa pyasn1 cffi pycparser

# 9. 文件与多媒体
pip install aiofiles pillow openpyxl et_xmlfile xxhash zstandard win32_setctime

# 10. 数据处理与分析
pip install pandas numpy python-dateutil pytz tzdata tzlocal

# 11. 日志与监控
pip install loguru sentry-sdk psutil

# 12. 命令行工具
pip install typer click click-didyoumean click-plugins click-repl colorama prompt_toolkit pygments rich rich-toolkit shellingham tqdm wcwidth

# 13. 开发工具与测试
pip install pytest iniconfig pluggy ruff annotated-doc docstring_parser jsonpatch jsonpointer jsonschema jsonschema-specifications referencing rpds-py rignore distro

# 14. AI与大模型
pip install anthropic openai langchain langchain-anthropic langchain-core langchain-mcp-adapters langchain-openai langgraph langgraph-checkpoint langgraph-prebuilt langgraph-sdk langsmith mcp tiktoken tenacity

# 15. 序列化与解析
pip install orjson ormsgpack ujson markdown-it-py mdurl PyYAML jiter

# 16. 网络与协议
pip install httpx-sse websockets httpcore h11 idna charset-normalizer dnspython

# 17. 工具与工具包
pip install user-agents ua-parser ua-parser-builtins uuid_utils python-dotenv six regex packaging pywin32

# 18. 其他依赖
pip install tenacity tqdm colorama wcwidth sniffio anyio
```

## 三、精简安装命令（按功能模块）

```bash
# 基础Web服务
pip install fastapi uvicorn gunicorn starlette websockets httpx

# 数据库全套
pip install SQLAlchemy alembic databases asyncpg psycopg aiomysql aiosqlite PyMySQL

# 异步任务处理
pip install celery redis APScheduler croniter

# 开发工具链
pip install pytest ruff loguru rich typer click

# AI大模型开发
pip install langchain openai anthropic langchain-openai langchain-anthropic tiktoken

# 数据处理
pip install pandas numpy openpyxl pillow

# 安全认证
pip install bcrypt cryptography PyJWT passlib python-jose
```

## 四、一键安装所有依赖

```bash
# 创建requirements.txt文件安装
echo "aiofiles aiomysql aiosqlite alembic amqp annotated-doc annotated-types anthropic anyio APScheduler asyncpg attrs bcrypt billiard celery certifi cffi charset-normalizer click click-didyoumean click-plugins click-repl colorama croniter cryptography databases distro dnspython docstring_parser ecdsa email-validator et_xmlfile fastapi fastapi-cli fastapi-cloud-cli fastapi-limiter fastar greenlet gunicorn h11 httpcore httptools httpx httpx-sse idna iniconfig itsdangerous Jinja2 jiter jsonpatch jsonpointer jsonschema jsonschema-specifications kombu langchain langchain-anthropic langchain-core langchain-mcp-adapters langchain-openai langgraph langgraph-checkpoint langgraph-prebuilt langgraph-sdk langsmith loguru Mako markdown-it-py MarkupSafe mcp mdurl numpy openai openpyxl orjson ormsgpack packaging pandas passlib pillow pluggy prompt_toolkit psutil psycopg pyasn1 pycparser pydantic pydantic-extra-types pydantic-settings pydantic-validation-decorator pydantic_core Pygments PyJWT PyMySQL pytest python-dateutil python-dotenv python-jose python-multipart pytz pywin32 PyYAML redis referencing regex requests requests-toolbelt rich rich-toolkit rignore rpds-py rsa ruff sentry-sdk shellingham six sniffio SQLAlchemy sqlglot sqlglotrs sse-starlette starlette tenacity tiktoken tqdm typer typing-inspection typing_extensions tzdata tzlocal ua-parser ua-parser-builtins ujson uuid_utils urllib3 user-agents uvicorn vine watchfiles wcwidth websockets win32_setctime xxhash zstandard" | tr ' ' '\n' > requirements.txt
pip install -r requirements.txt
```

## 五、常见问题说明

1. **平台特定包**：`pywin32`, `win32_setctime` 仅在Windows系统需要
2. **可选依赖**：`sqlglotrs` 是`sqlglot`的可选依赖，用于Rust加速
3. **版本兼容性**：`bcrypt` 需要Python 3.6+，与早期版本API有变化
4. **开发依赖**：`ruff`, `pytest`, `iniconfig`, `pluggy` 主要在开发环境使用
5. **AI模型依赖**：`tiktoken` 用于OpenAI模型的token计数，`anthropic`用于Claude模型

这个依赖集合显示这是一个功能非常全面的AI Web应用项目，包含：

- 完整的Web服务框架（FastAPI）
- 多数据库支持（PostgreSQL、MySQL、SQLite）
- 异步任务处理（Celery + Redis）
- AI大模型集成（OpenAI、Anthropic、LangChain）
- 完整的开发工具链
- 丰富的数据处理和安全认证功能

# 运行

```bash
cd backend

pip install -r requirements.txt


python main.py run --env=dev
```
