# 初始化项目(pyproject.toml)
```bash
uv init backend

cd backend
```

# 初始化 alembic.ini 的生成
```bash
alembic init alembic
```
- 创建 `backend/app` 文件夹，
- 将 `alembic` 文件夹 复制到 `app` 文件夹中
- 修改 根目录下 `alembic.ini` 文件中 `%(here)s/alembic` 为 `app/alembic`






# 运行
```bash
cd backend

pip install -r requirements.txt

conda env export -n py314_main > ./py314_main.yaml
# pip freeze > ./requirements.txt

cd backend
python main.py run --env=dev
```


# Python包分类及安装命令
## 基础库和工具
```txt
anyio==4.12.1                           # 异步IO支持库
attrs==25.4.0                           # 类装饰器
certifi==2026.1.4                       # SSL证书
cffi==2.0.0                             # C外部函数接口(与已安装版本一致)
charset-normalizer==3.4.4               # 字符编码检测
click==8.3.1                            # 命令行工具框架
click-didyoumean==0.3.1                 # Click扩展: 命令提示
click-plugins==1.1.1.2                  # Click扩展: 插件系统
click-repl==0.3.0                       # Click扩展: REPL支持
colorama==0.4.6                         # 跨平台彩色终端输出
distro==1.9.0                           # Linux发行版信息
greenlet==3.3.0                         # 协程支持
h11==0.16.0                             # HTTP/1.1协议实现
httpcore==1.0.9                         # HTTP客户端核心
httptools==0.7.1                        # HTTP协议工具
httpx==0.28.1                           # 异步HTTP客户端
httpx-sse==0.4.3                        # HTTPX SSE支持
idna==3.11                              # 国际化域名处理
iniconfig==2.3.0                        # INI配置文件解析
itsdangerous==2.2.0                     # 安全签名
jiter==0.12.0                           # JSON解析器
markdown-it-py==4.0.0                   # Markdown解析器
mdurl==0.1.2                            # URL处理工具
orjson==3.11.5                          # 高性能JSON编解码
packaging==25.0                         # 包版本处理
pluggy==1.6.0                           # 插件系统
prompt_toolkit==3.0.52                  # 命令行提示工具
psutil==7.2.1                           # 系统监控
pycparser==3.0                          # C语言解析器
Pygments==2.19.2                        # 语法高亮
python-dateutil==2.9.0.post0            # 日期时间处理
python-dotenv==1.2.1                    # 环境变量管理
pytz==2025.2                            # 时区处理
PyYAML==6.0.3                           # YAML解析器
regex==2026.1.15                        # 正则表达式
requests==2.32.5                        # HTTP请求库
requests-toolbelt==1.0.0                # Requests工具集
rich==14.2.0                            # 富文本终端
rich-toolkit==0.17.1                    # Rich扩展工具
rignore==0.7.6                          # 文件忽略模式
shellingham==1.5.4                      # Shell检测
six==1.17.0                             # Python2/3兼容
sniffio==1.3.1                          # 异步库检测
sse-starlette==3.2.0                    # Starlette SSE支持
tenacity==9.1.2                         # 重试库
tqdm==4.67.1                            # 进度条
typer==0.21.1                           # 命令行工具构建
typing-inspection==0.4.2                # 类型检查
typing_extensions==4.15.0               # 类型提示扩展
tzdata==2025.3                          # 时区数据库
tzlocal==5.3.1                          # 本地时区
ujson==5.11.0                           # 超快JSON编解码
urllib3==2.6.3                          # HTTP客户端
uuid_utils==0.14.0                      # UUID工具
vine==5.1.0                             # 回调工具
watchfiles==1.1.1                       # 文件监控
wcwidth==0.3.0                          # 字符宽度计算
websockets==16.0                        # WebSocket实现
win32_setctime==1.2.0                   # Windows文件时间设置
xxhash==3.6.0                           # 快速哈希
zstandard==0.25.0                       # Zstandard压缩
loguru==0.7.3                           # 日志库
```

## 构建和包管理工具
```txt
build==1.4.0                            # 包构建工具
setuptools==80.10.1                     # 包构建工具
wheel==0.46.2                           # Python wheel打包
pip-tools==7.5.2                        # pip依赖管理工具
pyproject_hooks==1.2.0                  # pyproject.toml钩子
ormsgpack==1.12.2                       # msgpack序列化
```

## Web框架和服务器
```txt
fastapi==0.128.0                        # FastAPI Web框架
starlette==0.50.0                       # ASGI框架(FastAPI依赖)
uvicorn==0.40.0                         # ASGI服务器
gunicorn==23.0.0                        # WSGI HTTP服务器
fastapi-cli==0.0.20                     # FastAPI命令行工具
fastapi-cloud-cli==0.11.0               # FastAPI云部署工具
fastapi-limiter==0.1.6                  # FastAPI限流
fastar==0.8.0                           # FastAPI工具集
python-multipart==0.0.21                # 多部分表单解析
```

## 数据库和ORM
```txt
SQLAlchemy==2.0.46                      # SQL工具包和ORM
alembic==1.18.1                         # 数据库迁移工具
databases==0.9.0                        # 异步数据库支持
aiomysql==0.3.2                         # 异步MySQL客户端
PyMySQL==1.1.2                          # MySQL Python驱动
redis==7.1.0                            # Redis客户端
Mako==1.3.10                            # 模板引擎(Alembic依赖)
```

## 安全认证
```txt
bcrypt==5.0.0                           # 密码哈希
cryptography==46.0.3                    # 加密算法
passlib==1.7.4                          # 密码哈希工具
PyJWT==2.10.1                           # JWT令牌
python-jose==3.5.0                      # JOSE实现
rsa==4.9.1                              # RSA加密
ecdsa==0.19.1                           # ECDSA签名
pyasn1==0.6.2                           # ASN.1编解码
email-validator==2.3.0                  # 邮箱验证
```

## 任务队列和定时任务
```txt
celery==5.6.2                           # 分布式任务队列
kombu==5.6.2                            # AMQP消息队列(Celery依赖)
amqp==5.3.1                             # AMQP协议实现
billiard==4.2.4                         # 多进程池(Celery依赖)
APScheduler==3.11.2                     # 定时任务调度
croniter==6.0.0                         # Cron表达式解析
```

## AI和机器学习
```txt
openai==2.15.0                          # OpenAI API客户端
anthropic==0.76.0                       # Anthropic API客户端
langchain==1.2.6                        # LangChain框架
langchain-core==1.2.7                   # LangChain核心
langchain-openai==1.1.7                 # LangChain OpenAI集成
langchain-anthropic==1.3.1              # LangChain Anthropic集成
langchain-mcp-adapters==0.2.1           # LangChain MCP适配器
langgraph==1.0.6                        # LangGraph工作流
langgraph-checkpoint==4.0.0             # LangGraph检查点
langgraph-prebuilt==1.0.6               # LangGraph预建组件
langgraph-sdk==0.3.3                    # LangGraph SDK
langsmith==0.6.4                        # LangChain追踪
mcp==1.25.0                             # 模型上下文协议
tiktoken==0.12.0                        # OpenAI分词器
annotated-doc==0.0.4                    # 文档注解
```

## 数据分析和处理
```txt
pandas==3.0.0                           # 数据分析库
numpy==2.4.1                            # 数值计算
openpyxl==3.1.5                         # Excel读写
et_xmlfile==2.0.0                       # XML文件支持(openpyxl依赖)
```

## 模板引擎
```txt
Jinja2==3.1.6                           # 模板引擎
MarkupSafe==3.0.3                       # 安全HTML字符串
```

## 验证和序列化
```txt
pydantic==2.12.5                        # 数据验证和设置管理
pydantic_core==2.41.5                   # Pydantic核心
pydantic-extra-types==2.11.0            # Pydantic额外类型
pydantic-settings==2.12.0               # Pydantic设置管理
pydantic-validation-decorator==0.1.5    # Pydantic验证装饰器
annotated-types==0.7.0                  # 注解类型
docstring_parser==0.17.0                # 文档字符串解析
jsonpatch==1.33                         # JSON补丁
jsonpointer==3.0.0                      # JSON指针
jsonschema==4.26.0                      # JSON模式验证
jsonschema-specifications==2025.9.1     # JSON模式规范
referencing==0.37.0                     # JSON引用
rpds-py==0.30.0                         # 持久化数据结构
```

## 异步文件操作
```txt
aiofiles==25.1.0                        # 异步文件操作
```

## 图像处理
```txt
pillow==12.1.0                          # 图像处理库
```

## 用户代理分析
```txt
user-agents==2.2.0                      # 用户代理解析
ua-parser==1.0.1                        # 用户代理解析器
ua-parser-builtins==202601              # 用户代理解析内置数据
```

## 监控和错误追踪
```txt
sentry-sdk==2.50.0                      # Sentry错误追踪
```

## 网络工具
```txt
dnspython==2.8.0                        # DNS工具包
```

## 测试框架
```txt
pytest==9.0.2                           # 测试框架
```

## Windows特定
```txt
pywin32==311                            # Windows扩展
```

## 代码检查
```txt
ruff==0.14.13                           # Rust编写的Python代码检查器
```


# 一键安装所有依赖的最高版本(不指定具体版本)，可以使用以下方法: 

## 方法1: 生成并安装最新版依赖文件
```bash
# 1. 从当前项目依赖生成 requirements.txt(不指定版本)
echo "anyio
attrs
certifi
cffi
charset-normalizer
click
click-didyoumean
click-plugins
click-repl
colorama
distro
greenlet
h11
httpcore
httptools
httpx
httpx-sse
idna
iniconfig
itsdangerous
jiter
markdown-it-py
mdurl
orjson
packaging
pluggy
prompt_toolkit
psutil
pycparser
Pygments
python-dateutil
python-dotenv
pytz
PyYAML
regex
requests
requests-toolbelt
rich
rich-toolkit
rignore
shellingham
six
sniffio
sse-starlette
tenacity
tqdm
typer
typing-inspection
typing_extensions
tzdata
tzlocal
ujson
urllib3
uuid_utils
vine
watchfiles
wcwidth
websockets
win32_setctime
xxhash
zstandard
fastapi
starlette
uvicorn
fastapi-cli
fastapi-cloud-cli
fastapi-limiter
fastar
gunicorn
python-multipart
SQLAlchemy
alembic
databases
aiomysql
PyMySQL
redis
Mako
bcrypt
cryptography
passlib
PyJWT
python-jose
rsa
ecdsa
pyasn1
email-validator
celery
kombu
amqp
billiard
APScheduler
croniter
openai
anthropic
langchain
langchain-core
langchain-openai
langchain-anthropic
langchain-mcp-adapters
langgraph
langgraph-checkpoint
langgraph-prebuilt
langgraph-sdk
langsmith
mcp
tiktoken
annotated-doc
pandas
numpy
openpyxl
et_xmlfile
Jinja2
MarkupSafe
pydantic
pydantic-core
pydantic-extra-types
pydantic-settings
pydantic-validation-decorator
annotated-types
docstring_parser
jsonpatch
jsonpointer
jsonschema
jsonschema-specifications
referencing
rpds-py
aiofiles
pillow
user-agents
ua-parser
ua-parser-builtins
sentry-sdk
dnspython
pytest
pywin32
ruff" > requirements_latest.txt

# 2. 安装最新版本
pip install --upgrade -r requirements_latest.txt
```

## 方法2: 直接安装所有包的最新版(一行命令)
```bash
pip install --upgrade anyio attrs certifi cffi charset-normalizer click click-didyoumean click-plugins click-repl colorama distro greenlet h11 httpcore httptools httpx httpx-sse idna iniconfig itsdangerous jiter markdown-it-py mdurl orjson packaging pluggy prompt_toolkit psutil pycparser Pygments python-dateutil python-dotenv pytz PyYAML regex requests requests-toolbelt rich rich-toolkit rignore shellingham six sniffio sse-starlette tenacity tqdm typer typing-inspection typing_extensions tzdata tzlocal ujson urllib3 uuid_utils vine watchfiles wcwidth websockets win32_setctime xxhash zstandard fastapi starlette uvicorn fastapi-cli fastapi-cloud-cli fastapi-limiter fastar gunicorn python-multipart SQLAlchemy alembic databases aiomysql PyMySQL redis Mako bcrypt cryptography passlib PyJWT python-jose rsa ecdsa pyasn1 email-validator celery kombu amqp billiard APScheduler croniter openai anthropic langchain langchain-core langchain-openai langchain-anthropic langchain-mcp-adapters langgraph langgraph-checkpoint langgraph-prebuilt langgraph-sdk langsmith mcp tiktoken annotated-doc pandas numpy openpyxl et_xmlfile Jinja2 MarkupSafe pydantic pydantic-core pydantic-extra-types pydantic-settings pydantic-validation-decorator annotated-types docstring_parser jsonpatch jsonpointer jsonschema jsonschema-specifications referencing rpds-py aiofiles pillow user-agents ua-parser ua-parser-builtins sentry-sdk dnspython pytest pywin32 ruff
```

## 方法3: 使用脚本安装
创建一个 `install_latest.py` 脚本: 
```python
#!/usr/bin/env python3
import subprocess

packages = [
    "anyio", "attrs", "certifi", "cffi", "charset-normalizer", "click", 
    "click-didyoumean", "click-plugins", "click-repl", "colorama", "distro",
    "greenlet", "h11", "httpcore", "httptools", "httpx", "httpx-sse", "idna",
    "iniconfig", "itsdangerous", "jiter", "markdown-it-py", "mdurl", "orjson",
    "packaging", "pluggy", "prompt_toolkit", "psutil", "pycparser", "Pygments",
    "python-dateutil", "python-dotenv", "pytz", "PyYAML", "regex", "requests",
    "requests-toolbelt", "rich", "rich-toolkit", "rignore", "shellingham", "six",
    "sniffio", "sse-starlette", "tenacity", "tqdm", "typer", "typing-inspection",
    "typing_extensions", "tzdata", "tzlocal", "ujson", "urllib3", "uuid_utils",
    "vine", "watchfiles", "wcwidth", "websockets", "win32_setctime", "xxhash",
    "zstandard", "fastapi", "starlette", "uvicorn", "fastapi-cli", 
    "fastapi-cloud-cli", "fastapi-limiter", "fastar", "gunicorn", 
    "python-multipart", "SQLAlchemy", "alembic", "databases", "aiomysql",
    "PyMySQL", "redis", "Mako", "bcrypt", "cryptography", "passlib", "PyJWT",
    "python-jose", "rsa", "ecdsa", "pyasn1", "email-validator", "celery",
    "kombu", "amqp", "billiard", "APScheduler", "croniter", "openai",
    "anthropic", "langchain", "langchain-core", "langchain-openai",
    "langchain-anthropic", "langchain-mcp-adapters", "langgraph",
    "langgraph-checkpoint", "langgraph-prebuilt", "langgraph-sdk", "langsmith",
    "mcp", "tiktoken", "annotated-doc", "pandas", "numpy", "openpyxl",
    "et_xmlfile", "Jinja2", "MarkupSafe", "pydantic", "pydantic-core",
    "pydantic-extra-types", "pydantic-settings", 
    "pydantic-validation-decorator", "annotated-types", "docstring_parser",
    "jsonpatch", "jsonpointer", "jsonschema", "jsonschema-specifications",
    "referencing", "rpds-py", "aiofiles", "pillow", "user-agents", 
    "ua-parser", "ua-parser-builtins", "sentry-sdk", "dnspython", "pytest",
    "pywin32", "ruff"
]

print(f"正在安装 {len(packages)} 个包的最新版本...")

# 分批安装以避免命令行过长
batch_size = 50
for i in range(0, len(packages), batch_size):
    batch = packages[i:i+batch_size]
    cmd = ["pip", "install", "--upgrade"] + batch
    print(f"安装批次 {i//batch_size + 1}: {batch[:3]}... 等 {len(batch)} 个包")
    subprocess.run(cmd)

print("所有包安装完成！")
```

运行脚本: 
```bash
python install_latest.py
```

## 方法4: 使用 pip-compile(最推荐)
```bash
# 1. 安装 pip-tools
pip install pip-tools

# 2. 创建 requirements.in 文件，只写包名
- requirements.in
```text
anyio
attrs
certifi
cffi
charset-normalizer
click
click-didyoumean
click-plugins
click-repl
colorama
distro
greenlet
h11
httpcore
httptools
httpx
httpx-sse
idna
iniconfig
itsdangerous
jiter
markdown-it-py
mdurl
orjson
packaging
pluggy
prompt_toolkit
psutil
pycparser
Pygments
python-dateutil
python-dotenv
pytz
PyYAML
regex
requests
requests-toolbelt
rich
rich-toolkit
rignore
shellingham
six
sniffio
sse-starlette
tenacity
tqdm
typer
typing-inspection
typing_extensions
tzdata
tzlocal
ujson
urllib3
uuid_utils
vine
watchfiles
wcwidth
websockets
win32_setctime
xxhash
zstandard
fastapi
starlette
uvicorn
fastapi-cli
fastapi-cloud-cli
fastapi-limiter
fastar
gunicorn
python-multipart
SQLAlchemy
alembic
databases
aiomysql
PyMySQL
redis
Mako
bcrypt
cryptography
passlib
PyJWT
python-jose
rsa
ecdsa
pyasn1
email-validator
celery
kombu
amqp
billiard
APScheduler
croniter
openai
anthropic
langchain
langchain-core
langchain-openai
langchain-anthropic
langchain-mcp-adapters
langgraph
langgraph-checkpoint
langgraph-prebuilt
langgraph-sdk
langsmith
mcp
tiktoken
annotated-doc
pandas
numpy
openpyxl
et_xmlfile
Jinja2
MarkupSafe
pydantic
pydantic-core
pydantic-extra-types
pydantic-settings
pydantic-validation-decorator
annotated-types
docstring_parser
jsonpatch
jsonpointer
jsonschema
jsonschema-specifications
referencing
rpds-py
aiofiles
pillow
user-agents
ua-parser
ua-parser-builtins
sentry-sdk
dnspython
pytest
pywin32
ruff
```

# 3. 生成带有最新版本的 requirements.txt
pip-compile --upgrade requirements.in -o requirements_latest.txt

# 4. 安装
pip install -r requirements_latest.txt
```

**推荐使用方法4**，因为它会: 
1. 自动解析依赖关系
2. 安装最新的兼容版本
3. 生成带有精确版本号的 requirements.txt 文件
4. 避免版本冲突
