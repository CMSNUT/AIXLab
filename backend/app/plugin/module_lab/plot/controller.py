# -*- coding: utf-8 -*-

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, UploadFile, Body, Path, Query
from fastapi.responses import FileResponse, StreamingResponse, JSONResponse
import httpx
from pathlib import Path as PathLib

from app.common.response import ErrorResponse, SuccessResponse, StreamResponse, UploadFileResponse
from app.core.dependencies import AuthPermission
from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.base_params import PaginationQueryParam
from app.utils.common_util import bytes2file_response
from app.core.logger import log
from app.core.base_schema import BatchSetAvailable
from app.core.router_class import OperationLogRoute
from app.config.setting import settings
from .model import BatchRequest, CalculationRequest

from .service import LabPlotService
from .schema import  LabPlotCreateSchema, LabPlotUpdateSchema, LabPlotQueryParam

LabPlotRouter = APIRouter(route_class=OperationLogRoute, prefix='/plot', tags=["绘图工具管理模块"]) 


@LabPlotRouter.get("/detail/{id}", summary="获取绘图工具管理详情", description="获取绘图工具管理详情")
async def get_plot_detail_controller(
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_lab:plot:query"]))
) -> JSONResponse:
    """获取绘图工具管理详情接口"""
    result_dict = await LabPlotService.detail_plot_service(auth=auth, id=id)
    log.info(f"获取绘图工具管理详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取绘图工具管理详情成功")

@LabPlotRouter.get("/list", summary="查询绘图工具管理列表", description="查询绘图工具管理列表")
async def get_plot_list_controller(
    page: PaginationQueryParam = Depends(),
    search: LabPlotQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_lab:plot:query"]))
) -> JSONResponse:
    """查询绘图工具管理列表接口（数据库分页）"""
    result_dict = await LabPlotService.page_plot_service(
        auth=auth,
        page_no=page.page_no if page.page_no is not None else 1,
        page_size=page.page_size if page.page_size is not None else 10,
        search=search,
        order_by=page.order_by
    )
    log.info("查询绘图工具管理列表成功")
    return SuccessResponse(data=result_dict, msg="查询绘图工具管理列表成功")

@LabPlotRouter.post("/create", summary="创建绘图工具管理", description="创建绘图工具管理")
async def create_plot_controller(
    data: LabPlotCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(["module_lab:plot:create"]))
) -> JSONResponse:
    """创建绘图工具管理接口"""
    result_dict = await LabPlotService.create_plot_service(auth=auth, data=data)
    log.info("创建绘图工具管理成功")
    return SuccessResponse(data=result_dict, msg="创建绘图工具管理成功")

@LabPlotRouter.put("/update/{id}", summary="修改绘图工具管理", description="修改绘图工具管理")
async def update_plot_controller(
    data: LabPlotUpdateSchema,
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_lab:plot:update"]))
) -> JSONResponse:
    """修改绘图工具管理接口"""
    result_dict = await LabPlotService.update_plot_service(auth=auth, id=id, data=data)
    log.info("修改绘图工具管理成功")
    return SuccessResponse(data=result_dict, msg="修改绘图工具管理成功")

@LabPlotRouter.delete("/delete", summary="删除绘图工具管理", description="删除绘图工具管理")
async def delete_plot_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_lab:plot:delete"]))
) -> JSONResponse:
    """删除绘图工具管理接口"""
    await LabPlotService.delete_plot_service(auth=auth, ids=ids)
    log.info(f"删除绘图工具管理成功: {ids}")
    return SuccessResponse(msg="删除绘图工具管理成功")

@LabPlotRouter.patch("/available/setting", summary="批量修改绘图工具管理状态", description="批量修改绘图工具管理状态")
async def batch_set_available_plot_controller(
    data: BatchSetAvailable,
    auth: AuthSchema = Depends(AuthPermission(["module_lab:plot:patch"]))
) -> JSONResponse:
    """批量修改绘图工具管理状态接口"""
    await LabPlotService.set_available_plot_service(auth=auth, data=data)
    log.info(f"批量修改绘图工具管理状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改绘图工具管理状态成功")

@LabPlotRouter.post('/export', summary="导出绘图工具管理", description="导出绘图工具管理")
async def export_plot_list_controller(
    search: LabPlotQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_lab:plot:export"]))
) -> StreamingResponse:
    """导出绘图工具管理接口"""
    result_dict_list = await LabPlotService.list_plot_service(search=search, auth=auth)
    export_result = await LabPlotService.batch_export_plot_service(obj_list=result_dict_list)
    log.info('导出绘图工具管理成功')
    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            'Content-Disposition': 'attachment; filename=lab_plot.xlsx'
        }
    )

@LabPlotRouter.post('/import', summary="导入绘图工具管理", description="导入绘图工具管理")
async def import_plot_list_controller(
    file: UploadFile,
    auth: AuthSchema = Depends(AuthPermission(["module_lab:plot:import"]))
) -> JSONResponse:
    """导入绘图工具管理接口"""
    batch_import_result = await LabPlotService.batch_import_plot_service(file=file, auth=auth, update_support=True)
    log.info("导入绘图工具管理成功")
    return SuccessResponse(data=batch_import_result, msg="导入绘图工具管理成功")

@LabPlotRouter.post('/download/template', summary="获取绘图工具管理导入模板", description="获取绘图工具管理导入模板", dependencies=[Depends(AuthPermission(["module_lab:plot:download"]))])
async def export_plot_template_controller() -> StreamingResponse:
    """获取绘图工具管理导入模板接口"""
    import_template_result = await LabPlotService.import_template_download_plot_service()
    log.info('获取绘图工具管理导入模板成功')
    return StreamResponse(
        data=bytes2file_response(import_template_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename=lab_plot_template.xlsx'}
    )


@LabPlotRouter.post("/add", summary="加法计算")
async def calculate_add_controller(
    req: CalculationRequest = Body(..., description="加法计算请求参数")
) -> JSONResponse:
    try:
        # 调用业务逻辑层，获取R服务返回的结果
        add_result = await LabPlotService.add_service(a=req.a, b=req.b)
        
        # 返回标准成功响应（匹配统一响应模型）
        return SuccessResponse( add_result )
    except HTTPException as e:
        # 捕获service层抛出的异常，返回标准错误响应
        return ErrorResponse(e)
    except Exception as e:
        # 捕获未预期的异常
        return ErrorResponse(e)



# 批量计算端点
@LabPlotRouter.post("/batch_add")
async def calculate_batch(request: BatchRequest):
    """批量执行多个计算操作"""
    try:
        # 准备批量请求数据
        operations_data = []
        for op in request.operations:
            operations_data.append({
                "type": op.type,
                "a": op.a,
                "b": op.b
            })
        
        r_request_data = {
            "operations": operations_data
        }
        
        # 调用R后端批量API
        async with httpx.AsyncClient(timeout=settings.R_API_TIMEOUT) as client:
            response = await client.post(
                f"{settings.R_API_BASE_URL}/api/r452/batch_add",
                json=r_request_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"R批量服务错误: {response.text}"
                )
            
            result = response.json()
            
            # 添加代理层信息
            result["proxy_layer"] = {
                "name": "Python FastAPI Proxy",
                "request_count": len(operations_data)
            }
            
            return result
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"批量处理失败: {str(e)}"
        )

