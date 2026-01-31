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

from .service import ResourceCorpusService
from .schema import ResourceCorpusCreateSchema, ResourceCorpusUpdateSchema, ResourceCorpusQueryParam

ResourceCorpusRouter = APIRouter(route_class=OperationLogRoute, prefix='/corpus', tags=["语料模块"]) 

@ResourceCorpusRouter.get("/detail/{id}", summary="获取语料详情", description="获取语料详情")
async def get_corpus_detail_controller(
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_resource:corpus:query"]))
) -> JSONResponse:
    """获取语料详情接口"""
    result_dict = await ResourceCorpusService.detail_corpus_service(auth=auth, id=id)
    log.info(f"获取语料详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取语料详情成功")

@ResourceCorpusRouter.get("/list", summary="查询语料列表", description="查询语料列表")
async def get_corpus_list_controller(
    page: PaginationQueryParam = Depends(),
    search: ResourceCorpusQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_resource:corpus:query"]))
) -> JSONResponse:
    """查询语料列表接口（数据库分页）"""
    result_dict = await ResourceCorpusService.page_corpus_service(
        auth=auth,
        page_no=page.page_no if page.page_no is not None else 1,
        page_size=page.page_size if page.page_size is not None else 10,
        search=search,
        order_by=page.order_by
    )
    log.info("查询语料列表成功")
    return SuccessResponse(data=result_dict, msg="查询语料列表成功")

@ResourceCorpusRouter.post("/create", summary="创建语料", description="创建语料")
async def create_corpus_controller(
    data: ResourceCorpusCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(["module_resource:corpus:create"]))
) -> JSONResponse:
    """创建语料接口"""
    result_dict = await ResourceCorpusService.create_corpus_service(auth=auth, data=data)
    log.info("创建语料成功")
    return SuccessResponse(data=result_dict, msg="创建语料成功")

@ResourceCorpusRouter.put("/update/{id}", summary="修改语料", description="修改语料")
async def update_corpus_controller(
    data: ResourceCorpusUpdateSchema,
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_resource:corpus:update"]))
) -> JSONResponse:
    """修改语料接口"""
    result_dict = await ResourceCorpusService.update_corpus_service(auth=auth, id=id, data=data)
    log.info("修改语料成功")
    return SuccessResponse(data=result_dict, msg="修改语料成功")

@ResourceCorpusRouter.delete("/delete", summary="删除语料", description="删除语料")
async def delete_corpus_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_resource:corpus:delete"]))
) -> JSONResponse:
    """删除语料接口"""
    await ResourceCorpusService.delete_corpus_service(auth=auth, ids=ids)
    log.info(f"删除语料成功: {ids}")
    return SuccessResponse(msg="删除语料成功")

@ResourceCorpusRouter.patch("/available/setting", summary="批量修改语料状态", description="批量修改语料状态")
async def batch_set_available_corpus_controller(
    data: BatchSetAvailable,
    auth: AuthSchema = Depends(AuthPermission(["module_resource:corpus:patch"]))
) -> JSONResponse:
    """批量修改语料状态接口"""
    await ResourceCorpusService.set_available_corpus_service(auth=auth, data=data)
    log.info(f"批量修改语料状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改语料状态成功")

@ResourceCorpusRouter.post('/export', summary="导出语料", description="导出语料")
async def export_corpus_list_controller(
    search: ResourceCorpusQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_resource:corpus:export"]))
) -> StreamingResponse:
    """导出语料接口"""
    result_dict_list = await ResourceCorpusService.list_corpus_service(search=search, auth=auth)
    export_result = await ResourceCorpusService.batch_export_corpus_service(obj_list=result_dict_list)
    log.info('导出语料成功')
    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            'Content-Disposition': 'attachment; filename=resource_corpus.xlsx'
        }
    )

@ResourceCorpusRouter.post('/import', summary="导入语料", description="导入语料")
async def import_corpus_list_controller(
    file: UploadFile,
    auth: AuthSchema = Depends(AuthPermission(["module_resource:corpus:import"]))
) -> JSONResponse:
    """导入语料接口"""
    batch_import_result = await ResourceCorpusService.batch_import_corpus_service(file=file, auth=auth, update_support=True)
    log.info("导入语料成功")
    return SuccessResponse(data=batch_import_result, msg="导入语料成功")

@ResourceCorpusRouter.post('/download/template', summary="获取语料导入模板", description="获取语料导入模板", dependencies=[Depends(AuthPermission(["module_resource:corpus:download"]))])
async def export_corpus_template_controller() -> StreamingResponse:
    """获取语料导入模板接口"""
    import_template_result = await ResourceCorpusService.import_template_download_corpus_service()
    log.info('获取语料导入模板成功')
    return StreamResponse(
        data=bytes2file_response(import_template_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename=resource_corpus_template.xlsx'}
    )