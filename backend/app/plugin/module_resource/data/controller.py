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

from .service import ResourceDataService
from .schema import ResourceDataCreateSchema, ResourceDataUpdateSchema, ResourceDataQueryParam

ResourceDataRouter = APIRouter(route_class=OperationLogRoute, prefix='/data', tags=["数据模块"]) 

@ResourceDataRouter.get("/detail/{id}", summary="获取数据详情", description="获取数据详情")
async def get_data_detail_controller(
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_resource:data:query"]))
) -> JSONResponse:
    """获取数据详情接口"""
    result_dict = await ResourceDataService.detail_data_service(auth=auth, id=id)
    log.info(f"获取数据详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取数据详情成功")

@ResourceDataRouter.get("/list", summary="查询数据列表", description="查询数据列表")
async def get_data_list_controller(
    page: PaginationQueryParam = Depends(),
    search: ResourceDataQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_resource:data:query"]))
) -> JSONResponse:
    """查询数据列表接口（数据库分页）"""
    result_dict = await ResourceDataService.page_data_service(
        auth=auth,
        page_no=page.page_no if page.page_no is not None else 1,
        page_size=page.page_size if page.page_size is not None else 10,
        search=search,
        order_by=page.order_by
    )
    log.info("查询数据列表成功")
    return SuccessResponse(data=result_dict, msg="查询数据列表成功")

@ResourceDataRouter.post("/create", summary="创建数据", description="创建数据")
async def create_data_controller(
    data: ResourceDataCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(["module_resource:data:create"]))
) -> JSONResponse:
    """创建数据接口"""
    result_dict = await ResourceDataService.create_data_service(auth=auth, data=data)
    log.info("创建数据成功")
    return SuccessResponse(data=result_dict, msg="创建数据成功")

@ResourceDataRouter.put("/update/{id}", summary="修改数据", description="修改数据")
async def update_data_controller(
    data: ResourceDataUpdateSchema,
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_resource:data:update"]))
) -> JSONResponse:
    """修改数据接口"""
    result_dict = await ResourceDataService.update_data_service(auth=auth, id=id, data=data)
    log.info("修改数据成功")
    return SuccessResponse(data=result_dict, msg="修改数据成功")

@ResourceDataRouter.delete("/delete", summary="删除数据", description="删除数据")
async def delete_data_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_resource:data:delete"]))
) -> JSONResponse:
    """删除数据接口"""
    await ResourceDataService.delete_data_service(auth=auth, ids=ids)
    log.info(f"删除数据成功: {ids}")
    return SuccessResponse(msg="删除数据成功")

@ResourceDataRouter.patch("/available/setting", summary="批量修改数据状态", description="批量修改数据状态")
async def batch_set_available_data_controller(
    data: BatchSetAvailable,
    auth: AuthSchema = Depends(AuthPermission(["module_resource:data:patch"]))
) -> JSONResponse:
    """批量修改数据状态接口"""
    await ResourceDataService.set_available_data_service(auth=auth, data=data)
    log.info(f"批量修改数据状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改数据状态成功")

@ResourceDataRouter.post('/export', summary="导出数据", description="导出数据")
async def export_data_list_controller(
    search: ResourceDataQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_resource:data:export"]))
) -> StreamingResponse:
    """导出数据接口"""
    result_dict_list = await ResourceDataService.list_data_service(search=search, auth=auth)
    export_result = await ResourceDataService.batch_export_data_service(obj_list=result_dict_list)
    log.info('导出数据成功')
    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            'Content-Disposition': 'attachment; filename=resource_data.xlsx'
        }
    )

@ResourceDataRouter.post('/import', summary="导入数据", description="导入数据")
async def import_data_list_controller(
    file: UploadFile,
    auth: AuthSchema = Depends(AuthPermission(["module_resource:data:import"]))
) -> JSONResponse:
    """导入数据接口"""
    batch_import_result = await ResourceDataService.batch_import_data_service(file=file, auth=auth, update_support=True)
    log.info("导入数据成功")
    return SuccessResponse(data=batch_import_result, msg="导入数据成功")

@ResourceDataRouter.post('/download/template', summary="获取数据导入模板", description="获取数据导入模板", dependencies=[Depends(AuthPermission(["module_resource:data:download"]))])
async def export_data_template_controller() -> StreamingResponse:
    """获取数据导入模板接口"""
    import_template_result = await ResourceDataService.import_template_download_data_service()
    log.info('获取数据导入模板成功')
    return StreamResponse(
        data=bytes2file_response(import_template_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename=resource_data_template.xlsx'}
    )