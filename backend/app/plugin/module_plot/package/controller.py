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

from .service import PlotPackageService
from .schema import PlotPackageCreateSchema, PlotPackageUpdateSchema, PlotPackageQueryParam

PlotPackageRouter = APIRouter(route_class=OperationLogRoute, prefix='/package', tags=["绘图库包管理模块"]) 

@PlotPackageRouter.get("/detail/{id}", summary="获取绘图库包管理详情", description="获取绘图库包管理详情")
async def get_package_detail_controller(
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_plot:package:query"]))
) -> JSONResponse:
    """获取绘图库包管理详情接口"""
    result_dict = await PlotPackageService.detail_package_service(auth=auth, id=id)
    log.info(f"获取绘图库包管理详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取绘图库包管理详情成功")

@PlotPackageRouter.get("/list", summary="查询绘图库包管理列表", description="查询绘图库包管理列表")
async def get_package_list_controller(
    page: PaginationQueryParam = Depends(),
    search: PlotPackageQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_plot:package:query"]))
) -> JSONResponse:
    """查询绘图库包管理列表接口（数据库分页）"""
    result_dict = await PlotPackageService.page_package_service(
        auth=auth,
        page_no=page.page_no if page.page_no is not None else 1,
        page_size=page.page_size if page.page_size is not None else 10,
        search=search,
        order_by=page.order_by
    )
    log.info("查询绘图库包管理列表成功")
    return SuccessResponse(data=result_dict, msg="查询绘图库包管理列表成功")

@PlotPackageRouter.post("/create", summary="创建绘图库包管理", description="创建绘图库包管理")
async def create_package_controller(
    data: PlotPackageCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(["module_plot:package:create"]))
) -> JSONResponse:
    """创建绘图库包管理接口"""
    result_dict = await PlotPackageService.create_package_service(auth=auth, data=data)
    log.info("创建绘图库包管理成功")
    return SuccessResponse(data=result_dict, msg="创建绘图库包管理成功")

@PlotPackageRouter.put("/update/{id}", summary="修改绘图库包管理", description="修改绘图库包管理")
async def update_package_controller(
    data: PlotPackageUpdateSchema,
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_plot:package:update"]))
) -> JSONResponse:
    """修改绘图库包管理接口"""
    result_dict = await PlotPackageService.update_package_service(auth=auth, id=id, data=data)
    log.info("修改绘图库包管理成功")
    return SuccessResponse(data=result_dict, msg="修改绘图库包管理成功")

@PlotPackageRouter.delete("/delete", summary="删除绘图库包管理", description="删除绘图库包管理")
async def delete_package_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_plot:package:delete"]))
) -> JSONResponse:
    """删除绘图库包管理接口"""
    await PlotPackageService.delete_package_service(auth=auth, ids=ids)
    log.info(f"删除绘图库包管理成功: {ids}")
    return SuccessResponse(msg="删除绘图库包管理成功")

@PlotPackageRouter.patch("/available/setting", summary="批量修改绘图库包管理状态", description="批量修改绘图库包管理状态")
async def batch_set_available_package_controller(
    data: BatchSetAvailable,
    auth: AuthSchema = Depends(AuthPermission(["module_plot:package:patch"]))
) -> JSONResponse:
    """批量修改绘图库包管理状态接口"""
    await PlotPackageService.set_available_package_service(auth=auth, data=data)
    log.info(f"批量修改绘图库包管理状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改绘图库包管理状态成功")

@PlotPackageRouter.post('/export', summary="导出绘图库包管理", description="导出绘图库包管理")
async def export_package_list_controller(
    search: PlotPackageQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_plot:package:export"]))
) -> StreamingResponse:
    """导出绘图库包管理接口"""
    result_dict_list = await PlotPackageService.list_package_service(search=search, auth=auth)
    export_result = await PlotPackageService.batch_export_package_service(obj_list=result_dict_list)
    log.info('导出绘图库包管理成功')
    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            'Content-Disposition': 'attachment; filename=plot_package.xlsx'
        }
    )

@PlotPackageRouter.post('/import', summary="导入绘图库包管理", description="导入绘图库包管理")
async def import_package_list_controller(
    file: UploadFile,
    auth: AuthSchema = Depends(AuthPermission(["module_plot:package:import"]))
) -> JSONResponse:
    """导入绘图库包管理接口"""
    batch_import_result = await PlotPackageService.batch_import_package_service(file=file, auth=auth, update_support=True)
    log.info("导入绘图库包管理成功")
    return SuccessResponse(data=batch_import_result, msg="导入绘图库包管理成功")

@PlotPackageRouter.post('/download/template', summary="获取绘图库包管理导入模板", description="获取绘图库包管理导入模板", dependencies=[Depends(AuthPermission(["module_plot:package:download"]))])
async def export_package_template_controller() -> StreamingResponse:
    """获取绘图库包管理导入模板接口"""
    import_template_result = await PlotPackageService.import_template_download_package_service()
    log.info('获取绘图库包管理导入模板成功')
    return StreamResponse(
        data=bytes2file_response(import_template_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename=plot_package_template.xlsx'}
    )