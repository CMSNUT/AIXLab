# -*- coding: utf-8 -*-

import io
from fastapi import UploadFile, HTTPException
import httpx
import pandas as pd

from app.core.base_schema import BatchSetAvailable, DownloadFileSchema
from app.core.exceptions import CustomException
from app.utils.excel_util import ExcelUtil
from app.core.logger import log
from app.api.v1.module_system.auth.schema import AuthSchema
from app.utils.upload_util import UploadUtil
from .schema import LabPlotCreateSchema, LabPlotUpdateSchema, LabPlotOutSchema, LabPlotQueryParam
from .crud import LabPlotCRUD
from httpx import AsyncClient, HTTPStatusError, TimeoutException, RequestError
from typing import Dict, Any
from app.config.setting import settings


class LabPlotService:
    """
    绘图工具管理服务层
    """
    
    @classmethod
    async def detail_plot_service(cls, auth: AuthSchema, id: int) -> dict:
        """详情"""
        obj = await LabPlotCRUD(auth).get_by_id_plot_crud(id=id)
        if not obj:
            raise CustomException(msg="该数据不存在")
        return LabPlotOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def list_plot_service(cls, auth: AuthSchema, search: LabPlotQueryParam | None = None, order_by: list[dict] | None = None) -> list[dict]:
        """列表查询"""
        search_dict = search.__dict__ if search else None
        obj_list = await LabPlotCRUD(auth).list_plot_crud(search=search_dict, order_by=order_by)
        return [LabPlotOutSchema.model_validate(obj).model_dump() for obj in obj_list]

    @classmethod
    async def page_plot_service(cls, auth: AuthSchema, page_no: int, page_size: int, search: LabPlotQueryParam | None = None, order_by: list[dict] | None = None) -> dict:
        """分页查询（数据库分页）"""
        search_dict = search.__dict__ if search else {}
        order_by_list = order_by or [{'id': 'asc'}]
        offset = (page_no - 1) * page_size
        result = await LabPlotCRUD(auth).page_plot_crud(
            offset=offset,
            limit=page_size,
            order_by=order_by_list,
            search=search_dict
        )
        return result
    
    @classmethod
    async def create_plot_service(cls, auth: AuthSchema, data: LabPlotCreateSchema) -> dict:
        """创建"""
        # 检查唯一性约束
        obj = await LabPlotCRUD(auth).create_plot_crud(data=data)
        return LabPlotOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def update_plot_service(cls, auth: AuthSchema, id: int, data: LabPlotUpdateSchema) -> dict:
        """更新"""
        # 检查数据是否存在
        obj = await LabPlotCRUD(auth).get_by_id_plot_crud(id=id)
        if not obj:
            raise CustomException(msg='更新失败，该数据不存在')
        
        # 检查唯一性约束
            
        obj = await LabPlotCRUD(auth).update_plot_crud(id=id, data=data)
        return LabPlotOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def delete_plot_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """删除"""
        if len(ids) < 1:
            raise CustomException(msg='删除失败，删除对象不能为空')
        for id in ids:
            obj = await LabPlotCRUD(auth).get_by_id_plot_crud(id=id)
            if not obj:
                raise CustomException(msg=f'删除失败，ID为{id}的数据不存在')
        await LabPlotCRUD(auth).delete_plot_crud(ids=ids)
    
    @classmethod
    async def set_available_plot_service(cls, auth: AuthSchema, data: BatchSetAvailable) -> None:
        """批量设置状态"""
        await LabPlotCRUD(auth).set_available_plot_crud(ids=data.ids)
    
    @classmethod
    async def batch_export_plot_service(cls, obj_list: list[dict]) -> bytes:
        """批量导出"""
        mapping_dict = {
            'id': '自增主键ID',
            'name': '绘图模块名称',
            'code': '模块英文名称',
            'field': '领域',
            'category': '类别',
            'description': '备注/描述',
            'image': '图片',
            'created_time': '创建时间',
            'updated_time': '更新时间',
            'created_id': '创建人ID',
            'updated_id': '更新人ID',
            'updated_id': '更新者ID',
        }

        data = obj_list.copy()
        for item in data:
            # 创建者转换
            creator_info = item.get('creator')
            if isinstance(creator_info, dict):
                item['creator'] = creator_info.get('name', '未知')
            elif creator_info is None:
                item['creator'] = '未知'

        return ExcelUtil.export_list2excel(list_data=data, mapping_dict=mapping_dict)

    @classmethod
    async def batch_import_plot_service(cls, auth: AuthSchema, file: UploadFile, update_support: bool = False) -> str:
        """批量导入"""
        header_dict = {
            '自增主键ID': 'id',
            '绘图模块名称': 'name',
            '模块英文名称': 'code',
            '领域': 'field',
            '类别': 'category',
            '备注/描述': 'description',
            '图片': 'image',
            '创建时间': 'created_time',
            '更新时间': 'updated_time',
            '创建人ID': 'created_id',
            '更新人ID': 'updated_id',
        }

        try:
            contents = await file.read()
            df = pd.read_excel(io.BytesIO(contents))
            await file.close()
            
            if df.empty:
                raise CustomException(msg="导入文件为空")
            
            missing_headers = [header for header in header_dict.keys() if header not in df.columns]
            if missing_headers:
                raise CustomException(msg=f"导入文件缺少必要的列: {', '.join(missing_headers)}")
            
            df.rename(columns=header_dict, inplace=True)
            
            # 验证必填字段
            
            error_msgs = []
            success_count = 0
            count = 0
            
            for index, row in df.iterrows():
                count += 1
                try:
                    data = {
                        "id": row['id'],
                        "name": row['name'],
                        "code": row['code'],
                        "field": row['field'],
                        "category": row['category'],
                        "description": row['description'],
                        "image": row['image'],
                        "created_time": row['created_time'],
                        "updated_time": row['updated_time'],
                        "created_id": row['created_id'],
                        "updated_id": row['updated_id'],
                    }
                    # 使用CreateSchema做校验后入库
                    create_schema = LabPlotCreateSchema.model_validate(data)
                    
                    # 检查唯一性约束
                    
                    await LabPlotCRUD(auth).create_plot_crud(data=create_schema)
                    success_count += 1
                except Exception as e:
                    error_msgs.append(f"第{count}行: {str(e)}")
                    continue

            result = f"成功导入 {success_count} 条数据"
            if error_msgs:
                result += "\n错误信息:\n" + "\n".join(error_msgs)
            return result
            
        except Exception as e:
            log.error(f"批量导入失败: {str(e)}")
            raise CustomException(msg=f"导入失败: {str(e)}")
    
    @classmethod
    async def import_template_download_plot_service(cls) -> bytes:
        """下载导入模板"""
        header_list = [
            '自增主键ID',
            '绘图模块名称',
            '模块英文名称',
            '领域',
            '类别',
            '备注/描述',
            '图片',
            '创建时间',
            '更新时间',
            '创建人ID',
            '更新人ID',
        ]
        selector_header_list = []
        option_list = []
        
        # 添加下拉选项
        selector_header_list.append('领域')
        option_list.append({'领域': []})
        
        return ExcelUtil.get_excel_template(
            header_list=header_list,
            selector_header_list=selector_header_list,
            option_list=option_list
        )
    
    @classmethod
    async def add_service(cls, a: float, b: float) -> Dict[str, Any]:
        """
        加法业务逻辑：
        1. 构建R服务要求的请求格式
        2. 调用R Plumber的add API
        3. 解析R响应，统一返回格式
        4. 异常透传：R服务的错误直接抛给控制器
        """
        # 1. 构建R服务期望的请求格式：{data: {a, b}}
        r_request_data = {"data": {"a": a, "b": b}}
        
        try:
            # 2. 异步调用R Plumber的加法API
            async with AsyncClient(timeout=settings.R_API_TIMEOUT) as client:
                r_response = await client.post(
                    url=f"{settings.R_API_BASE_URL}/api/r452/add",
                    json=r_request_data,  # 传JSON体，匹配R的解析逻辑
                    headers={"Content-Type": "application/json"}
                )
            # 3. 校验R API响应状态码，非200则抛出异常
            r_response.raise_for_status()
            
            # 4. 解析R返回的JSON数据（核心修改：之前直接返回Response对象）
            r_result = r_response.json()
            
            # 5. 校验R服务返回的success状态，失败则抛异常
            if not r_result.get("success"):
                raise HTTPException(
                    status_code=400,
                    detail=r_result.get("error", "R服务计算失败")
                )
            
            # 6. 返回解析后的R计算结果
            return r_result
            
        except TimeoutException:
            raise HTTPException(status_code=504, detail="R服务请求超时")
        except HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=f"R服务响应错误：{e.response.text}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"调用R服务失败：{str(e)}")
        

