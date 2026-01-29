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

from .service import RscLiteratureService
from .schema import RscLiteratureCreateSchema, RscLiteratureUpdateSchema, RscLiteratureQueryParam

RscLiteratureRouter = APIRouter(route_class=OperationLogRoute, prefix='/literature', tags=["文献管理模块"]) 

@RscLiteratureRouter.get("/detail/{id}", summary="获取文献管理详情", description="获取文献管理详情")
async def get_literature_detail_controller(
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_rsc:literature:query"]))
) -> JSONResponse:
    """获取文献管理详情接口"""
    result_dict = await RscLiteratureService.detail_literature_service(auth=auth, id=id)
    log.info(f"获取文献管理详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取文献管理详情成功")

@RscLiteratureRouter.get("/list", summary="查询文献管理列表", description="查询文献管理列表")
async def get_literature_list_controller(
    page: PaginationQueryParam = Depends(),
    search: RscLiteratureQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_rsc:literature:query"]))
) -> JSONResponse:
    """查询文献管理列表接口（数据库分页）"""
    result_dict = await RscLiteratureService.page_literature_service(
        auth=auth,
        page_no=page.page_no if page.page_no is not None else 1,
        page_size=page.page_size if page.page_size is not None else 10,
        search=search,
        order_by=page.order_by
    )
    log.info("查询文献管理列表成功")
    return SuccessResponse(data=result_dict, msg="查询文献管理列表成功")

@RscLiteratureRouter.post("/create", summary="创建文献管理", description="创建文献管理")
async def create_literature_controller(
    data: RscLiteratureCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(["module_rsc:literature:create"]))
) -> JSONResponse:
    """创建文献管理接口"""
    result_dict = await RscLiteratureService.create_literature_service(auth=auth, data=data)
    log.info("创建文献管理成功")
    return SuccessResponse(data=result_dict, msg="创建文献管理成功")

@RscLiteratureRouter.put("/update/{id}", summary="修改文献管理", description="修改文献管理")
async def update_literature_controller(
    data: RscLiteratureUpdateSchema,
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_rsc:literature:update"]))
) -> JSONResponse:
    """修改文献管理接口"""
    result_dict = await RscLiteratureService.update_literature_service(auth=auth, id=id, data=data)
    log.info("修改文献管理成功")
    return SuccessResponse(data=result_dict, msg="修改文献管理成功")

@RscLiteratureRouter.delete("/delete", summary="删除文献管理", description="删除文献管理")
async def delete_literature_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_rsc:literature:delete"]))
) -> JSONResponse:
    """删除文献管理接口"""
    await RscLiteratureService.delete_literature_service(auth=auth, ids=ids)
    log.info(f"删除文献管理成功: {ids}")
    return SuccessResponse(msg="删除文献管理成功")

@RscLiteratureRouter.patch("/available/setting", summary="批量修改文献管理状态", description="批量修改文献管理状态")
async def batch_set_available_literature_controller(
    data: BatchSetAvailable,
    auth: AuthSchema = Depends(AuthPermission(["module_rsc:literature:patch"]))
) -> JSONResponse:
    """批量修改文献管理状态接口"""
    await RscLiteratureService.set_available_literature_service(auth=auth, data=data)
    log.info(f"批量修改文献管理状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改文献管理状态成功")

@RscLiteratureRouter.post('/export', summary="导出文献管理", description="导出文献管理")
async def export_literature_list_controller(
    search: RscLiteratureQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_rsc:literature:export"]))
) -> StreamingResponse:
    """导出文献管理接口"""
    result_dict_list = await RscLiteratureService.list_literature_service(search=search, auth=auth)
    export_result = await RscLiteratureService.batch_export_literature_service(obj_list=result_dict_list)
    log.info('导出文献管理成功')
    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            'Content-Disposition': 'attachment; filename=rsc_literature.xlsx'
        }
    )

@RscLiteratureRouter.post('/import', summary="导入文献管理", description="导入文献管理")
async def import_literature_list_controller(
    file: UploadFile,
    auth: AuthSchema = Depends(AuthPermission(["module_rsc:literature:import"]))
) -> JSONResponse:
    """导入文献管理接口"""
    batch_import_result = await RscLiteratureService.batch_import_literature_service(file=file, auth=auth, update_support=True)
    log.info("导入文献管理成功")
    return SuccessResponse(data=batch_import_result, msg="导入文献管理成功")

@RscLiteratureRouter.post('/download/template', summary="获取文献管理导入模板", description="获取文献管理导入模板", dependencies=[Depends(AuthPermission(["module_rsc:literature:download"]))])
async def export_literature_template_controller() -> StreamingResponse:
    """获取文献管理导入模板接口"""
    import_template_result = await RscLiteratureService.import_template_download_literature_service()
    log.info('获取文献管理导入模板成功')
    return StreamResponse(
        data=bytes2file_response(import_template_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename=rsc_literature_template.xlsx'}
    )