# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, UploadFile, Body, Path, Query
from fastapi.responses import StreamingResponse, JSONResponse

from app.common.response import SuccessResponse, StreamResponse
from app.core.dependencies import AuthPermission
from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.base_params import PaginationQueryParam
from app.utils.common_util import bytes2file_response
from app.core.logger import log
from app.core.base_schema import BatchSetAvailable
from app.core.router_class import OperationLogRoute

from .service import ResourceChartService
from .schema import ResourceChartCreateSchema, ResourceChartUpdateSchema, ResourceChartQueryParam

ResourceChartRouter = APIRouter(route_class=OperationLogRoute, prefix='/chart', tags=["图表模块"]) 

@ResourceChartRouter.get("/detail/{id}", summary="获取图表详情", description="获取图表详情")
async def get_chart_detail_controller(
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_resource:chart:query"]))
) -> JSONResponse:
    """获取图表详情接口"""
    result_dict = await ResourceChartService.detail_chart_service(auth=auth, id=id)
    log.info(f"获取图表详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取图表详情成功")

@ResourceChartRouter.get("/list", summary="查询图表列表", description="查询图表列表")
async def get_chart_list_controller(
    page: PaginationQueryParam = Depends(),
    search: ResourceChartQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_resource:chart:query"]))
) -> JSONResponse:
    """查询图表列表接口（数据库分页）"""
    result_dict = await ResourceChartService.page_chart_service(
        auth=auth,
        page_no=page.page_no if page.page_no is not None else 1,
        page_size=page.page_size if page.page_size is not None else 10,
        search=search,
        order_by=page.order_by
    )
    log.info("查询图表列表成功")
    return SuccessResponse(data=result_dict, msg="查询图表列表成功")

@ResourceChartRouter.post("/create", summary="创建图表", description="创建图表")
async def create_chart_controller(
    data: ResourceChartCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(["module_resource:chart:create"]))
) -> JSONResponse:
    """创建图表接口"""
    result_dict = await ResourceChartService.create_chart_service(auth=auth, data=data)
    log.info("创建图表成功")
    return SuccessResponse(data=result_dict, msg="创建图表成功")

@ResourceChartRouter.put("/update/{id}", summary="修改图表", description="修改图表")
async def update_chart_controller(
    data: ResourceChartUpdateSchema,
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_resource:chart:update"]))
) -> JSONResponse:
    """修改图表接口"""
    result_dict = await ResourceChartService.update_chart_service(auth=auth, id=id, data=data)
    log.info("修改图表成功")
    return SuccessResponse(data=result_dict, msg="修改图表成功")

@ResourceChartRouter.delete("/delete", summary="删除图表", description="删除图表")
async def delete_chart_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_resource:chart:delete"]))
) -> JSONResponse:
    """删除图表接口"""
    await ResourceChartService.delete_chart_service(auth=auth, ids=ids)
    log.info(f"删除图表成功: {ids}")
    return SuccessResponse(msg="删除图表成功")

@ResourceChartRouter.patch("/available/setting", summary="批量修改图表状态", description="批量修改图表状态")
async def batch_set_available_chart_controller(
    data: BatchSetAvailable,
    auth: AuthSchema = Depends(AuthPermission(["module_resource:chart:patch"]))
) -> JSONResponse:
    """批量修改图表状态接口"""
    await ResourceChartService.set_available_chart_service(auth=auth, data=data)
    log.info(f"批量修改图表状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改图表状态成功")

@ResourceChartRouter.post('/export', summary="导出图表", description="导出图表")
async def export_chart_list_controller(
    search: ResourceChartQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_resource:chart:export"]))
) -> StreamingResponse:
    """导出图表接口"""
    result_dict_list = await ResourceChartService.list_chart_service(search=search, auth=auth)
    export_result = await ResourceChartService.batch_export_chart_service(obj_list=result_dict_list)
    log.info('导出图表成功')
    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            'Content-Disposition': 'attachment; filename=resource_chart.xlsx'
        }
    )

@ResourceChartRouter.post('/import', summary="导入图表", description="导入图表")
async def import_chart_list_controller(
    file: UploadFile,
    auth: AuthSchema = Depends(AuthPermission(["module_resource:chart:import"]))
) -> JSONResponse:
    """导入图表接口"""
    batch_import_result = await ResourceChartService.batch_import_chart_service(file=file, auth=auth, update_support=True)
    log.info("导入图表成功")
    return SuccessResponse(data=batch_import_result, msg="导入图表成功")

@ResourceChartRouter.post('/download/template', summary="获取图表导入模板", description="获取图表导入模板", dependencies=[Depends(AuthPermission(["module_resource:chart:download"]))])
async def export_chart_template_controller() -> StreamingResponse:
    """获取图表导入模板接口"""
    import_template_result = await ResourceChartService.import_template_download_chart_service()
    log.info('获取图表导入模板成功')
    return StreamResponse(
        data=bytes2file_response(import_template_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename=resource_chart_template.xlsx'}
    )