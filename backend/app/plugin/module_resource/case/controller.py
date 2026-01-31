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

from .service import ResourceCaseService
from .schema import ResourceCaseCreateSchema, ResourceCaseUpdateSchema, ResourceCaseQueryParam

ResourceCaseRouter = APIRouter(route_class=OperationLogRoute, prefix='/case', tags=["案例模块"]) 

@ResourceCaseRouter.get("/detail/{id}", summary="获取案例详情", description="获取案例详情")
async def get_case_detail_controller(
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_resource:case:query"]))
) -> JSONResponse:
    """获取案例详情接口"""
    result_dict = await ResourceCaseService.detail_case_service(auth=auth, id=id)
    log.info(f"获取案例详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取案例详情成功")

@ResourceCaseRouter.get("/list", summary="查询案例列表", description="查询案例列表")
async def get_case_list_controller(
    page: PaginationQueryParam = Depends(),
    search: ResourceCaseQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_resource:case:query"]))
) -> JSONResponse:
    """查询案例列表接口（数据库分页）"""
    result_dict = await ResourceCaseService.page_case_service(
        auth=auth,
        page_no=page.page_no if page.page_no is not None else 1,
        page_size=page.page_size if page.page_size is not None else 10,
        search=search,
        order_by=page.order_by
    )
    log.info("查询案例列表成功")
    return SuccessResponse(data=result_dict, msg="查询案例列表成功")

@ResourceCaseRouter.post("/create", summary="创建案例", description="创建案例")
async def create_case_controller(
    data: ResourceCaseCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(["module_resource:case:create"]))
) -> JSONResponse:
    """创建案例接口"""
    result_dict = await ResourceCaseService.create_case_service(auth=auth, data=data)
    log.info("创建案例成功")
    return SuccessResponse(data=result_dict, msg="创建案例成功")

@ResourceCaseRouter.put("/update/{id}", summary="修改案例", description="修改案例")
async def update_case_controller(
    data: ResourceCaseUpdateSchema,
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_resource:case:update"]))
) -> JSONResponse:
    """修改案例接口"""
    result_dict = await ResourceCaseService.update_case_service(auth=auth, id=id, data=data)
    log.info("修改案例成功")
    return SuccessResponse(data=result_dict, msg="修改案例成功")

@ResourceCaseRouter.delete("/delete", summary="删除案例", description="删除案例")
async def delete_case_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_resource:case:delete"]))
) -> JSONResponse:
    """删除案例接口"""
    await ResourceCaseService.delete_case_service(auth=auth, ids=ids)
    log.info(f"删除案例成功: {ids}")
    return SuccessResponse(msg="删除案例成功")

@ResourceCaseRouter.patch("/available/setting", summary="批量修改案例状态", description="批量修改案例状态")
async def batch_set_available_case_controller(
    data: BatchSetAvailable,
    auth: AuthSchema = Depends(AuthPermission(["module_resource:case:patch"]))
) -> JSONResponse:
    """批量修改案例状态接口"""
    await ResourceCaseService.set_available_case_service(auth=auth, data=data)
    log.info(f"批量修改案例状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改案例状态成功")

@ResourceCaseRouter.post('/export', summary="导出案例", description="导出案例")
async def export_case_list_controller(
    search: ResourceCaseQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_resource:case:export"]))
) -> StreamingResponse:
    """导出案例接口"""
    result_dict_list = await ResourceCaseService.list_case_service(search=search, auth=auth)
    export_result = await ResourceCaseService.batch_export_case_service(obj_list=result_dict_list)
    log.info('导出案例成功')
    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            'Content-Disposition': 'attachment; filename=resource_case.xlsx'
        }
    )

@ResourceCaseRouter.post('/import', summary="导入案例", description="导入案例")
async def import_case_list_controller(
    file: UploadFile,
    auth: AuthSchema = Depends(AuthPermission(["module_resource:case:import"]))
) -> JSONResponse:
    """导入案例接口"""
    batch_import_result = await ResourceCaseService.batch_import_case_service(file=file, auth=auth, update_support=True)
    log.info("导入案例成功")
    return SuccessResponse(data=batch_import_result, msg="导入案例成功")

@ResourceCaseRouter.post('/download/template', summary="获取案例导入模板", description="获取案例导入模板", dependencies=[Depends(AuthPermission(["module_resource:case:download"]))])
async def export_case_template_controller() -> StreamingResponse:
    """获取案例导入模板接口"""
    import_template_result = await ResourceCaseService.import_template_download_case_service()
    log.info('获取案例导入模板成功')
    return StreamResponse(
        data=bytes2file_response(import_template_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename=resource_case_template.xlsx'}
    )