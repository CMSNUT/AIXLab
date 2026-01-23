@echo off
chcp 65001 >nul
:: 关闭批处理自身的命令回显，解决中文乱码

:: ==================== 配置项（根据你的实际路径/环境名修改） ====================
:: Conda安装根路径（必填，替换为你的Anaconda/Miniconda路径）
set "CONDA_PATH=D:\anaconda3"
:: 项目根路径（脚本所在目录，无需修改，自动识别）
set "PROJECT_DIR=%~dp0"

set "PY_MAIN_ENV=py310_main"               :: Python主后端环境名
set "PY_MAIN_PATH=%PROJECT_DIR%backend"    :: Python主后端脚本目录
set "PY_MAIN_SCRIPT=main.py"           :: Python主后端启动命令（带run参数）


:: ==================== 并行启动各服务（独立CMD窗口） ====================
echo 正在启动所有服务（Python子服务 + R子服务 + 主后端 + 前端）...
echo.

:: 1. 启动Python子服务（py314）- 独立CMD窗口，激活conda环境后运行
echo 启动Python子服务(%PY_Main_ENV%)...
start "Python-Main" cmd /k "echo 正在启动Python服务... && echo 激活conda环境... && call "%CONDA_PATH%\Scripts\activate.bat" %PY_Main_ENV% && cd /d "%PY_Main_PATH%" && python "%PY_Main_SCRIPT%" run && pause"

:: ==================== 启动完成提示 ====================
echo.
echo ✅ 所有服务已启动！
echo.
pause