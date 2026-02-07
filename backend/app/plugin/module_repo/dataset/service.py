# -*- coding: utf-8 -*-

import io
from fastapi import UploadFile
import pandas as pd

from app.core.base_schema import BatchSetAvailable
from app.core.exceptions import CustomException
from app.utils.excel_util import ExcelUtil
from app.core.logger import log
from app.api.v1.module_system.auth.schema import AuthSchema
from .schema import RepoDatasetCreateSchema, RepoDatasetUpdateSchema, RepoDatasetOutSchema, RepoDatasetQueryParam
from .crud import RepoDatasetCRUD


class RepoDatasetService:
    """
    数据仓库管理服务层
    """
    
    @classmethod
    async def detail_dataset_service(cls, auth: AuthSchema, id: int) -> dict:
        """详情"""
        obj = await RepoDatasetCRUD(auth).get_by_id_dataset_crud(id=id)
        if not obj:
            raise CustomException(msg="该数据不存在")
        return RepoDatasetOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def list_dataset_service(cls, auth: AuthSchema, search: RepoDatasetQueryParam | None = None, order_by: list[dict] | None = None) -> list[dict]:
        """列表查询"""
        search_dict = search.__dict__ if search else None
        obj_list = await RepoDatasetCRUD(auth).list_dataset_crud(search=search_dict, order_by=order_by)
        return [RepoDatasetOutSchema.model_validate(obj).model_dump() for obj in obj_list]

    @classmethod
    async def page_dataset_service(cls, auth: AuthSchema, page_no: int, page_size: int, search: RepoDatasetQueryParam | None = None, order_by: list[dict] | None = None) -> dict:
        """分页查询（数据库分页）"""
        search_dict = search.__dict__ if search else {}
        order_by_list = order_by or [{'id': 'asc'}]
        offset = (page_no - 1) * page_size
        result = await RepoDatasetCRUD(auth).page_dataset_crud(
            offset=offset,
            limit=page_size,
            order_by=order_by_list,
            search=search_dict
        )
        return result
    
    @classmethod
    async def create_dataset_service(cls, auth: AuthSchema, data: RepoDatasetCreateSchema) -> dict:
        """创建"""
        # 检查唯一性约束
        obj = await RepoDatasetCRUD(auth).create_dataset_crud(data=data)
        return RepoDatasetOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def update_dataset_service(cls, auth: AuthSchema, id: int, data: RepoDatasetUpdateSchema) -> dict:
        """更新"""
        # 检查数据是否存在
        obj = await RepoDatasetCRUD(auth).get_by_id_dataset_crud(id=id)
        if not obj:
            raise CustomException(msg='更新失败，该数据不存在')
        
        # 检查唯一性约束
            
        obj = await RepoDatasetCRUD(auth).update_dataset_crud(id=id, data=data)
        return RepoDatasetOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def delete_dataset_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """删除"""
        if len(ids) < 1:
            raise CustomException(msg='删除失败，删除对象不能为空')
        for id in ids:
            obj = await RepoDatasetCRUD(auth).get_by_id_dataset_crud(id=id)
            if not obj:
                raise CustomException(msg=f'删除失败，ID为{id}的数据不存在')
        await RepoDatasetCRUD(auth).delete_dataset_crud(ids=ids)
    
    @classmethod
    async def set_available_dataset_service(cls, auth: AuthSchema, data: BatchSetAvailable) -> None:
        """批量设置状态"""
        await RepoDatasetCRUD(auth).set_available_dataset_crud(ids=data.ids)
    
    @classmethod
    async def batch_export_dataset_service(cls, obj_list: list[dict]) -> bytes:
        """批量导出"""
        mapping_dict = {
            'id': '自增主键ID',
            'name': '数据仓库名称',
            'alias': '数据英文名称',
            'format': '数据格式',
            'field': '应用领域',
            'category': '数据类别',
            'description': '数据描述',
            'local_file': '本地文件',
            'url_link': '网络地址',
            'cloud_link': '网盘链接',
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
    async def batch_import_dataset_service(cls, auth: AuthSchema, file: UploadFile, update_support: bool = False) -> str:
        """批量导入"""
        header_dict = {
            '自增主键ID': 'id',
            '数据仓库名称': 'name',
            '数据英文名称': 'alias',
            '数据格式': 'format',
            '应用领域': 'field',
            '数据类别': 'category',
            '数据描述': 'description',
            '本地文件': 'local_file',
            '网络地址': 'url_link',
            '网盘链接': 'cloud_link',
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
                        "alias": row['alias'],
                        "format": row['format'],
                        "field": row['field'],
                        "category": row['category'],
                        "description": row['description'],
                        "local_file": row['local_file'],
                        "url_link": row['url_link'],
                        "cloud_link": row['cloud_link'],
                        "created_time": row['created_time'],
                        "updated_time": row['updated_time'],
                        "created_id": row['created_id'],
                        "updated_id": row['updated_id'],
                    }
                    # 使用CreateSchema做校验后入库
                    create_schema = RepoDatasetCreateSchema.model_validate(data)
                    
                    # 检查唯一性约束
                    
                    await RepoDatasetCRUD(auth).create_dataset_crud(data=create_schema)
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
    async def import_template_download_dataset_service(cls) -> bytes:
        """下载导入模板"""
        header_list = [
            '自增主键ID',
            '数据仓库名称',
            '数据英文名称',
            '数据格式',
            '应用领域',
            '数据类别',
            '数据描述',
            '本地文件',
            '网络地址',
            '网盘链接',
            '创建时间',
            '更新时间',
            '创建人ID',
            '更新人ID',
        ]
        selector_header_list = []
        option_list = []
        
        # 添加下拉选项
        selector_header_list.append('数据格式')
        option_list.append({'数据格式': []})
        selector_header_list.append('应用领域')
        option_list.append({'应用领域': []})
        
        return ExcelUtil.get_excel_template(
            header_list=header_list,
            selector_header_list=selector_header_list,
            option_list=option_list
        )