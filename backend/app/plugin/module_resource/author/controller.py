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

from .service import ResourceAuthorService
from .schema import ResourceAuthorCreateSchema, ResourceAuthorUpdateSchema, ResourceAuthorQueryParam

ResourceAuthorRouter = APIRouter(route_class=OperationLogRoute, prefix='/author', tags=["作者模块"]) 

@ResourceAuthorRouter.get("/detail/{id}", summary="获取作者详情", description="获取作者详情")
async def get_author_detail_controller(
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_resource:author:query"]))
) -> JSONResponse:
    """获取作者详情接口"""
    result_dict = await ResourceAuthorService.detail_author_service(auth=auth, id=id)
    log.info(f"获取作者详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取作者详情成功")

@ResourceAuthorRouter.get("/list", summary="查询作者列表", description="查询作者列表")
async def get_author_list_controller(
    page: PaginationQueryParam = Depends(),
    search: ResourceAuthorQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_resource:author:query"]))
) -> JSONResponse:
    """查询作者列表接口（数据库分页）"""
    result_dict = await ResourceAuthorService.page_author_service(
        auth=auth,
        page_no=page.page_no if page.page_no is not None else 1,
        page_size=page.page_size if page.page_size is not None else 10,
        search=search,
        order_by=page.order_by
    )
    log.info("查询作者列表成功")
    return SuccessResponse(data=result_dict, msg="查询作者列表成功")

@ResourceAuthorRouter.post("/create", summary="创建作者", description="创建作者")
async def create_author_controller(
    data: ResourceAuthorCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(["module_resource:author:create"]))
) -> JSONResponse:
    """创建作者接口"""
    result_dict = await ResourceAuthorService.create_author_service(auth=auth, data=data)
    log.info("创建作者成功")
    return SuccessResponse(data=result_dict, msg="创建作者成功")

@ResourceAuthorRouter.put("/update/{id}", summary="修改作者", description="修改作者")
async def update_author_controller(
    data: ResourceAuthorUpdateSchema,
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_resource:author:update"]))
) -> JSONResponse:
    """修改作者接口"""
    result_dict = await ResourceAuthorService.update_author_service(auth=auth, id=id, data=data)
    log.info("修改作者成功")
    return SuccessResponse(data=result_dict, msg="修改作者成功")

@ResourceAuthorRouter.delete("/delete", summary="删除作者", description="删除作者")
async def delete_author_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_resource:author:delete"]))
) -> JSONResponse:
    """删除作者接口"""
    await ResourceAuthorService.delete_author_service(auth=auth, ids=ids)
    log.info(f"删除作者成功: {ids}")
    return SuccessResponse(msg="删除作者成功")

@ResourceAuthorRouter.patch("/available/setting", summary="批量修改作者状态", description="批量修改作者状态")
async def batch_set_available_author_controller(
    data: BatchSetAvailable,
    auth: AuthSchema = Depends(AuthPermission(["module_resource:author:patch"]))
) -> JSONResponse:
    """批量修改作者状态接口"""
    await ResourceAuthorService.set_available_author_service(auth=auth, data=data)
    log.info(f"批量修改作者状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改作者状态成功")

@ResourceAuthorRouter.post('/export', summary="导出作者", description="导出作者")
async def export_author_list_controller(
    search: ResourceAuthorQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_resource:author:export"]))
) -> StreamingResponse:
    """导出作者接口"""
    result_dict_list = await ResourceAuthorService.list_author_service(search=search, auth=auth)
    export_result = await ResourceAuthorService.batch_export_author_service(obj_list=result_dict_list)
    log.info('导出作者成功')
    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            'Content-Disposition': 'attachment; filename=resource_author.xlsx'
        }
    )

@ResourceAuthorRouter.post('/import', summary="导入作者", description="导入作者")
async def import_author_list_controller(
    file: UploadFile,
    auth: AuthSchema = Depends(AuthPermission(["module_resource:author:import"]))
) -> JSONResponse:
    """导入作者接口"""
    batch_import_result = await ResourceAuthorService.batch_import_author_service(file=file, auth=auth, update_support=True)
    log.info("导入作者成功")
    return SuccessResponse(data=batch_import_result, msg="导入作者成功")

@ResourceAuthorRouter.post('/download/template', summary="获取作者导入模板", description="获取作者导入模板", dependencies=[Depends(AuthPermission(["module_resource:author:download"]))])
async def export_author_template_controller() -> StreamingResponse:
    """获取作者导入模板接口"""
    import_template_result = await ResourceAuthorService.import_template_download_author_service()
    log.info('获取作者导入模板成功')
    return StreamResponse(
        data=bytes2file_response(import_template_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename=resource_author_template.xlsx'}
    )