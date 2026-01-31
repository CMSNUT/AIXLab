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

from .service import ResourcePaperService
from .schema import ResourcePaperCreateSchema, ResourcePaperUpdateSchema, ResourcePaperQueryParam

ResourcePaperRouter = APIRouter(route_class=OperationLogRoute, prefix='/paper', tags=["文献模块"]) 

@ResourcePaperRouter.get("/detail/{id}", summary="获取文献详情", description="获取文献详情")
async def get_paper_detail_controller(
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_resource:paper:query"]))
) -> JSONResponse:
    """获取文献详情接口"""
    result_dict = await ResourcePaperService.detail_paper_service(auth=auth, id=id)
    log.info(f"获取文献详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取文献详情成功")

@ResourcePaperRouter.get("/list", summary="查询文献列表", description="查询文献列表")
async def get_paper_list_controller(
    page: PaginationQueryParam = Depends(),
    search: ResourcePaperQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_resource:paper:query"]))
) -> JSONResponse:
    """查询文献列表接口（数据库分页）"""
    result_dict = await ResourcePaperService.page_paper_service(
        auth=auth,
        page_no=page.page_no if page.page_no is not None else 1,
        page_size=page.page_size if page.page_size is not None else 10,
        search=search,
        order_by=page.order_by
    )
    log.info("查询文献列表成功")
    return SuccessResponse(data=result_dict, msg="查询文献列表成功")

@ResourcePaperRouter.post("/create", summary="创建文献", description="创建文献")
async def create_paper_controller(
    data: ResourcePaperCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(["module_resource:paper:create"]))
) -> JSONResponse:
    """创建文献接口"""
    result_dict = await ResourcePaperService.create_paper_service(auth=auth, data=data)
    log.info("创建文献成功")
    return SuccessResponse(data=result_dict, msg="创建文献成功")

@ResourcePaperRouter.put("/update/{id}", summary="修改文献", description="修改文献")
async def update_paper_controller(
    data: ResourcePaperUpdateSchema,
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_resource:paper:update"]))
) -> JSONResponse:
    """修改文献接口"""
    result_dict = await ResourcePaperService.update_paper_service(auth=auth, id=id, data=data)
    log.info("修改文献成功")
    return SuccessResponse(data=result_dict, msg="修改文献成功")

@ResourcePaperRouter.delete("/delete", summary="删除文献", description="删除文献")
async def delete_paper_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_resource:paper:delete"]))
) -> JSONResponse:
    """删除文献接口"""
    await ResourcePaperService.delete_paper_service(auth=auth, ids=ids)
    log.info(f"删除文献成功: {ids}")
    return SuccessResponse(msg="删除文献成功")

@ResourcePaperRouter.patch("/available/setting", summary="批量修改文献状态", description="批量修改文献状态")
async def batch_set_available_paper_controller(
    data: BatchSetAvailable,
    auth: AuthSchema = Depends(AuthPermission(["module_resource:paper:patch"]))
) -> JSONResponse:
    """批量修改文献状态接口"""
    await ResourcePaperService.set_available_paper_service(auth=auth, data=data)
    log.info(f"批量修改文献状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改文献状态成功")

@ResourcePaperRouter.post('/export', summary="导出文献", description="导出文献")
async def export_paper_list_controller(
    search: ResourcePaperQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_resource:paper:export"]))
) -> StreamingResponse:
    """导出文献接口"""
    result_dict_list = await ResourcePaperService.list_paper_service(search=search, auth=auth)
    export_result = await ResourcePaperService.batch_export_paper_service(obj_list=result_dict_list)
    log.info('导出文献成功')
    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            'Content-Disposition': 'attachment; filename=resource_paper.xlsx'
        }
    )

@ResourcePaperRouter.post('/import', summary="导入文献", description="导入文献")
async def import_paper_list_controller(
    file: UploadFile,
    auth: AuthSchema = Depends(AuthPermission(["module_resource:paper:import"]))
) -> JSONResponse:
    """导入文献接口"""
    batch_import_result = await ResourcePaperService.batch_import_paper_service(file=file, auth=auth, update_support=True)
    log.info("导入文献成功")
    return SuccessResponse(data=batch_import_result, msg="导入文献成功")

@ResourcePaperRouter.post('/download/template', summary="获取文献导入模板", description="获取文献导入模板", dependencies=[Depends(AuthPermission(["module_resource:paper:download"]))])
async def export_paper_template_controller() -> StreamingResponse:
    """获取文献导入模板接口"""
    import_template_result = await ResourcePaperService.import_template_download_paper_service()
    log.info('获取文献导入模板成功')
    return StreamResponse(
        data=bytes2file_response(import_template_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename=resource_paper_template.xlsx'}
    )