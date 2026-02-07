from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import httpx
from app.config.setting import settings

HealthRouter = APIRouter(prefix="/health", tags=["健康检查"])


@HealthRouter.get("", summary="健康检查", description="检查系统健康状态")
async def health_check() -> JSONResponse:
    """
    健康检查接口

    返回:
    - JSONResponse: 包含健康状态的JSON响应
    """
    return JSONResponse(content={"msg": True}, status_code=200)

# R服务健康检查
@HealthRouter.get("/api/r452/health")
async def r_health_check():
    """检查R后端服务状态"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{settings.R_API_BASE_URL}/api/r452/health")
            return {
                "python_proxy": "running",
                "r_service": response.json(),
                "status": "connected"
            }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"R服务不可用: {str(e)}"
        )