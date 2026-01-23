from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn
import requests
import os
import json

app = FastAPI(title="AIXLab API", version="1.0")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据模型


class PlotRequest(BaseModel):
    language: str  # "python" 或 "r"
    plot_type: str = "scatter"
    parameters: Optional[Dict[str, Any]] = None


# 数据集路径
IRIS_PATH = os.path.join(os.path.dirname(__file__), "data", "iris.csv")


@app.get("/")
async def root():
    return {"message": "AIXLab API 运行中", "version": "1.0"}


@app.get("/api/health")
async def health_check():
    """健康检查"""
    services_status = {
        "main_service": "healthy",
        "python_service": "unknown",
        "r_service": "unknown"
    }

    # 检查Python分析服务
    try:
        response = requests.get(
            "http://localhost:8001/api/python/health", timeout=3)
        if response.status_code == 200:
            services_status["python_service"] = "healthy"
        else:
            services_status["python_service"] = "unhealthy"
    except:
        services_status["python_service"] = "unreachable"

    # 检查R分析服务
    try:
        response = requests.get(
            "http://localhost:8002/api/r/health", timeout=3)
        if response.status_code == 200:
            services_status["r_service"] = "healthy"
        else:
            services_status["r_service"] = "unhealthy"
    except:
        services_status["r_service"] = "unreachable"

    return services_status


@app.post("/api/plot")
async def create_plot(request: PlotRequest):
    """创建图表"""

    # 检查语言支持
    if request.language.lower() not in ["python", "r"]:
        raise HTTPException(status_code=400, detail="只支持 'python' 或 'r' 语言")

    # 构建请求数据
    plot_data = {
        "dataset_path": IRIS_PATH,
        "plot_type": request.plot_type,
        "parameters": request.parameters or {}
    }

    try:
        # 调用相应的分析服务
        if request.language.lower() == "python":
            service_url = "http://localhost:8001"
            endpoint = f"{service_url}/api/python/plot"
        else:
            service_url = "http://localhost:8002"
            endpoint = f"{service_url}/api/r/plot"

        # 发送请求
        response = requests.post(endpoint, json=plot_data, timeout=30)

        if response.status_code == 200:
            result = response.json()
            result["language"] = request.language
            return result
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"分析服务错误: {response.text[:200]}"
            )

    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503,
            detail=f"{request.language} 分析服务未启动, 请先启动分析服务"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"请求失败: {str(e)}")


@app.get("/api/test/python-plot")
async def test_python_plot():
    """测试Python绘图"""
    try:
        response = requests.post(
            "http://localhost:8001/api/python/plot",
            json={
                "dataset_path": IRIS_PATH,
                "plot_type": "scatter",
                "parameters": {}
            },
            timeout=10
        )
        result = response.json()
        result["language"] = "python"
        return result
    except Exception as e:
        return {
            "success": False,
            "error": f"Python分析服务未启动或错误: {str(e)}",
            "language": "python"
        }


@app.get("/api/test/r-plot")
async def test_r_plot():
    """测试R绘图"""
    try:
        response = requests.post(
            "http://localhost:8002/api/r/plot",
            json={
                "dataset_path": IRIS_PATH,
                "plot_type": "scatter",
                "parameters": {}
            },
            timeout=10
        )
        result = response.json()
        result["language"] = "r"
        return result
    except Exception as e:
        return {
            "success": False,
            "error": f"R分析服务未启动或错误: {str(e)}",
            "language": "r"
        }

if __name__ == "__main__":
    # 检查数据文件
    if not os.path.exists(IRIS_PATH):
        print(f"警告: 数据集文件不存在: {IRIS_PATH}")
        print("将使用内置示例数据")

    print("=" * 60)
    print("AIXLab 主后端服务启动")
    print("API地址: http://localhost:8000")
    print("API文档: http://localhost:8000/docs")
    print("Python分析服务: http://localhost:8001")
    print("R分析服务: http://localhost:8002")
    print("前端: http://localhost:5173")
    print("=" * 60)

    # 使用字符串模块名启动, 以支持reload
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
