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

from .service import RepoDatasetService
from .schema import RepoDatasetCreateSchema, RepoDatasetUpdateSchema, RepoDatasetQueryParam

RepoDatasetRouter = APIRouter(route_class=OperationLogRoute, prefix='/dataset', tags=["数据仓库管理模块"]) 

@RepoDatasetRouter.get("/detail/{id}", summary="获取数据仓库管理详情", description="获取数据仓库管理详情")
async def get_dataset_detail_controller(
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_repo:dataset:query"]))
) -> JSONResponse:
    """获取数据仓库管理详情接口"""
    result_dict = await RepoDatasetService.detail_dataset_service(auth=auth, id=id)
    log.info(f"获取数据仓库管理详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取数据仓库管理详情成功")

@RepoDatasetRouter.get("/list", summary="查询数据仓库管理列表", description="查询数据仓库管理列表")
async def get_dataset_list_controller(
    page: PaginationQueryParam = Depends(),
    search: RepoDatasetQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_repo:dataset:query"]))
) -> JSONResponse:
    """查询数据仓库管理列表接口（数据库分页）"""
    result_dict = await RepoDatasetService.page_dataset_service(
        auth=auth,
        page_no=page.page_no if page.page_no is not None else 1,
        page_size=page.page_size if page.page_size is not None else 10,
        search=search,
        order_by=page.order_by
    )
    log.info("查询数据仓库管理列表成功")
    return SuccessResponse(data=result_dict, msg="查询数据仓库管理列表成功")

@RepoDatasetRouter.post("/create", summary="创建数据仓库管理", description="创建数据仓库管理")
async def create_dataset_controller(
    data: RepoDatasetCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(["module_repo:dataset:create"]))
) -> JSONResponse:
    """创建数据仓库管理接口"""
    result_dict = await RepoDatasetService.create_dataset_service(auth=auth, data=data)
    log.info("创建数据仓库管理成功")
    return SuccessResponse(data=result_dict, msg="创建数据仓库管理成功")

@RepoDatasetRouter.put("/update/{id}", summary="修改数据仓库管理", description="修改数据仓库管理")
async def update_dataset_controller(
    data: RepoDatasetUpdateSchema,
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_repo:dataset:update"]))
) -> JSONResponse:
    """修改数据仓库管理接口"""
    result_dict = await RepoDatasetService.update_dataset_service(auth=auth, id=id, data=data)
    log.info("修改数据仓库管理成功")
    return SuccessResponse(data=result_dict, msg="修改数据仓库管理成功")

@RepoDatasetRouter.delete("/delete", summary="删除数据仓库管理", description="删除数据仓库管理")
async def delete_dataset_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_repo:dataset:delete"]))
) -> JSONResponse:
    """删除数据仓库管理接口"""
    await RepoDatasetService.delete_dataset_service(auth=auth, ids=ids)
    log.info(f"删除数据仓库管理成功: {ids}")
    return SuccessResponse(msg="删除数据仓库管理成功")

@RepoDatasetRouter.patch("/available/setting", summary="批量修改数据仓库管理状态", description="批量修改数据仓库管理状态")
async def batch_set_available_dataset_controller(
    data: BatchSetAvailable,
    auth: AuthSchema = Depends(AuthPermission(["module_repo:dataset:patch"]))
) -> JSONResponse:
    """批量修改数据仓库管理状态接口"""
    await RepoDatasetService.set_available_dataset_service(auth=auth, data=data)
    log.info(f"批量修改数据仓库管理状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改数据仓库管理状态成功")

@RepoDatasetRouter.post('/export', summary="导出数据仓库管理", description="导出数据仓库管理")
async def export_dataset_list_controller(
    search: RepoDatasetQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_repo:dataset:export"]))
) -> StreamingResponse:
    """导出数据仓库管理接口"""
    result_dict_list = await RepoDatasetService.list_dataset_service(search=search, auth=auth)
    export_result = await RepoDatasetService.batch_export_dataset_service(obj_list=result_dict_list)
    log.info('导出数据仓库管理成功')
    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            'Content-Disposition': 'attachment; filename=repo_dataset.xlsx'
        }
    )

@RepoDatasetRouter.post('/import', summary="导入数据仓库管理", description="导入数据仓库管理")
async def import_dataset_list_controller(
    file: UploadFile,
    auth: AuthSchema = Depends(AuthPermission(["module_repo:dataset:import"]))
) -> JSONResponse:
    """导入数据仓库管理接口"""
    batch_import_result = await RepoDatasetService.batch_import_dataset_service(file=file, auth=auth, update_support=True)
    log.info("导入数据仓库管理成功")
    return SuccessResponse(data=batch_import_result, msg="导入数据仓库管理成功")

@RepoDatasetRouter.post('/download/template', summary="获取数据仓库管理导入模板", description="获取数据仓库管理导入模板", dependencies=[Depends(AuthPermission(["module_repo:dataset:download"]))])
async def export_dataset_template_controller() -> StreamingResponse:
    """获取数据仓库管理导入模板接口"""
    import_template_result = await RepoDatasetService.import_template_download_dataset_service()
    log.info('获取数据仓库管理导入模板成功')
    return StreamResponse(
        data=bytes2file_response(import_template_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename=repo_dataset_template.xlsx'}
    )