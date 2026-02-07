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

from .service import ExampleSectionService
from .schema import ExampleSectionCreateSchema, ExampleSectionUpdateSchema, ExampleSectionQueryParam

ExampleSectionRouter = APIRouter(route_class=OperationLogRoute, prefix='/section', tags=["案例节点管理模块"]) 

@ExampleSectionRouter.get("/detail/{id}", summary="获取案例节点管理详情", description="获取案例节点管理详情")
async def get_section_detail_controller(
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_example:section:query"]))
) -> JSONResponse:
    """获取案例节点管理详情接口"""
    result_dict = await ExampleSectionService.detail_section_service(auth=auth, id=id)
    log.info(f"获取案例节点管理详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取案例节点管理详情成功")

@ExampleSectionRouter.get("/list", summary="查询案例节点管理列表", description="查询案例节点管理列表")
async def get_section_list_controller(
    page: PaginationQueryParam = Depends(),
    search: ExampleSectionQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_example:section:query"]))
) -> JSONResponse:
    """查询案例节点管理列表接口（数据库分页）"""
    result_dict = await ExampleSectionService.page_section_service(
        auth=auth,
        page_no=page.page_no if page.page_no is not None else 1,
        page_size=page.page_size if page.page_size is not None else 10,
        search=search,
        order_by=page.order_by
    )
    log.info("查询案例节点管理列表成功")
    return SuccessResponse(data=result_dict, msg="查询案例节点管理列表成功")

@ExampleSectionRouter.post("/create", summary="创建案例节点管理", description="创建案例节点管理")
async def create_section_controller(
    data: ExampleSectionCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(["module_example:section:create"]))
) -> JSONResponse:
    """创建案例节点管理接口"""
    result_dict = await ExampleSectionService.create_section_service(auth=auth, data=data)
    log.info("创建案例节点管理成功")
    return SuccessResponse(data=result_dict, msg="创建案例节点管理成功")

@ExampleSectionRouter.put("/update/{id}", summary="修改案例节点管理", description="修改案例节点管理")
async def update_section_controller(
    data: ExampleSectionUpdateSchema,
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_example:section:update"]))
) -> JSONResponse:
    """修改案例节点管理接口"""
    result_dict = await ExampleSectionService.update_section_service(auth=auth, id=id, data=data)
    log.info("修改案例节点管理成功")
    return SuccessResponse(data=result_dict, msg="修改案例节点管理成功")

@ExampleSectionRouter.delete("/delete", summary="删除案例节点管理", description="删除案例节点管理")
async def delete_section_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_example:section:delete"]))
) -> JSONResponse:
    """删除案例节点管理接口"""
    await ExampleSectionService.delete_section_service(auth=auth, ids=ids)
    log.info(f"删除案例节点管理成功: {ids}")
    return SuccessResponse(msg="删除案例节点管理成功")

@ExampleSectionRouter.patch("/available/setting", summary="批量修改案例节点管理状态", description="批量修改案例节点管理状态")
async def batch_set_available_section_controller(
    data: BatchSetAvailable,
    auth: AuthSchema = Depends(AuthPermission(["module_example:section:patch"]))
) -> JSONResponse:
    """批量修改案例节点管理状态接口"""
    await ExampleSectionService.set_available_section_service(auth=auth, data=data)
    log.info(f"批量修改案例节点管理状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改案例节点管理状态成功")

@ExampleSectionRouter.post('/export', summary="导出案例节点管理", description="导出案例节点管理")
async def export_section_list_controller(
    search: ExampleSectionQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_example:section:export"]))
) -> StreamingResponse:
    """导出案例节点管理接口"""
    result_dict_list = await ExampleSectionService.list_section_service(search=search, auth=auth)
    export_result = await ExampleSectionService.batch_export_section_service(obj_list=result_dict_list)
    log.info('导出案例节点管理成功')
    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            'Content-Disposition': 'attachment; filename=example_section.xlsx'
        }
    )

@ExampleSectionRouter.post('/import', summary="导入案例节点管理", description="导入案例节点管理")
async def import_section_list_controller(
    file: UploadFile,
    auth: AuthSchema = Depends(AuthPermission(["module_example:section:import"]))
) -> JSONResponse:
    """导入案例节点管理接口"""
    batch_import_result = await ExampleSectionService.batch_import_section_service(file=file, auth=auth, update_support=True)
    log.info("导入案例节点管理成功")
    return SuccessResponse(data=batch_import_result, msg="导入案例节点管理成功")

@ExampleSectionRouter.post('/download/template', summary="获取案例节点管理导入模板", description="获取案例节点管理导入模板", dependencies=[Depends(AuthPermission(["module_example:section:download"]))])
async def export_section_template_controller() -> StreamingResponse:
    """获取案例节点管理导入模板接口"""
    import_template_result = await ExampleSectionService.import_template_download_section_service()
    log.info('获取案例节点管理导入模板成功')
    return StreamResponse(
        data=bytes2file_response(import_template_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename=example_section_template.xlsx'}
    )