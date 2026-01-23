@echo off
chcp 65001 >nul
:: 关闭批处理自身的命令回显，解决中文乱码

:: ==================== 配置项（根据你的实际路径/环境名修改） ====================
:: Conda安装根路径（必填，替换为你的Anaconda/Miniconda路径）
set "CONDA_PATH=D:\anaconda3"
:: 项目根路径（脚本所在目录，无需修改，自动识别）
set "PROJECT_DIR=%~dp0"

:: 各Python服务环境名+路径配置
set "PY_MAIN_ENV=py310_main"          :: Python主后端环境名
set "PY_MAIN_PATH=%PROJECT_DIR%backend" :: Python主后端脚本目录
set "PY_MAIN_SCRIPT=main.py run"      :: Python主后端启动命令（带run参数）

set "PY_314_ENV=py314"                 :: Python子服务环境名
set "PY_314_PATH=%PROJECT_DIR%python_services/py314_service" :: Python子服务目录
set "PY_314_SCRIPT=app.py"            :: Python子服务启动脚本
     
:: 各R服务配置（无conda，指定Rscript路径）
set "R_452_PATH=%PROJECT_DIR%r_services/r452_service" :: R服务脚本目录
set "R_452_SCRIPT=run.R" :: R服务启动脚本
set "RSCRIPT_452_PATH=D:\R\R-4.5.2\bin\x64\Rscript.exe" :: Rscript路径

:: 前端服务配置
set "FRONTEND_PATH=%PROJECT_DIR%frontend" :: 前端项目目录
set "FRONTEND_CMD=pnpm dev"           :: 前端启动命令

:: ==================== 并行启动各服务（独立CMD窗口） ====================
echo 正在启动所有服务（Python子服务 + R子服务 + 主后端 + 前端）...

:: 1. 启动Python子服务（py314）- 独立CMD窗口，激活conda环境后运行
start "Python-314 (py314)" cmd /k "call %CONDA_PATH%\Scripts\activate.bat %PY_314_ENV% && cd /d %PY_314_PATH% && python %PY_314_SCRIPT% && pause"

:: 2. 启动R服务（r452_env）- 独立CMD窗口
:: ==================== 启动R服务（无conda） ====================
start "R-Service (r452_env)" cmd /k "cd /d %R_452_PATH% && "%RSCRIPT_452_PATH%" %R_452_SCRIPT% && pause"

:: 3. 启动Python主后端（py310_main）- 独立CMD窗口，激活conda环境后运行
start "Python-Main (py310_main)" cmd /k "call %CONDA_PATH%\Scripts\activate.bat %PY_MAIN_ENV% && cd /d %PY_MAIN_PATH% && python %PY_MAIN_SCRIPT% && pause"

:: 4. 启动前端（pnpm dev）- 独立CMD窗口，直接运行pnpm（需确保pnpm已加环境变量）
start "Frontend (pnpm dev)" cmd /k "cd /d %FRONTEND_PATH% && %FRONTEND_CMD% && pause"

:: ==================== 启动完成提示 ====================
echo.
echo ✅ 所有服务已启动！
echo 📌 Python子服务：%PY_SUB_ENV%环境（独立CMD窗口）
echo 📌 R服务：%R_ENV%环境（独立CMD窗口）
echo 📌 Python主后端：%PY_MAIN_ENV%环境（独立CMD窗口）
echo 📌 前端：%FRONTEND_CMD%（独立CMD窗口）
echo 🔴 停止服务：直接关闭对应CMD窗口即可
pause