from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import json

app = FastAPI(title="AIXLAB API Gateway", version="1.0")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 服务配置
PYAPI_URL = "http://pyapi:8001"
RAPI_URL = "http://rapi:8002"

# 健康检查
@app.get("/")
async def root():
    return {"service": "AIXLAB Backend", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "ok"}

# 数据查看接口
@app.post("/api/iris/view")
async def view_iris(backend: str = "python"):
    """查看Iris数据集"""
    if backend == "python":
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{PYAPI_URL}/iris/view")
    elif backend == "R":
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{RAPI_URL}/iris/view")
    else:
        raise HTTPException(400, "backend must be 'python' or 'R'")
    
    return response.json()

# 聚类分析接口
@app.post("/api/iris/cluster")
async def cluster_iris(backend: str = "python", n_clusters: int = 3):
    """Iris数据集聚类分析"""
    if backend == "python":
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{PYAPI_URL}/iris/cluster",
                json={"n_clusters": n_clusters}
            )
    elif backend == "R":
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{RAPI_URL}/iris/cluster",
                json={"n_clusters": n_clusters}
            )
    else:
        raise HTTPException(400, "backend must be 'python' or 'R'")
    
    return response.json()

# 绘图接口
@app.post("/api/iris/plot")
async def plot_iris(
    backend: str = "python",
    plot_type: str = "scatter",
    x_col: str = "sepal_length",
    y_col: str = "sepal_width"
):
    """Iris数据集绘图"""
    if backend == "python":
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{PYAPI_URL}/iris/plot",
                json={
                    "plot_type": plot_type,
                    "x_col": x_col,
                    "y_col": y_col
                }
            )
    elif backend == "R":
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{RAPI_URL}/iris/plot",
                json={
                    "plot_type": plot_type,
                    "x_col": x_col,
                    "y_col": y_col
                }
            )
    else:
        raise HTTPException(400, "backend must be 'python' or 'R'")
    
    return response.json()