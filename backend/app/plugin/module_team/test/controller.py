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

from .service import TeamTestService
from .schema import TeamTestCreateSchema, TeamTestUpdateSchema, TeamTestQueryParam

TeamTestRouter = APIRouter(route_class=OperationLogRoute, prefix='/test', tags=["团队测试模块"]) 

@TeamTestRouter.get("/detail/{id}", summary="获取团队测试详情", description="获取团队测试详情")
async def get_test_detail_controller(
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_team:test:query"]))
) -> JSONResponse:
    """获取团队测试详情接口"""
    result_dict = await TeamTestService.detail_test_service(auth=auth, id=id)
    log.info(f"获取团队测试详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取团队测试详情成功")

@TeamTestRouter.get("/list", summary="查询团队测试列表", description="查询团队测试列表")
async def get_test_list_controller(
    page: PaginationQueryParam = Depends(),
    search: TeamTestQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_team:test:query"]))
) -> JSONResponse:
    """查询团队测试列表接口（数据库分页）"""
    result_dict = await TeamTestService.page_test_service(
        auth=auth,
        page_no=page.page_no if page.page_no is not None else 1,
        page_size=page.page_size if page.page_size is not None else 10,
        search=search,
        order_by=page.order_by
    )
    log.info("查询团队测试列表成功")
    return SuccessResponse(data=result_dict, msg="查询团队测试列表成功")

@TeamTestRouter.post("/create", summary="创建团队测试", description="创建团队测试")
async def create_test_controller(
    data: TeamTestCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(["module_team:test:create"]))
) -> JSONResponse:
    """创建团队测试接口"""
    result_dict = await TeamTestService.create_test_service(auth=auth, data=data)
    log.info("创建团队测试成功")
    return SuccessResponse(data=result_dict, msg="创建团队测试成功")

@TeamTestRouter.put("/update/{id}", summary="修改团队测试", description="修改团队测试")
async def update_test_controller(
    data: TeamTestUpdateSchema,
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_team:test:update"]))
) -> JSONResponse:
    """修改团队测试接口"""
    result_dict = await TeamTestService.update_test_service(auth=auth, id=id, data=data)
    log.info("修改团队测试成功")
    return SuccessResponse(data=result_dict, msg="修改团队测试成功")

@TeamTestRouter.delete("/delete", summary="删除团队测试", description="删除团队测试")
async def delete_test_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_team:test:delete"]))
) -> JSONResponse:
    """删除团队测试接口"""
    await TeamTestService.delete_test_service(auth=auth, ids=ids)
    log.info(f"删除团队测试成功: {ids}")
    return SuccessResponse(msg="删除团队测试成功")

@TeamTestRouter.patch("/available/setting", summary="批量修改团队测试状态", description="批量修改团队测试状态")
async def batch_set_available_test_controller(
    data: BatchSetAvailable,
    auth: AuthSchema = Depends(AuthPermission(["module_team:test:patch"]))
) -> JSONResponse:
    """批量修改团队测试状态接口"""
    await TeamTestService.set_available_test_service(auth=auth, data=data)
    log.info(f"批量修改团队测试状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改团队测试状态成功")

@TeamTestRouter.post('/export', summary="导出团队测试", description="导出团队测试")
async def export_test_list_controller(
    search: TeamTestQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_team:test:export"]))
) -> StreamingResponse:
    """导出团队测试接口"""
    result_dict_list = await TeamTestService.list_test_service(search=search, auth=auth)
    export_result = await TeamTestService.batch_export_test_service(obj_list=result_dict_list)
    log.info('导出团队测试成功')
    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            'Content-Disposition': 'attachment; filename=team_test.xlsx'
        }
    )

@TeamTestRouter.post('/import', summary="导入团队测试", description="导入团队测试")
async def import_test_list_controller(
    file: UploadFile,
    auth: AuthSchema = Depends(AuthPermission(["module_team:test:import"]))
) -> JSONResponse:
    """导入团队测试接口"""
    batch_import_result = await TeamTestService.batch_import_test_service(file=file, auth=auth, update_support=True)
    log.info("导入团队测试成功")
    return SuccessResponse(data=batch_import_result, msg="导入团队测试成功")

@TeamTestRouter.post('/download/template', summary="获取团队测试导入模板", description="获取团队测试导入模板", dependencies=[Depends(AuthPermission(["module_team:test:download"]))])
async def export_test_template_controller() -> StreamingResponse:
    """获取团队测试导入模板接口"""
    import_template_result = await TeamTestService.import_template_download_test_service()
    log.info('获取团队测试导入模板成功')
    return StreamResponse(
        data=bytes2file_response(import_template_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename=team_test_template.xlsx'}
    )