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

from .service import PlotScriptService
from .schema import PlotScriptCreateSchema, PlotScriptUpdateSchema, PlotScriptQueryParam

PlotScriptRouter = APIRouter(route_class=OperationLogRoute, prefix='/script', tags=["绘图脚本管理模块"]) 

@PlotScriptRouter.get("/detail/{id}", summary="获取绘图脚本管理详情", description="获取绘图脚本管理详情")
async def get_script_detail_controller(
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_plot:script:query"]))
) -> JSONResponse:
    """获取绘图脚本管理详情接口"""
    result_dict = await PlotScriptService.detail_script_service(auth=auth, id=id)
    log.info(f"获取绘图脚本管理详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取绘图脚本管理详情成功")

@PlotScriptRouter.get("/list", summary="查询绘图脚本管理列表", description="查询绘图脚本管理列表")
async def get_script_list_controller(
    page: PaginationQueryParam = Depends(),
    search: PlotScriptQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_plot:script:query"]))
) -> JSONResponse:
    """查询绘图脚本管理列表接口（数据库分页）"""
    result_dict = await PlotScriptService.page_script_service(
        auth=auth,
        page_no=page.page_no if page.page_no is not None else 1,
        page_size=page.page_size if page.page_size is not None else 10,
        search=search,
        order_by=page.order_by
    )
    log.info("查询绘图脚本管理列表成功")
    return SuccessResponse(data=result_dict, msg="查询绘图脚本管理列表成功")

@PlotScriptRouter.post("/create", summary="创建绘图脚本管理", description="创建绘图脚本管理")
async def create_script_controller(
    data: PlotScriptCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(["module_plot:script:create"]))
) -> JSONResponse:
    """创建绘图脚本管理接口"""
    result_dict = await PlotScriptService.create_script_service(auth=auth, data=data)
    log.info("创建绘图脚本管理成功")
    return SuccessResponse(data=result_dict, msg="创建绘图脚本管理成功")

@PlotScriptRouter.put("/update/{id}", summary="修改绘图脚本管理", description="修改绘图脚本管理")
async def update_script_controller(
    data: PlotScriptUpdateSchema,
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_plot:script:update"]))
) -> JSONResponse:
    """修改绘图脚本管理接口"""
    result_dict = await PlotScriptService.update_script_service(auth=auth, id=id, data=data)
    log.info("修改绘图脚本管理成功")
    return SuccessResponse(data=result_dict, msg="修改绘图脚本管理成功")

@PlotScriptRouter.delete("/delete", summary="删除绘图脚本管理", description="删除绘图脚本管理")
async def delete_script_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_plot:script:delete"]))
) -> JSONResponse:
    """删除绘图脚本管理接口"""
    await PlotScriptService.delete_script_service(auth=auth, ids=ids)
    log.info(f"删除绘图脚本管理成功: {ids}")
    return SuccessResponse(msg="删除绘图脚本管理成功")

@PlotScriptRouter.patch("/available/setting", summary="批量修改绘图脚本管理状态", description="批量修改绘图脚本管理状态")
async def batch_set_available_script_controller(
    data: BatchSetAvailable,
    auth: AuthSchema = Depends(AuthPermission(["module_plot:script:patch"]))
) -> JSONResponse:
    """批量修改绘图脚本管理状态接口"""
    await PlotScriptService.set_available_script_service(auth=auth, data=data)
    log.info(f"批量修改绘图脚本管理状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改绘图脚本管理状态成功")

@PlotScriptRouter.post('/export', summary="导出绘图脚本管理", description="导出绘图脚本管理")
async def export_script_list_controller(
    search: PlotScriptQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_plot:script:export"]))
) -> StreamingResponse:
    """导出绘图脚本管理接口"""
    result_dict_list = await PlotScriptService.list_script_service(search=search, auth=auth)
    export_result = await PlotScriptService.batch_export_script_service(obj_list=result_dict_list)
    log.info('导出绘图脚本管理成功')
    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            'Content-Disposition': 'attachment; filename=plot_script.xlsx'
        }
    )

@PlotScriptRouter.post('/import', summary="导入绘图脚本管理", description="导入绘图脚本管理")
async def import_script_list_controller(
    file: UploadFile,
    auth: AuthSchema = Depends(AuthPermission(["module_plot:script:import"]))
) -> JSONResponse:
    """导入绘图脚本管理接口"""
    batch_import_result = await PlotScriptService.batch_import_script_service(file=file, auth=auth, update_support=True)
    log.info("导入绘图脚本管理成功")
    return SuccessResponse(data=batch_import_result, msg="导入绘图脚本管理成功")

@PlotScriptRouter.post('/download/template', summary="获取绘图脚本管理导入模板", description="获取绘图脚本管理导入模板", dependencies=[Depends(AuthPermission(["module_plot:script:download"]))])
async def export_script_template_controller() -> StreamingResponse:
    """获取绘图脚本管理导入模板接口"""
    import_template_result = await PlotScriptService.import_template_download_script_service()
    log.info('获取绘图脚本管理导入模板成功')
    return StreamResponse(
        data=bytes2file_response(import_template_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename=plot_script_template.xlsx'}
    )