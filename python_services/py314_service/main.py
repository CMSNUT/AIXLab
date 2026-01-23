import os
from typing import Any, Dict, Optional
from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

import pandas as pd

from fastapi.middleware.cors import CORSMiddleware

# 创建FastAPI实例(注意: 不要设置docs_url=None)
app = FastAPI(
    title="AIXLab Python分析服务",
    description="AIXLab Python分析服务API文档",
    version="0.1.0"
)

# 挂载静态文件目录(用于存放本地Swagger UI资源, 若不需要可跳过)
# 如果你不想手动下载资源, 方案2更简单
# app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源, 实际生产环境应限制
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据模型


class PlotRequest(BaseModel):
    dataset_path: str
    plot_type: str = "scatter"
    parameters: Optional[Dict[str, Any]] = None


class ExecuteRequest(BaseModel):
    dataset_path: str
    code: str
    parameters: Optional[Dict[str, Any]] = None


# ========== API端点 ==========


@app.get("/")
async def root():
    return {
        "message": "AIXLab Python分析服务运行中",
        "version": "1.0",
        "endpoints": {
            "health": "/api/py314/health (GET)"
        }
    }


@app.get("/api/py314/health")
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "service": "py314",
        "version": "0.1.0",
        "timestamp": pd.Timestamp.now().isoformat()
    }


if __name__ == "__main__":
  print("=" * 60)
  print("AIXLab Python分析服务启动")
  print("=" * 60)
  print("服务端口: 8001")
  print("API Swagger UI文档: http://localhost:8001/docs")
  print("API Redoc 文档: http://localhost:8001/redoc")
  print("=" * 60)

  # 启动服务
  uvicorn.run(
    "main:app", 
    host="0.0.0.0", 
    port=8001, 
    reload=True,
    log_level="debug"  # 改为debug级别
  )
