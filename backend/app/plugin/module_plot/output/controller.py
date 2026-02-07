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

from .service import PlotOutputService
from .schema import PlotOutputCreateSchema, PlotOutputUpdateSchema, PlotOutputQueryParam

PlotOutputRouter = APIRouter(route_class=OperationLogRoute, prefix='/output', tags=["绘图结果管理模块"]) 

@PlotOutputRouter.get("/detail/{id}", summary="获取绘图结果管理详情", description="获取绘图结果管理详情")
async def get_output_detail_controller(
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_plot:output:query"]))
) -> JSONResponse:
    """获取绘图结果管理详情接口"""
    result_dict = await PlotOutputService.detail_output_service(auth=auth, id=id)
    log.info(f"获取绘图结果管理详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取绘图结果管理详情成功")

@PlotOutputRouter.get("/list", summary="查询绘图结果管理列表", description="查询绘图结果管理列表")
async def get_output_list_controller(
    page: PaginationQueryParam = Depends(),
    search: PlotOutputQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_plot:output:query"]))
) -> JSONResponse:
    """查询绘图结果管理列表接口（数据库分页）"""
    result_dict = await PlotOutputService.page_output_service(
        auth=auth,
        page_no=page.page_no if page.page_no is not None else 1,
        page_size=page.page_size if page.page_size is not None else 10,
        search=search,
        order_by=page.order_by
    )
    log.info("查询绘图结果管理列表成功")
    return SuccessResponse(data=result_dict, msg="查询绘图结果管理列表成功")

@PlotOutputRouter.post("/create", summary="创建绘图结果管理", description="创建绘图结果管理")
async def create_output_controller(
    data: PlotOutputCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(["module_plot:output:create"]))
) -> JSONResponse:
    """创建绘图结果管理接口"""
    result_dict = await PlotOutputService.create_output_service(auth=auth, data=data)
    log.info("创建绘图结果管理成功")
    return SuccessResponse(data=result_dict, msg="创建绘图结果管理成功")

@PlotOutputRouter.put("/update/{id}", summary="修改绘图结果管理", description="修改绘图结果管理")
async def update_output_controller(
    data: PlotOutputUpdateSchema,
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_plot:output:update"]))
) -> JSONResponse:
    """修改绘图结果管理接口"""
    result_dict = await PlotOutputService.update_output_service(auth=auth, id=id, data=data)
    log.info("修改绘图结果管理成功")
    return SuccessResponse(data=result_dict, msg="修改绘图结果管理成功")

@PlotOutputRouter.delete("/delete", summary="删除绘图结果管理", description="删除绘图结果管理")
async def delete_output_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_plot:output:delete"]))
) -> JSONResponse:
    """删除绘图结果管理接口"""
    await PlotOutputService.delete_output_service(auth=auth, ids=ids)
    log.info(f"删除绘图结果管理成功: {ids}")
    return SuccessResponse(msg="删除绘图结果管理成功")

@PlotOutputRouter.patch("/available/setting", summary="批量修改绘图结果管理状态", description="批量修改绘图结果管理状态")
async def batch_set_available_output_controller(
    data: BatchSetAvailable,
    auth: AuthSchema = Depends(AuthPermission(["module_plot:output:patch"]))
) -> JSONResponse:
    """批量修改绘图结果管理状态接口"""
    await PlotOutputService.set_available_output_service(auth=auth, data=data)
    log.info(f"批量修改绘图结果管理状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改绘图结果管理状态成功")

@PlotOutputRouter.post('/export', summary="导出绘图结果管理", description="导出绘图结果管理")
async def export_output_list_controller(
    search: PlotOutputQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_plot:output:export"]))
) -> StreamingResponse:
    """导出绘图结果管理接口"""
    result_dict_list = await PlotOutputService.list_output_service(search=search, auth=auth)
    export_result = await PlotOutputService.batch_export_output_service(obj_list=result_dict_list)
    log.info('导出绘图结果管理成功')
    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            'Content-Disposition': 'attachment; filename=plot_output.xlsx'
        }
    )

@PlotOutputRouter.post('/import', summary="导入绘图结果管理", description="导入绘图结果管理")
async def import_output_list_controller(
    file: UploadFile,
    auth: AuthSchema = Depends(AuthPermission(["module_plot:output:import"]))
) -> JSONResponse:
    """导入绘图结果管理接口"""
    batch_import_result = await PlotOutputService.batch_import_output_service(file=file, auth=auth, update_support=True)
    log.info("导入绘图结果管理成功")
    return SuccessResponse(data=batch_import_result, msg="导入绘图结果管理成功")

@PlotOutputRouter.post('/download/template', summary="获取绘图结果管理导入模板", description="获取绘图结果管理导入模板", dependencies=[Depends(AuthPermission(["module_plot:output:download"]))])
async def export_output_template_controller() -> StreamingResponse:
    """获取绘图结果管理导入模板接口"""
    import_template_result = await PlotOutputService.import_template_download_output_service()
    log.info('获取绘图结果管理导入模板成功')
    return StreamResponse(
        data=bytes2file_response(import_template_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename=plot_output_template.xlsx'}
    )