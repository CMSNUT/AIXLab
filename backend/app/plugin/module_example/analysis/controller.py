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

from .service import ExampleAnalysisService
from .schema import ExampleAnalysisCreateSchema, ExampleAnalysisUpdateSchema, ExampleAnalysisQueryParam

ExampleAnalysisRouter = APIRouter(route_class=OperationLogRoute, prefix='/analysis', tags=["案例分析管理模块"]) 

@ExampleAnalysisRouter.get("/detail/{id}", summary="获取案例分析管理详情", description="获取案例分析管理详情")
async def get_analysis_detail_controller(
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_example:analysis:query"]))
) -> JSONResponse:
    """获取案例分析管理详情接口"""
    result_dict = await ExampleAnalysisService.detail_analysis_service(auth=auth, id=id)
    log.info(f"获取案例分析管理详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取案例分析管理详情成功")

@ExampleAnalysisRouter.get("/list", summary="查询案例分析管理列表", description="查询案例分析管理列表")
async def get_analysis_list_controller(
    page: PaginationQueryParam = Depends(),
    search: ExampleAnalysisQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_example:analysis:query"]))
) -> JSONResponse:
    """查询案例分析管理列表接口（数据库分页）"""
    result_dict = await ExampleAnalysisService.page_analysis_service(
        auth=auth,
        page_no=page.page_no if page.page_no is not None else 1,
        page_size=page.page_size if page.page_size is not None else 10,
        search=search,
        order_by=page.order_by
    )
    log.info("查询案例分析管理列表成功")
    return SuccessResponse(data=result_dict, msg="查询案例分析管理列表成功")

@ExampleAnalysisRouter.post("/create", summary="创建案例分析管理", description="创建案例分析管理")
async def create_analysis_controller(
    data: ExampleAnalysisCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(["module_example:analysis:create"]))
) -> JSONResponse:
    """创建案例分析管理接口"""
    result_dict = await ExampleAnalysisService.create_analysis_service(auth=auth, data=data)
    log.info("创建案例分析管理成功")
    return SuccessResponse(data=result_dict, msg="创建案例分析管理成功")

@ExampleAnalysisRouter.put("/update/{id}", summary="修改案例分析管理", description="修改案例分析管理")
async def update_analysis_controller(
    data: ExampleAnalysisUpdateSchema,
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_example:analysis:update"]))
) -> JSONResponse:
    """修改案例分析管理接口"""
    result_dict = await ExampleAnalysisService.update_analysis_service(auth=auth, id=id, data=data)
    log.info("修改案例分析管理成功")
    return SuccessResponse(data=result_dict, msg="修改案例分析管理成功")

@ExampleAnalysisRouter.delete("/delete", summary="删除案例分析管理", description="删除案例分析管理")
async def delete_analysis_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_example:analysis:delete"]))
) -> JSONResponse:
    """删除案例分析管理接口"""
    await ExampleAnalysisService.delete_analysis_service(auth=auth, ids=ids)
    log.info(f"删除案例分析管理成功: {ids}")
    return SuccessResponse(msg="删除案例分析管理成功")

@ExampleAnalysisRouter.patch("/available/setting", summary="批量修改案例分析管理状态", description="批量修改案例分析管理状态")
async def batch_set_available_analysis_controller(
    data: BatchSetAvailable,
    auth: AuthSchema = Depends(AuthPermission(["module_example:analysis:patch"]))
) -> JSONResponse:
    """批量修改案例分析管理状态接口"""
    await ExampleAnalysisService.set_available_analysis_service(auth=auth, data=data)
    log.info(f"批量修改案例分析管理状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改案例分析管理状态成功")

@ExampleAnalysisRouter.post('/export', summary="导出案例分析管理", description="导出案例分析管理")
async def export_analysis_list_controller(
    search: ExampleAnalysisQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_example:analysis:export"]))
) -> StreamingResponse:
    """导出案例分析管理接口"""
    result_dict_list = await ExampleAnalysisService.list_analysis_service(search=search, auth=auth)
    export_result = await ExampleAnalysisService.batch_export_analysis_service(obj_list=result_dict_list)
    log.info('导出案例分析管理成功')
    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            'Content-Disposition': 'attachment; filename=example_analysis.xlsx'
        }
    )

@ExampleAnalysisRouter.post('/import', summary="导入案例分析管理", description="导入案例分析管理")
async def import_analysis_list_controller(
    file: UploadFile,
    auth: AuthSchema = Depends(AuthPermission(["module_example:analysis:import"]))
) -> JSONResponse:
    """导入案例分析管理接口"""
    batch_import_result = await ExampleAnalysisService.batch_import_analysis_service(file=file, auth=auth, update_support=True)
    log.info("导入案例分析管理成功")
    return SuccessResponse(data=batch_import_result, msg="导入案例分析管理成功")

@ExampleAnalysisRouter.post('/download/template', summary="获取案例分析管理导入模板", description="获取案例分析管理导入模板", dependencies=[Depends(AuthPermission(["module_example:analysis:download"]))])
async def export_analysis_template_controller() -> StreamingResponse:
    """获取案例分析管理导入模板接口"""
    import_template_result = await ExampleAnalysisService.import_template_download_analysis_service()
    log.info('获取案例分析管理导入模板成功')
    return StreamResponse(
        data=bytes2file_response(import_template_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename=example_analysis_template.xlsx'}
    )