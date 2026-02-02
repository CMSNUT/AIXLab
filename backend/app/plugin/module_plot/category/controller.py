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

from .service import PlotCategoryService
from .schema import PlotCategoryCreateSchema, PlotCategoryUpdateSchema, PlotCategoryQueryParam

PlotCategoryRouter = APIRouter(route_class=OperationLogRoute, prefix='/category', tags=["绘图模块管理模块"]) 

@PlotCategoryRouter.get("/detail/{id}", summary="获取绘图模块管理详情", description="获取绘图模块管理详情")
async def get_category_detail_controller(
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_plot:category:query"]))
) -> JSONResponse:
    """获取绘图模块管理详情接口"""
    result_dict = await PlotCategoryService.detail_category_service(auth=auth, id=id)
    log.info(f"获取绘图模块管理详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取绘图模块管理详情成功")

@PlotCategoryRouter.get("/list", summary="查询绘图模块管理列表", description="查询绘图模块管理列表")
async def get_category_list_controller(
    page: PaginationQueryParam = Depends(),
    search: PlotCategoryQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_plot:category:query"]))
) -> JSONResponse:
    """查询绘图模块管理列表接口（数据库分页）"""
    result_dict = await PlotCategoryService.page_category_service(
        auth=auth,
        page_no=page.page_no if page.page_no is not None else 1,
        page_size=page.page_size if page.page_size is not None else 10,
        search=search,
        order_by=page.order_by
    )
    log.info("查询绘图模块管理列表成功")
    return SuccessResponse(data=result_dict, msg="查询绘图模块管理列表成功")

@PlotCategoryRouter.post("/create", summary="创建绘图模块管理", description="创建绘图模块管理")
async def create_category_controller(
    data: PlotCategoryCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(["module_plot:category:create"]))
) -> JSONResponse:
    """创建绘图模块管理接口"""
    result_dict = await PlotCategoryService.create_category_service(auth=auth, data=data)
    log.info("创建绘图模块管理成功")
    return SuccessResponse(data=result_dict, msg="创建绘图模块管理成功")

@PlotCategoryRouter.put("/update/{id}", summary="修改绘图模块管理", description="修改绘图模块管理")
async def update_category_controller(
    data: PlotCategoryUpdateSchema,
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_plot:category:update"]))
) -> JSONResponse:
    """修改绘图模块管理接口"""
    result_dict = await PlotCategoryService.update_category_service(auth=auth, id=id, data=data)
    log.info("修改绘图模块管理成功")
    return SuccessResponse(data=result_dict, msg="修改绘图模块管理成功")

@PlotCategoryRouter.delete("/delete", summary="删除绘图模块管理", description="删除绘图模块管理")
async def delete_category_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_plot:category:delete"]))
) -> JSONResponse:
    """删除绘图模块管理接口"""
    await PlotCategoryService.delete_category_service(auth=auth, ids=ids)
    log.info(f"删除绘图模块管理成功: {ids}")
    return SuccessResponse(msg="删除绘图模块管理成功")

@PlotCategoryRouter.patch("/available/setting", summary="批量修改绘图模块管理状态", description="批量修改绘图模块管理状态")
async def batch_set_available_category_controller(
    data: BatchSetAvailable,
    auth: AuthSchema = Depends(AuthPermission(["module_plot:category:patch"]))
) -> JSONResponse:
    """批量修改绘图模块管理状态接口"""
    await PlotCategoryService.set_available_category_service(auth=auth, data=data)
    log.info(f"批量修改绘图模块管理状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改绘图模块管理状态成功")

@PlotCategoryRouter.post('/export', summary="导出绘图模块管理", description="导出绘图模块管理")
async def export_category_list_controller(
    search: PlotCategoryQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_plot:category:export"]))
) -> StreamingResponse:
    """导出绘图模块管理接口"""
    result_dict_list = await PlotCategoryService.list_category_service(search=search, auth=auth)
    export_result = await PlotCategoryService.batch_export_category_service(obj_list=result_dict_list)
    log.info('导出绘图模块管理成功')
    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            'Content-Disposition': 'attachment; filename=plot_category.xlsx'
        }
    )

@PlotCategoryRouter.post('/import', summary="导入绘图模块管理", description="导入绘图模块管理")
async def import_category_list_controller(
    file: UploadFile,
    auth: AuthSchema = Depends(AuthPermission(["module_plot:category:import"]))
) -> JSONResponse:
    """导入绘图模块管理接口"""
    batch_import_result = await PlotCategoryService.batch_import_category_service(file=file, auth=auth, update_support=True)
    log.info("导入绘图模块管理成功")
    return SuccessResponse(data=batch_import_result, msg="导入绘图模块管理成功")

@PlotCategoryRouter.post('/download/template', summary="获取绘图模块管理导入模板", description="获取绘图模块管理导入模板", dependencies=[Depends(AuthPermission(["module_plot:category:download"]))])
async def export_category_template_controller() -> StreamingResponse:
    """获取绘图模块管理导入模板接口"""
    import_template_result = await PlotCategoryService.import_template_download_category_service()
    log.info('获取绘图模块管理导入模板成功')
    return StreamResponse(
        data=bytes2file_response(import_template_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename=plot_category_template.xlsx'}
    )