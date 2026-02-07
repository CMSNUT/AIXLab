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

from .service import RepoProgramService
from .schema import RepoProgramCreateSchema, RepoProgramUpdateSchema, RepoProgramQueryParam

RepoProgramRouter = APIRouter(route_class=OperationLogRoute, prefix='/program', tags=["代码仓库管理模块"]) 

@RepoProgramRouter.get("/detail/{id}", summary="获取代码仓库管理详情", description="获取代码仓库管理详情")
async def get_program_detail_controller(
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_repo:program:query"]))
) -> JSONResponse:
    """获取代码仓库管理详情接口"""
    result_dict = await RepoProgramService.detail_program_service(auth=auth, id=id)
    log.info(f"获取代码仓库管理详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取代码仓库管理详情成功")

@RepoProgramRouter.get("/list", summary="查询代码仓库管理列表", description="查询代码仓库管理列表")
async def get_program_list_controller(
    page: PaginationQueryParam = Depends(),
    search: RepoProgramQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_repo:program:query"]))
) -> JSONResponse:
    """查询代码仓库管理列表接口（数据库分页）"""
    result_dict = await RepoProgramService.page_program_service(
        auth=auth,
        page_no=page.page_no if page.page_no is not None else 1,
        page_size=page.page_size if page.page_size is not None else 10,
        search=search,
        order_by=page.order_by
    )
    log.info("查询代码仓库管理列表成功")
    return SuccessResponse(data=result_dict, msg="查询代码仓库管理列表成功")

@RepoProgramRouter.post("/create", summary="创建代码仓库管理", description="创建代码仓库管理")
async def create_program_controller(
    data: RepoProgramCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(["module_repo:program:create"]))
) -> JSONResponse:
    """创建代码仓库管理接口"""
    result_dict = await RepoProgramService.create_program_service(auth=auth, data=data)
    log.info("创建代码仓库管理成功")
    return SuccessResponse(data=result_dict, msg="创建代码仓库管理成功")

@RepoProgramRouter.put("/update/{id}", summary="修改代码仓库管理", description="修改代码仓库管理")
async def update_program_controller(
    data: RepoProgramUpdateSchema,
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_repo:program:update"]))
) -> JSONResponse:
    """修改代码仓库管理接口"""
    result_dict = await RepoProgramService.update_program_service(auth=auth, id=id, data=data)
    log.info("修改代码仓库管理成功")
    return SuccessResponse(data=result_dict, msg="修改代码仓库管理成功")

@RepoProgramRouter.delete("/delete", summary="删除代码仓库管理", description="删除代码仓库管理")
async def delete_program_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_repo:program:delete"]))
) -> JSONResponse:
    """删除代码仓库管理接口"""
    await RepoProgramService.delete_program_service(auth=auth, ids=ids)
    log.info(f"删除代码仓库管理成功: {ids}")
    return SuccessResponse(msg="删除代码仓库管理成功")

@RepoProgramRouter.patch("/available/setting", summary="批量修改代码仓库管理状态", description="批量修改代码仓库管理状态")
async def batch_set_available_program_controller(
    data: BatchSetAvailable,
    auth: AuthSchema = Depends(AuthPermission(["module_repo:program:patch"]))
) -> JSONResponse:
    """批量修改代码仓库管理状态接口"""
    await RepoProgramService.set_available_program_service(auth=auth, data=data)
    log.info(f"批量修改代码仓库管理状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改代码仓库管理状态成功")

@RepoProgramRouter.post('/export', summary="导出代码仓库管理", description="导出代码仓库管理")
async def export_program_list_controller(
    search: RepoProgramQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_repo:program:export"]))
) -> StreamingResponse:
    """导出代码仓库管理接口"""
    result_dict_list = await RepoProgramService.list_program_service(search=search, auth=auth)
    export_result = await RepoProgramService.batch_export_program_service(obj_list=result_dict_list)
    log.info('导出代码仓库管理成功')
    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            'Content-Disposition': 'attachment; filename=repo_program.xlsx'
        }
    )

@RepoProgramRouter.post('/import', summary="导入代码仓库管理", description="导入代码仓库管理")
async def import_program_list_controller(
    file: UploadFile,
    auth: AuthSchema = Depends(AuthPermission(["module_repo:program:import"]))
) -> JSONResponse:
    """导入代码仓库管理接口"""
    batch_import_result = await RepoProgramService.batch_import_program_service(file=file, auth=auth, update_support=True)
    log.info("导入代码仓库管理成功")
    return SuccessResponse(data=batch_import_result, msg="导入代码仓库管理成功")

@RepoProgramRouter.post('/download/template', summary="获取代码仓库管理导入模板", description="获取代码仓库管理导入模板", dependencies=[Depends(AuthPermission(["module_repo:program:download"]))])
async def export_program_template_controller() -> StreamingResponse:
    """获取代码仓库管理导入模板接口"""
    import_template_result = await RepoProgramService.import_template_download_program_service()
    log.info('获取代码仓库管理导入模板成功')
    return StreamResponse(
        data=bytes2file_response(import_template_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename=repo_program_template.xlsx'}
    )