@echo off
chcp 65001 >nul  # 解决中文乱码问题
echo 正在启动后端服务，请稍等...

:: 1. 启动主后端（py310_main环境）：打开新CMD窗口，激活环境并运行
start "Backend-Main (py310_main)" cmd /k "call conda activate py310_main && cd /d .\backend && python main.py run"

:: 2. 启动py310_service（py310环境）：打开新CMD窗口，激活环境并运行
start "py310_service (py310)" cmd /k "call conda activate py310 && cd /d .\python_services\py310_service && python app.py"

echo 所有后端服务已启动！每个服务在独立CMD窗口运行，关闭窗口可停止对应服务。
pause