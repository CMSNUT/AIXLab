from fastapi import APIRouter
from fastapi.responses import JSONResponse
import requests

HealthRouter = APIRouter(prefix="/health", tags=["健康检查"])


@HealthRouter.get("", summary="健康检查", description="检查系统健康状态")
async def health_check() -> JSONResponse:
    """
    健康检查接口

    返回:
    - JSONResponse: 包含健康状态的JSON响应
    """
    # return JSONResponse(content={"msg": True}, status_code=200)

    services_status = {
        "main_service": "healthy",
        "py314_service": "unknown",
        "r452_service": "unknown"
    }

    # 检查Python分析服务
    try:
        response = requests.get(
            "http://localhost:8001/api/py314/health", timeout=3)
        if response.status_code == 200:
            services_status["py314_service"] = "healthy"
        else:
            services_status["py314_service"] = "unhealthy"
    except:
        services_status["py314_service"] = "unreachable"

    # 检查R分析服务
    try:
        response = requests.get(
            "http://localhost:8002/api/r452/health", timeout=3)
        if response.status_code == 200:
            services_status["r452_service"] = "healthy"
        else:
            services_status["r452_service"] = "unhealthy"
    except:
        services_status["r452_service"] = "unreachable"

    return services_status
