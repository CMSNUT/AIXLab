from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn
import pandas as pd



app = FastAPI(title="AIXLab Python分析服务")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源，实际生产环境应限制
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
        "message": "AIXLab py314_service 运行中",
        "version": "0.1.0",
        "endpoints": {
            "health": "/api/py314/health (GET)"
        }
    }


@app.get("/api/py314/health")
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "service": "py314_service",
        "version": "0.1.0",
        "timestamp": pd.Timestamp.now().isoformat()
    }


if __name__ == "__main__":
    print("=" * 60)
    print("AIXLab py314_service启动")
    print("=" * 60)
    print("服务端口: 8001")
    print("API文档: http://localhost:8001/docs")
    print("健康检查: http://localhost:8001/health")
    print("=" * 60)

    # 启动服务
    uvicorn.run("app:app", host="localhost", port=8001, reload=True)
