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

from .service import ResourceScriptService
from .schema import ResourceScriptCreateSchema, ResourceScriptUpdateSchema, ResourceScriptQueryParam

ResourceScriptRouter = APIRouter(route_class=OperationLogRoute, prefix='/script', tags=["脚本模块"]) 

@ResourceScriptRouter.get("/detail/{id}", summary="获取脚本详情", description="获取脚本详情")
async def get_script_detail_controller(
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_resource:script:query"]))
) -> JSONResponse:
    """获取脚本详情接口"""
    result_dict = await ResourceScriptService.detail_script_service(auth=auth, id=id)
    log.info(f"获取脚本详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取脚本详情成功")

@ResourceScriptRouter.get("/list", summary="查询脚本列表", description="查询脚本列表")
async def get_script_list_controller(
    page: PaginationQueryParam = Depends(),
    search: ResourceScriptQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_resource:script:query"]))
) -> JSONResponse:
    """查询脚本列表接口（数据库分页）"""
    result_dict = await ResourceScriptService.page_script_service(
        auth=auth,
        page_no=page.page_no if page.page_no is not None else 1,
        page_size=page.page_size if page.page_size is not None else 10,
        search=search,
        order_by=page.order_by
    )
    log.info("查询脚本列表成功")
    return SuccessResponse(data=result_dict, msg="查询脚本列表成功")

@ResourceScriptRouter.post("/create", summary="创建脚本", description="创建脚本")
async def create_script_controller(
    data: ResourceScriptCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(["module_resource:script:create"]))
) -> JSONResponse:
    """创建脚本接口"""
    result_dict = await ResourceScriptService.create_script_service(auth=auth, data=data)
    log.info("创建脚本成功")
    return SuccessResponse(data=result_dict, msg="创建脚本成功")

@ResourceScriptRouter.put("/update/{id}", summary="修改脚本", description="修改脚本")
async def update_script_controller(
    data: ResourceScriptUpdateSchema,
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_resource:script:update"]))
) -> JSONResponse:
    """修改脚本接口"""
    result_dict = await ResourceScriptService.update_script_service(auth=auth, id=id, data=data)
    log.info("修改脚本成功")
    return SuccessResponse(data=result_dict, msg="修改脚本成功")

@ResourceScriptRouter.delete("/delete", summary="删除脚本", description="删除脚本")
async def delete_script_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_resource:script:delete"]))
) -> JSONResponse:
    """删除脚本接口"""
    await ResourceScriptService.delete_script_service(auth=auth, ids=ids)
    log.info(f"删除脚本成功: {ids}")
    return SuccessResponse(msg="删除脚本成功")

@ResourceScriptRouter.patch("/available/setting", summary="批量修改脚本状态", description="批量修改脚本状态")
async def batch_set_available_script_controller(
    data: BatchSetAvailable,
    auth: AuthSchema = Depends(AuthPermission(["module_resource:script:patch"]))
) -> JSONResponse:
    """批量修改脚本状态接口"""
    await ResourceScriptService.set_available_script_service(auth=auth, data=data)
    log.info(f"批量修改脚本状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改脚本状态成功")

@ResourceScriptRouter.post('/export', summary="导出脚本", description="导出脚本")
async def export_script_list_controller(
    search: ResourceScriptQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_resource:script:export"]))
) -> StreamingResponse:
    """导出脚本接口"""
    result_dict_list = await ResourceScriptService.list_script_service(search=search, auth=auth)
    export_result = await ResourceScriptService.batch_export_script_service(obj_list=result_dict_list)
    log.info('导出脚本成功')
    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            'Content-Disposition': 'attachment; filename=resource_script.xlsx'
        }
    )

@ResourceScriptRouter.post('/import', summary="导入脚本", description="导入脚本")
async def import_script_list_controller(
    file: UploadFile,
    auth: AuthSchema = Depends(AuthPermission(["module_resource:script:import"]))
) -> JSONResponse:
    """导入脚本接口"""
    batch_import_result = await ResourceScriptService.batch_import_script_service(file=file, auth=auth, update_support=True)
    log.info("导入脚本成功")
    return SuccessResponse(data=batch_import_result, msg="导入脚本成功")

@ResourceScriptRouter.post('/download/template', summary="获取脚本导入模板", description="获取脚本导入模板", dependencies=[Depends(AuthPermission(["module_resource:script:download"]))])
async def export_script_template_controller() -> StreamingResponse:
    """获取脚本导入模板接口"""
    import_template_result = await ResourceScriptService.import_template_download_script_service()
    log.info('获取脚本导入模板成功')
    return StreamResponse(
        data=bytes2file_response(import_template_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename=resource_script_template.xlsx'}
    )