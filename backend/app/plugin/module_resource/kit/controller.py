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

from .service import ResourceKitService
from .schema import ResourceKitCreateSchema, ResourceKitUpdateSchema, ResourceKitQueryParam

ResourceKitRouter = APIRouter(route_class=OperationLogRoute, prefix='/kit', tags=["模块模块"]) 

@ResourceKitRouter.get("/detail/{id}", summary="获取模块详情", description="获取模块详情")
async def get_kit_detail_controller(
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_resource:kit:query"]))
) -> JSONResponse:
    """获取模块详情接口"""
    result_dict = await ResourceKitService.detail_kit_service(auth=auth, id=id)
    log.info(f"获取模块详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取模块详情成功")

@ResourceKitRouter.get("/list", summary="查询模块列表", description="查询模块列表")
async def get_kit_list_controller(
    page: PaginationQueryParam = Depends(),
    search: ResourceKitQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_resource:kit:query"]))
) -> JSONResponse:
    """查询模块列表接口（数据库分页）"""
    result_dict = await ResourceKitService.page_kit_service(
        auth=auth,
        page_no=page.page_no if page.page_no is not None else 1,
        page_size=page.page_size if page.page_size is not None else 10,
        search=search,
        order_by=page.order_by
    )
    log.info("查询模块列表成功")
    return SuccessResponse(data=result_dict, msg="查询模块列表成功")

@ResourceKitRouter.post("/create", summary="创建模块", description="创建模块")
async def create_kit_controller(
    data: ResourceKitCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(["module_resource:kit:create"]))
) -> JSONResponse:
    """创建模块接口"""
    result_dict = await ResourceKitService.create_kit_service(auth=auth, data=data)
    log.info("创建模块成功")
    return SuccessResponse(data=result_dict, msg="创建模块成功")

@ResourceKitRouter.put("/update/{id}", summary="修改模块", description="修改模块")
async def update_kit_controller(
    data: ResourceKitUpdateSchema,
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_resource:kit:update"]))
) -> JSONResponse:
    """修改模块接口"""
    result_dict = await ResourceKitService.update_kit_service(auth=auth, id=id, data=data)
    log.info("修改模块成功")
    return SuccessResponse(data=result_dict, msg="修改模块成功")

@ResourceKitRouter.delete("/delete", summary="删除模块", description="删除模块")
async def delete_kit_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_resource:kit:delete"]))
) -> JSONResponse:
    """删除模块接口"""
    await ResourceKitService.delete_kit_service(auth=auth, ids=ids)
    log.info(f"删除模块成功: {ids}")
    return SuccessResponse(msg="删除模块成功")

@ResourceKitRouter.patch("/available/setting", summary="批量修改模块状态", description="批量修改模块状态")
async def batch_set_available_kit_controller(
    data: BatchSetAvailable,
    auth: AuthSchema = Depends(AuthPermission(["module_resource:kit:patch"]))
) -> JSONResponse:
    """批量修改模块状态接口"""
    await ResourceKitService.set_available_kit_service(auth=auth, data=data)
    log.info(f"批量修改模块状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改模块状态成功")

@ResourceKitRouter.post('/export', summary="导出模块", description="导出模块")
async def export_kit_list_controller(
    search: ResourceKitQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_resource:kit:export"]))
) -> StreamingResponse:
    """导出模块接口"""
    result_dict_list = await ResourceKitService.list_kit_service(search=search, auth=auth)
    export_result = await ResourceKitService.batch_export_kit_service(obj_list=result_dict_list)
    log.info('导出模块成功')
    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            'Content-Disposition': 'attachment; filename=resource_kit.xlsx'
        }
    )

@ResourceKitRouter.post('/import', summary="导入模块", description="导入模块")
async def import_kit_list_controller(
    file: UploadFile,
    auth: AuthSchema = Depends(AuthPermission(["module_resource:kit:import"]))
) -> JSONResponse:
    """导入模块接口"""
    batch_import_result = await ResourceKitService.batch_import_kit_service(file=file, auth=auth, update_support=True)
    log.info("导入模块成功")
    return SuccessResponse(data=batch_import_result, msg="导入模块成功")

@ResourceKitRouter.post('/download/template', summary="获取模块导入模板", description="获取模块导入模板", dependencies=[Depends(AuthPermission(["module_resource:kit:download"]))])
async def export_kit_template_controller() -> StreamingResponse:
    """获取模块导入模板接口"""
    import_template_result = await ResourceKitService.import_template_download_kit_service()
    log.info('获取模块导入模板成功')
    return StreamResponse(
        data=bytes2file_response(import_template_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename=resource_kit_template.xlsx'}
    )