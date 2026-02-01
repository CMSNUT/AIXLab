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

from .service import TeamTest22Service
from .schema import TeamTest22CreateSchema, TeamTest22UpdateSchema, TeamTest22QueryParam

TeamTest22Router = APIRouter(route_class=OperationLogRoute, prefix='/test22', tags=["测试22模块"]) 

@TeamTest22Router.get("/detail/{id}", summary="获取测试22详情", description="获取测试22详情")
async def get_test22_detail_controller(
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_team:test22:query"]))
) -> JSONResponse:
    """获取测试22详情接口"""
    result_dict = await TeamTest22Service.detail_test22_service(auth=auth, id=id)
    log.info(f"获取测试22详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取测试22详情成功")

@TeamTest22Router.get("/list", summary="查询测试22列表", description="查询测试22列表")
async def get_test22_list_controller(
    page: PaginationQueryParam = Depends(),
    search: TeamTest22QueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_team:test22:query"]))
) -> JSONResponse:
    """查询测试22列表接口（数据库分页）"""
    result_dict = await TeamTest22Service.page_test22_service(
        auth=auth,
        page_no=page.page_no if page.page_no is not None else 1,
        page_size=page.page_size if page.page_size is not None else 10,
        search=search,
        order_by=page.order_by
    )
    log.info("查询测试22列表成功")
    return SuccessResponse(data=result_dict, msg="查询测试22列表成功")

@TeamTest22Router.post("/create", summary="创建测试22", description="创建测试22")
async def create_test22_controller(
    data: TeamTest22CreateSchema,
    auth: AuthSchema = Depends(AuthPermission(["module_team:test22:create"]))
) -> JSONResponse:
    """创建测试22接口"""
    result_dict = await TeamTest22Service.create_test22_service(auth=auth, data=data)
    log.info("创建测试22成功")
    return SuccessResponse(data=result_dict, msg="创建测试22成功")

@TeamTest22Router.put("/update/{id}", summary="修改测试22", description="修改测试22")
async def update_test22_controller(
    data: TeamTest22UpdateSchema,
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_team:test22:update"]))
) -> JSONResponse:
    """修改测试22接口"""
    result_dict = await TeamTest22Service.update_test22_service(auth=auth, id=id, data=data)
    log.info("修改测试22成功")
    return SuccessResponse(data=result_dict, msg="修改测试22成功")

@TeamTest22Router.delete("/delete", summary="删除测试22", description="删除测试22")
async def delete_test22_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_team:test22:delete"]))
) -> JSONResponse:
    """删除测试22接口"""
    await TeamTest22Service.delete_test22_service(auth=auth, ids=ids)
    log.info(f"删除测试22成功: {ids}")
    return SuccessResponse(msg="删除测试22成功")

@TeamTest22Router.patch("/available/setting", summary="批量修改测试22状态", description="批量修改测试22状态")
async def batch_set_available_test22_controller(
    data: BatchSetAvailable,
    auth: AuthSchema = Depends(AuthPermission(["module_team:test22:patch"]))
) -> JSONResponse:
    """批量修改测试22状态接口"""
    await TeamTest22Service.set_available_test22_service(auth=auth, data=data)
    log.info(f"批量修改测试22状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改测试22状态成功")

@TeamTest22Router.post('/export', summary="导出测试22", description="导出测试22")
async def export_test22_list_controller(
    search: TeamTest22QueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_team:test22:export"]))
) -> StreamingResponse:
    """导出测试22接口"""
    result_dict_list = await TeamTest22Service.list_test22_service(search=search, auth=auth)
    export_result = await TeamTest22Service.batch_export_test22_service(obj_list=result_dict_list)
    log.info('导出测试22成功')
    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            'Content-Disposition': 'attachment; filename=team_test22.xlsx'
        }
    )

@TeamTest22Router.post('/import', summary="导入测试22", description="导入测试22")
async def import_test22_list_controller(
    file: UploadFile,
    auth: AuthSchema = Depends(AuthPermission(["module_team:test22:import"]))
) -> JSONResponse:
    """导入测试22接口"""
    batch_import_result = await TeamTest22Service.batch_import_test22_service(file=file, auth=auth, update_support=True)
    log.info("导入测试22成功")
    return SuccessResponse(data=batch_import_result, msg="导入测试22成功")

@TeamTest22Router.post('/download/template', summary="获取测试22导入模板", description="获取测试22导入模板", dependencies=[Depends(AuthPermission(["module_team:test22:download"]))])
async def export_test22_template_controller() -> StreamingResponse:
    """获取测试22导入模板接口"""
    import_template_result = await TeamTest22Service.import_template_download_test22_service()
    log.info('获取测试22导入模板成功')
    return StreamResponse(
        data=bytes2file_response(import_template_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename=team_test22_template.xlsx'}
    )