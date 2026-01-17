# 一、配置anaconda虚拟环境
## 1. conda 创建环境
```bash
conda create -n ipac-env python=3.12
```

## 2. 从已有conda环境中复制
```bash
conda env export > environment.yml
pip freeze > requirements.txt
```
## 3. 在 VS Code 中选择环境
- 打开 Python 解释器选择器
    - 点击 VS Code 左下角的 Python 版本
    - 或按 Ctrl + Shift + P → "Python: Select Interpreter"

## 4. 项目配置
- 创建 .vscode/settings.json
```json
{
    "python.defaultInterpreterPath": "~/anaconda3/envs/ipac-env/bin/python",
    "python.terminal.activateEnvironment": true,
    "python.terminal.activateEnvInCurrentTerminal": true
}
```

# 二、全栈项目架构
## 1. 基础架构
- 前端：vue3 + vite + element-plus + axios + pinia + router + nprogress + JavaScript
- 后端：主后端 fastAPI + python分析后端 fastAPI + R后端 plumber
- 数据库：MySQL

## 2. 项目整体架构
```text
AIXLAB/
├── frontend/                    # Vue3前端项目
├── backend/                     # FastAPI主后端
├── pyapi/                       # Python分析后端
├── rapi/                        # R语言分析后端
├── database/                    # 数据库相关文件
├── environment.yml
├── README.md                    
└── requirements.txt
```

# 三、主后端架构 (backend/)
## 1. 主后端目录
```text
backend/              # 主后端
├── app/
│   ├── __init__.py
│   ├── main.py      # FastAPI应用
│   ├── config.py    # 配置
│   ├── database.py  # 数据库
│   ├── models.py    # 数据模型
│   ├── routers/     # API路由
│   └── services/    # 业务服务
│── requirements.txt
└── Dockerfile
```
## 2. pyapi/ (Python分析后端)
```text
pyapi/               # Python分析后端
├── app/
│   ├── __init__.py
│   ├── main.py      # Python分析API
│   └── analysis/    # 分析功能
│── requirements.txt
└── Dockerfile
```

## 3. rapi/ (R分析后端)
```text
rapi/                # R分析后端
├── R/
│   ├── app.R       # Plumber API
│   └── analysis.R  # R分析功能
├── Dockerfile
└── requirements.R
```

## 2. 创建项目
```bash
# 1. 创建项目目录
mkdir backend
mkdir pyapi
mkdir rapi

cd backend

# 2. 创建项目结构
......
```

## 3. 代码顺序




# 四、Python分析后端架构 (pyapi/)


# 五、R语言分析后端架构 (rapi/)


# 六、前端项目（frontend）
### 3.1 初始化项目
```bash

```

### 3.2 目录结构
```text

``` 


