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

from .service import ExampleNoteService
from .schema import ExampleNoteCreateSchema, ExampleNoteUpdateSchema, ExampleNoteQueryParam

ExampleNoteRouter = APIRouter(route_class=OperationLogRoute, prefix='/note', tags=["案例分析笔记管理模块"]) 

@ExampleNoteRouter.get("/detail/{id}", summary="获取案例分析笔记管理详情", description="获取案例分析笔记管理详情")
async def get_note_detail_controller(
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_example:note:query"]))
) -> JSONResponse:
    """获取案例分析笔记管理详情接口"""
    result_dict = await ExampleNoteService.detail_note_service(auth=auth, id=id)
    log.info(f"获取案例分析笔记管理详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取案例分析笔记管理详情成功")

@ExampleNoteRouter.get("/list", summary="查询案例分析笔记管理列表", description="查询案例分析笔记管理列表")
async def get_note_list_controller(
    page: PaginationQueryParam = Depends(),
    search: ExampleNoteQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_example:note:query"]))
) -> JSONResponse:
    """查询案例分析笔记管理列表接口（数据库分页）"""
    result_dict = await ExampleNoteService.page_note_service(
        auth=auth,
        page_no=page.page_no if page.page_no is not None else 1,
        page_size=page.page_size if page.page_size is not None else 10,
        search=search,
        order_by=page.order_by
    )
    log.info("查询案例分析笔记管理列表成功")
    return SuccessResponse(data=result_dict, msg="查询案例分析笔记管理列表成功")

@ExampleNoteRouter.post("/create", summary="创建案例分析笔记管理", description="创建案例分析笔记管理")
async def create_note_controller(
    data: ExampleNoteCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(["module_example:note:create"]))
) -> JSONResponse:
    """创建案例分析笔记管理接口"""
    result_dict = await ExampleNoteService.create_note_service(auth=auth, data=data)
    log.info("创建案例分析笔记管理成功")
    return SuccessResponse(data=result_dict, msg="创建案例分析笔记管理成功")

@ExampleNoteRouter.put("/update/{id}", summary="修改案例分析笔记管理", description="修改案例分析笔记管理")
async def update_note_controller(
    data: ExampleNoteUpdateSchema,
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_example:note:update"]))
) -> JSONResponse:
    """修改案例分析笔记管理接口"""
    result_dict = await ExampleNoteService.update_note_service(auth=auth, id=id, data=data)
    log.info("修改案例分析笔记管理成功")
    return SuccessResponse(data=result_dict, msg="修改案例分析笔记管理成功")

@ExampleNoteRouter.delete("/delete", summary="删除案例分析笔记管理", description="删除案例分析笔记管理")
async def delete_note_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_example:note:delete"]))
) -> JSONResponse:
    """删除案例分析笔记管理接口"""
    await ExampleNoteService.delete_note_service(auth=auth, ids=ids)
    log.info(f"删除案例分析笔记管理成功: {ids}")
    return SuccessResponse(msg="删除案例分析笔记管理成功")

@ExampleNoteRouter.patch("/available/setting", summary="批量修改案例分析笔记管理状态", description="批量修改案例分析笔记管理状态")
async def batch_set_available_note_controller(
    data: BatchSetAvailable,
    auth: AuthSchema = Depends(AuthPermission(["module_example:note:patch"]))
) -> JSONResponse:
    """批量修改案例分析笔记管理状态接口"""
    await ExampleNoteService.set_available_note_service(auth=auth, data=data)
    log.info(f"批量修改案例分析笔记管理状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改案例分析笔记管理状态成功")

@ExampleNoteRouter.post('/export', summary="导出案例分析笔记管理", description="导出案例分析笔记管理")
async def export_note_list_controller(
    search: ExampleNoteQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_example:note:export"]))
) -> StreamingResponse:
    """导出案例分析笔记管理接口"""
    result_dict_list = await ExampleNoteService.list_note_service(search=search, auth=auth)
    export_result = await ExampleNoteService.batch_export_note_service(obj_list=result_dict_list)
    log.info('导出案例分析笔记管理成功')
    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            'Content-Disposition': 'attachment; filename=example_note.xlsx'
        }
    )

@ExampleNoteRouter.post('/import', summary="导入案例分析笔记管理", description="导入案例分析笔记管理")
async def import_note_list_controller(
    file: UploadFile,
    auth: AuthSchema = Depends(AuthPermission(["module_example:note:import"]))
) -> JSONResponse:
    """导入案例分析笔记管理接口"""
    batch_import_result = await ExampleNoteService.batch_import_note_service(file=file, auth=auth, update_support=True)
    log.info("导入案例分析笔记管理成功")
    return SuccessResponse(data=batch_import_result, msg="导入案例分析笔记管理成功")

@ExampleNoteRouter.post('/download/template', summary="获取案例分析笔记管理导入模板", description="获取案例分析笔记管理导入模板", dependencies=[Depends(AuthPermission(["module_example:note:download"]))])
async def export_note_template_controller() -> StreamingResponse:
    """获取案例分析笔记管理导入模板接口"""
    import_template_result = await ExampleNoteService.import_template_download_note_service()
    log.info('获取案例分析笔记管理导入模板成功')
    return StreamResponse(
        data=bytes2file_response(import_template_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename=example_note_template.xlsx'}
    )