from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn
import pandas as pd

from fastapi.responses import JSONResponse



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


# 创建FastAPI应用实例
app = FastAPI(
    title="AIXLab py314_service",  # 文档标题
    description="AIXLab Python 3.14 子服务接口文档",  # 文档描述
    version="1.0.0"  # 版本号
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源，实际生产环境应限制
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 健康检查接口（必填，对应日志中的/health）
@app.get("/api/py314/health", summary="健康检查", description="检查服务是否正常运行")
async def health_check():
    return JSONResponse(
        status_code=200,
        content={"status": "success", "message": "Service is running", "port": 8001}
    )

# 示例接口（添加至少一个业务接口）
@app.get("/api/hello", summary="测试接口", description="返回欢迎信息")
async def hello_world(name: str = "Guest"):
    return {"message": f"Hello {name}!", "service": "py314_service"}

# 启动服务的入口（如果需要直接运行该文件）
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8001,
        reload=True,  # 热重载，修改代码自动重启
        log_level="info"
    )
