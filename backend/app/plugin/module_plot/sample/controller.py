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

from .service import PlotSampleService
from .schema import PlotSampleCreateSchema, PlotSampleUpdateSchema, PlotSampleQueryParam

PlotSampleRouter = APIRouter(route_class=OperationLogRoute, prefix='/sample', tags=["绘图实例管理模块"]) 

@PlotSampleRouter.get("/detail/{id}", summary="获取绘图实例管理详情", description="获取绘图实例管理详情")
async def get_sample_detail_controller(
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_plot:sample:query"]))
) -> JSONResponse:
    """获取绘图实例管理详情接口"""
    result_dict = await PlotSampleService.detail_sample_service(auth=auth, id=id)
    log.info(f"获取绘图实例管理详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取绘图实例管理详情成功")

@PlotSampleRouter.get("/list", summary="查询绘图实例管理列表", description="查询绘图实例管理列表")
async def get_sample_list_controller(
    page: PaginationQueryParam = Depends(),
    search: PlotSampleQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_plot:sample:query"]))
) -> JSONResponse:
    """查询绘图实例管理列表接口（数据库分页）"""
    result_dict = await PlotSampleService.page_sample_service(
        auth=auth,
        page_no=page.page_no if page.page_no is not None else 1,
        page_size=page.page_size if page.page_size is not None else 10,
        search=search,
        order_by=page.order_by
    )
    log.info("查询绘图实例管理列表成功")
    return SuccessResponse(data=result_dict, msg="查询绘图实例管理列表成功")

@PlotSampleRouter.post("/create", summary="创建绘图实例管理", description="创建绘图实例管理")
async def create_sample_controller(
    data: PlotSampleCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(["module_plot:sample:create"]))
) -> JSONResponse:
    """创建绘图实例管理接口"""
    result_dict = await PlotSampleService.create_sample_service(auth=auth, data=data)
    log.info("创建绘图实例管理成功")
    return SuccessResponse(data=result_dict, msg="创建绘图实例管理成功")

@PlotSampleRouter.put("/update/{id}", summary="修改绘图实例管理", description="修改绘图实例管理")
async def update_sample_controller(
    data: PlotSampleUpdateSchema,
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_plot:sample:update"]))
) -> JSONResponse:
    """修改绘图实例管理接口"""
    result_dict = await PlotSampleService.update_sample_service(auth=auth, id=id, data=data)
    log.info("修改绘图实例管理成功")
    return SuccessResponse(data=result_dict, msg="修改绘图实例管理成功")

@PlotSampleRouter.delete("/delete", summary="删除绘图实例管理", description="删除绘图实例管理")
async def delete_sample_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_plot:sample:delete"]))
) -> JSONResponse:
    """删除绘图实例管理接口"""
    await PlotSampleService.delete_sample_service(auth=auth, ids=ids)
    log.info(f"删除绘图实例管理成功: {ids}")
    return SuccessResponse(msg="删除绘图实例管理成功")

@PlotSampleRouter.patch("/available/setting", summary="批量修改绘图实例管理状态", description="批量修改绘图实例管理状态")
async def batch_set_available_sample_controller(
    data: BatchSetAvailable,
    auth: AuthSchema = Depends(AuthPermission(["module_plot:sample:patch"]))
) -> JSONResponse:
    """批量修改绘图实例管理状态接口"""
    await PlotSampleService.set_available_sample_service(auth=auth, data=data)
    log.info(f"批量修改绘图实例管理状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改绘图实例管理状态成功")

@PlotSampleRouter.post('/export', summary="导出绘图实例管理", description="导出绘图实例管理")
async def export_sample_list_controller(
    search: PlotSampleQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_plot:sample:export"]))
) -> StreamingResponse:
    """导出绘图实例管理接口"""
    result_dict_list = await PlotSampleService.list_sample_service(search=search, auth=auth)
    export_result = await PlotSampleService.batch_export_sample_service(obj_list=result_dict_list)
    log.info('导出绘图实例管理成功')
    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            'Content-Disposition': 'attachment; filename=plot_sample.xlsx'
        }
    )

@PlotSampleRouter.post('/import', summary="导入绘图实例管理", description="导入绘图实例管理")
async def import_sample_list_controller(
    file: UploadFile,
    auth: AuthSchema = Depends(AuthPermission(["module_plot:sample:import"]))
) -> JSONResponse:
    """导入绘图实例管理接口"""
    batch_import_result = await PlotSampleService.batch_import_sample_service(file=file, auth=auth, update_support=True)
    log.info("导入绘图实例管理成功")
    return SuccessResponse(data=batch_import_result, msg="导入绘图实例管理成功")

@PlotSampleRouter.post('/download/template', summary="获取绘图实例管理导入模板", description="获取绘图实例管理导入模板", dependencies=[Depends(AuthPermission(["module_plot:sample:download"]))])
async def export_sample_template_controller() -> StreamingResponse:
    """获取绘图实例管理导入模板接口"""
    import_template_result = await PlotSampleService.import_template_download_sample_service()
    log.info('获取绘图实例管理导入模板成功')
    return StreamResponse(
        data=bytes2file_response(import_template_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename=plot_sample_template.xlsx'}
    )