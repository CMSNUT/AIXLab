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
        "py310_service": "unknown",
        "r_service": "unknown"
    }

    # 检查Python分析服务
    try:
        response = requests.get(
            "http://localhost:8001/api/py310_service/health", timeout=3)
        if response.status_code == 200:
            services_status["py310_service"] = "healthy"
        else:
            services_status["py310_service"] = "unhealthy"
    except:
        services_status["py310_service"] = "unreachable"

    # 检查R分析服务
    try:
        response = requests.get(
            "http://localhost:8002/api/r452_service/health", timeout=3)
        if response.status_code == 200:
            services_status["r_service"] = "healthy"
        else:
            services_status["r_service"] = "unhealthy"
    except:
        services_status["r_service"] = "unreachable"

    return services_status
