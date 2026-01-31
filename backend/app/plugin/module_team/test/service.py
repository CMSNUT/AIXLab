# -*- coding: utf-8 -*-

import io
from fastapi import UploadFile
import pandas as pd

from app.core.base_schema import BatchSetAvailable
from app.core.exceptions import CustomException
from app.utils.excel_util import ExcelUtil
from app.core.logger import log
from app.api.v1.module_system.auth.schema import AuthSchema
from .schema import TeamTestCreateSchema, TeamTestUpdateSchema, TeamTestOutSchema, TeamTestQueryParam
from .crud import TeamTestCRUD


class TeamTestService:
    """
    测试服务层
    """
    
    @classmethod
    async def detail_test_service(cls, auth: AuthSchema, id: int) -> dict:
        """详情"""
        obj = await TeamTestCRUD(auth).get_by_id_test_crud(id=id)
        if not obj:
            raise CustomException(msg="该数据不存在")
        return TeamTestOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def list_test_service(cls, auth: AuthSchema, search: TeamTestQueryParam | None = None, order_by: list[dict] | None = None) -> list[dict]:
        """列表查询"""
        search_dict = search.__dict__ if search else None
        obj_list = await TeamTestCRUD(auth).list_test_crud(search=search_dict, order_by=order_by)
        return [TeamTestOutSchema.model_validate(obj).model_dump() for obj in obj_list]

    @classmethod
    async def page_test_service(cls, auth: AuthSchema, page_no: int, page_size: int, search: TeamTestQueryParam | None = None, order_by: list[dict] | None = None) -> dict:
        """分页查询（数据库分页）"""
        search_dict = search.__dict__ if search else {}
        order_by_list = order_by or [{'id': 'asc'}]
        offset = (page_no - 1) * page_size
        result = await TeamTestCRUD(auth).page_test_crud(
            offset=offset,
            limit=page_size,
            order_by=order_by_list,
            search=search_dict
        )
        return result
    
    @classmethod
    async def create_test_service(cls, auth: AuthSchema, data: TeamTestCreateSchema) -> dict:
        """创建"""
        # 检查唯一性约束
        obj = await TeamTestCRUD(auth).create_test_crud(data=data)
        return TeamTestOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def update_test_service(cls, auth: AuthSchema, id: int, data: TeamTestUpdateSchema) -> dict:
        """更新"""
        # 检查数据是否存在
        obj = await TeamTestCRUD(auth).get_by_id_test_crud(id=id)
        if not obj:
            raise CustomException(msg='更新失败，该数据不存在')
        
        # 检查唯一性约束
            
        obj = await TeamTestCRUD(auth).update_test_crud(id=id, data=data)
        return TeamTestOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def delete_test_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """删除"""
        if len(ids) < 1:
            raise CustomException(msg='删除失败，删除对象不能为空')
        for id in ids:
            obj = await TeamTestCRUD(auth).get_by_id_test_crud(id=id)
            if not obj:
                raise CustomException(msg=f'删除失败，ID为{id}的数据不存在')
        await TeamTestCRUD(auth).delete_test_crud(ids=ids)
    
    @classmethod
    async def set_available_test_service(cls, auth: AuthSchema, data: BatchSetAvailable) -> None:
        """批量设置状态"""
        await TeamTestCRUD(auth).set_available_test_crud(ids=data.ids)
    
    @classmethod
    async def batch_export_test_service(cls, obj_list: list[dict]) -> bytes:
        """批量导出"""
        mapping_dict = {
            'id': '主键ID',
            'name': '课题名称',
            'content': '课题简介',
            'file_path': '本地文件',
            'image_path': '本地图片',
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
    async def batch_import_test_service(cls, auth: AuthSchema, file: UploadFile, update_support: bool = False) -> str:
        """批量导入"""
        header_dict = {
            '主键ID': 'id',
            '课题名称': 'name',
            '课题简介': 'content',
            '本地文件': 'file_path',
            '本地图片': 'image_path',
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
                        "content": row['content'],
                        "file_path": row['file_path'],
                        "image_path": row['image_path'],
                        "created_time": row['created_time'],
                        "updated_time": row['updated_time'],
                        "created_id": row['created_id'],
                        "updated_id": row['updated_id'],
                    }
                    # 使用CreateSchema做校验后入库
                    create_schema = TeamTestCreateSchema.model_validate(data)
                    
                    # 检查唯一性约束
                    
                    await TeamTestCRUD(auth).create_test_crud(data=create_schema)
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
    async def import_template_download_test_service(cls) -> bytes:
        """下载导入模板"""
        header_list = [
            '主键ID',
            '课题名称',
            '课题简介',
            '本地文件',
            '本地图片',
            '创建时间',
            '更新时间',
            '创建人ID',
            '更新人ID',
        ]
        selector_header_list = []
        option_list = []
        
        # 添加下拉选项
        
        return ExcelUtil.get_excel_template(
            header_list=header_list,
            selector_header_list=selector_header_list,
            option_list=option_list
        )