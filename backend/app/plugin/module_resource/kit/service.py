# -*- coding: utf-8 -*-

import io
from fastapi import UploadFile
import pandas as pd

from app.core.base_schema import BatchSetAvailable
from app.core.exceptions import CustomException
from app.utils.excel_util import ExcelUtil
from app.core.logger import log
from app.api.v1.module_system.auth.schema import AuthSchema
from .schema import ResourceKitCreateSchema, ResourceKitUpdateSchema, ResourceKitOutSchema, ResourceKitQueryParam
from .crud import ResourceKitCRUD


class ResourceKitService:
    """
    模块服务层
    """
    
    @classmethod
    async def detail_kit_service(cls, auth: AuthSchema, id: int) -> dict:
        """详情"""
        obj = await ResourceKitCRUD(auth).get_by_id_kit_crud(id=id)
        if not obj:
            raise CustomException(msg="该数据不存在")
        return ResourceKitOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def list_kit_service(cls, auth: AuthSchema, search: ResourceKitQueryParam | None = None, order_by: list[dict] | None = None) -> list[dict]:
        """列表查询"""
        search_dict = search.__dict__ if search else None
        obj_list = await ResourceKitCRUD(auth).list_kit_crud(search=search_dict, order_by=order_by)
        return [ResourceKitOutSchema.model_validate(obj).model_dump() for obj in obj_list]

    @classmethod
    async def page_kit_service(cls, auth: AuthSchema, page_no: int, page_size: int, search: ResourceKitQueryParam | None = None, order_by: list[dict] | None = None) -> dict:
        """分页查询（数据库分页）"""
        search_dict = search.__dict__ if search else {}
        order_by_list = order_by or [{'id': 'asc'}]
        offset = (page_no - 1) * page_size
        result = await ResourceKitCRUD(auth).page_kit_crud(
            offset=offset,
            limit=page_size,
            order_by=order_by_list,
            search=search_dict
        )
        return result
    
    @classmethod
    async def create_kit_service(cls, auth: AuthSchema, data: ResourceKitCreateSchema) -> dict:
        """创建"""
        # 检查唯一性约束
        obj = await ResourceKitCRUD(auth).create_kit_crud(data=data)
        return ResourceKitOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def update_kit_service(cls, auth: AuthSchema, id: int, data: ResourceKitUpdateSchema) -> dict:
        """更新"""
        # 检查数据是否存在
        obj = await ResourceKitCRUD(auth).get_by_id_kit_crud(id=id)
        if not obj:
            raise CustomException(msg='更新失败，该数据不存在')
        
        # 检查唯一性约束
            
        obj = await ResourceKitCRUD(auth).update_kit_crud(id=id, data=data)
        return ResourceKitOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def delete_kit_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """删除"""
        if len(ids) < 1:
            raise CustomException(msg='删除失败，删除对象不能为空')
        for id in ids:
            obj = await ResourceKitCRUD(auth).get_by_id_kit_crud(id=id)
            if not obj:
                raise CustomException(msg=f'删除失败，ID为{id}的数据不存在')
        await ResourceKitCRUD(auth).delete_kit_crud(ids=ids)
    
    @classmethod
    async def set_available_kit_service(cls, auth: AuthSchema, data: BatchSetAvailable) -> None:
        """批量设置状态"""
        await ResourceKitCRUD(auth).set_available_kit_crud(ids=data.ids)
    
    @classmethod
    async def batch_export_kit_service(cls, obj_list: list[dict]) -> bytes:
        """批量导出"""
        mapping_dict = {
            'id': '自增主键ID',
            'name': '模块名称',
            'type': '模块类型',
            'language': '编程语言',
            'description': '备注/描述',
            'local_path': '本地文件',
            'network_url': '网络地址',
            'cloud_url': '网盘地址',
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
    async def batch_import_kit_service(cls, auth: AuthSchema, file: UploadFile, update_support: bool = False) -> str:
        """批量导入"""
        header_dict = {
            '自增主键ID': 'id',
            '模块名称': 'name',
            '模块类型': 'type',
            '编程语言': 'language',
            '备注/描述': 'description',
            '本地文件': 'local_path',
            '网络地址': 'network_url',
            '网盘地址': 'cloud_url',
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
                        "type": row['type'],
                        "language": row['language'],
                        "description": row['description'],
                        "local_path": row['local_path'],
                        "network_url": row['network_url'],
                        "cloud_url": row['cloud_url'],
                        "created_time": row['created_time'],
                        "updated_time": row['updated_time'],
                        "created_id": row['created_id'],
                        "updated_id": row['updated_id'],
                    }
                    # 使用CreateSchema做校验后入库
                    create_schema = ResourceKitCreateSchema.model_validate(data)
                    
                    # 检查唯一性约束
                    
                    await ResourceKitCRUD(auth).create_kit_crud(data=create_schema)
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
    async def import_template_download_kit_service(cls) -> bytes:
        """下载导入模板"""
        header_list = [
            '自增主键ID',
            '模块名称',
            '模块类型',
            '编程语言',
            '备注/描述',
            '本地文件',
            '网络地址',
            '网盘地址',
            '创建时间',
            '更新时间',
            '创建人ID',
            '更新人ID',
        ]
        selector_header_list = []
        option_list = []
        
        # 添加下拉选项
        selector_header_list.append('模块类型')
        option_list.append({'模块类型': []})
        selector_header_list.append('编程语言')
        option_list.append({'编程语言': []})
        
        return ExcelUtil.get_excel_template(
            header_list=header_list,
            selector_header_list=selector_header_list,
            option_list=option_list
        )