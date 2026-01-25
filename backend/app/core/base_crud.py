import builtins
from collections.abc import Sequence
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy import Select, asc, delete, desc, func, select, update
from sqlalchemy import inspect as sa_inspect
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.elements import ColumnElement

from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.base_model import MappedBase
from app.core.exceptions import CustomException
from app.core.permission import Permission

if TYPE_CHECKING:
    from sqlalchemy.engine import Result

ModelType = TypeVar("ModelType", bound=MappedBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
OutSchemaType = TypeVar("OutSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """基础数据层"""

    def __init__(self, model: type[ModelType], auth: AuthSchema) -> None:
        """
        初始化CRUDBase类

        参数:
        - model (Type[ModelType]): 数据模型类。
        - auth (AuthSchema): 认证信息。

        返回:
        - None
        """
        self.model = model
        self.auth = auth

    async def get(self, preload: list[str | Any] | None = None, **kwargs) -> ModelType | None:
        """
        根据条件获取单个对象

        参数:
        - preload (Optional[List[Union[str, Any]]]): 预加载关系，支持关系名字符串或SQLAlchemy loader option
        - **kwargs: 查询条件

        返回:
        - Optional[ModelType]: 对象实例

        异常:
        - CustomException: 查询失败时抛出异常
        """
        try:
            conditions = await self.__build_conditions(**kwargs)
            sql = select(self.model).where(*conditions)
            # 应用可配置的预加载选项
            for opt in self.__loader_options(preload):
                sql = sql.options(opt)

            sql = await self.__filter_permissions(sql)

            result: Result = await self.auth.db.execute(sql)
            obj = result.scalars().first()
            return obj
        except Exception as e:
            raise CustomException(msg=f"获取查询失败: {e!s}")

    async def list(
        self,
        search: dict | None = None,
        order_by: list[dict[str, str]] | None = None,
        preload: list[str | Any] | None = None,
    ) -> Sequence[ModelType]:
        """
        根据条件获取对象列表

        参数:
        - search (Optional[Dict]): 查询条件,格式为 {'id': value, 'name': value}
        - order_by (Optional[List[Dict[str, str]]]): 排序字段,格式为 [{'id': 'asc'}, {'name': 'desc'}]
        - preload (Optional[List[Union[str, Any]]]): 预加载关系，支持关系名字符串或SQLAlchemy loader option

        返回:
        - Sequence[ModelType]: 对象列表

        异常:
        - CustomException: 查询失败时抛出异常
        """
        try:
            conditions = await self.__build_conditions(**search) if search else []
            order = order_by or [{"id": "asc"}]
            sql = select(self.model).where(*conditions).order_by(*self.__order_by(order))
            # 应用可配置的预加载选项
            for opt in self.__loader_options(preload):
                sql = sql.options(opt)
            sql = await self.__filter_permissions(sql)
            result: Result = await self.auth.db.execute(sql)
            return result.scalars().all()
        except Exception as e:
            raise CustomException(msg=f"列表查询失败: {e!s}")

    async def tree_list(
        self,
        search: dict | None = None,
        order_by: builtins.list[dict[str, str]] | None = None,
        children_attr: str = "children",
        preload: builtins.list[str | Any] | None = None,
    ) -> Sequence[ModelType]:
        """
        获取树形结构数据列表

        参数:
        - search (Optional[Dict]): 查询条件
        - order_by (Optional[List[Dict[str, str]]]): 排序字段
        - children_attr (str): 子节点属性名
        - preload (Optional[List[Union[str, Any]]]): 额外预加载关系，若为None则默认包含children_attr

        返回:
        - Sequence[ModelType]: 树形结构数据列表

        异常:
        - CustomException: 查询失败时抛出异常
        """
        try:
            conditions = await self.__build_conditions(**search) if search else []
            order = order_by or [{"id": "asc"}]
            sql = select(self.model).where(*conditions).order_by(*self.__order_by(order))

            # 处理预加载选项
            final_preload = preload
            # 如果没有提供preload且children_attr存在，则添加到预加载选项中
            if preload is None and children_attr and hasattr(self.model, children_attr):
                # 获取模型默认预加载选项
                model_defaults = getattr(self.model, "__loader_options__", [])
                # 将children_attr添加到默认预加载选项中
                final_preload = [*list(model_defaults), children_attr]

            # 应用预加载选项
            for opt in self.__loader_options(final_preload):
                sql = sql.options(opt)

            sql = await self.__filter_permissions(sql)
            result: Result = await self.auth.db.execute(sql)
            return result.scalars().all()
        except Exception as e:
            raise CustomException(msg=f"树形列表查询失败: {e!s}")

    async def page(
        self,
        offset: int,
        limit: int,
        order_by: builtins.list[dict[str, str]],
        search: dict,
        out_schema: type[OutSchemaType],
        preload: builtins.list[str | Any] | None = None,
    ) -> dict:
        """
        获取分页数据

        参数:
        - offset (int): 偏移量
        - limit (int): 每页数量
        - order_by (List[Dict[str, str]]): 排序字段
        - search (Dict): 查询条件
        - out_schema (Type[OutSchemaType]): 输出数据模型
        - preload (Optional[List[Union[str, Any]]]): 预加载关系

        返回:
        - Dict: 分页数据

        异常:
        - CustomException: 查询失败时抛出异常
        """
        try:
            conditions = await self.__build_conditions(**search) if search else []
            order = order_by or [{"id": "asc"}]
            sql = select(self.model).where(*conditions).order_by(*self.__order_by(order))
            # 应用预加载选项
            for opt in self.__loader_options(preload):
                sql = sql.options(opt)
            sql = await self.__filter_permissions(sql)

            # 优化count查询：使用主键计数而非全表扫描
            mapper = sa_inspect(self.model)
            pk_cols = list(getattr(mapper, "primary_key", []))
            if pk_cols:
                # 使用主键的第一列进行计数（主键必定非NULL，性能更好）
                count_sql = select(func.count(pk_cols[0])).select_from(self.model)
            else:
                # 降级方案：使用count(*)
                count_sql = select(func.count()).select_from(self.model)

            if conditions:
                count_sql = count_sql.where(*conditions)
            count_sql = await self.__filter_permissions(count_sql)

            total_result = await self.auth.db.execute(count_sql)
            total = total_result.scalar() or 0

            result: Result = await self.auth.db.execute(sql.offset(offset).limit(limit))
            objs = result.scalars().all()

            return {
                "page_no": offset // limit + 1 if limit else 1,
                "page_size": limit or 10,
                "total": total,
                "has_next": offset + limit < total,
                "items": [out_schema.model_validate(obj).model_dump() for obj in objs],
            }
        except Exception as e:
            raise CustomException(msg=f"分页查询失败: {e!s}")

    async def create(self, data: CreateSchemaType | dict) -> ModelType:
        """
        创建新对象

        参数:
        - data (Union[CreateSchemaType, Dict]): 对象属性

        返回:
        - ModelType: 新创建的对象实例

        异常:
        - CustomException: 创建失败时抛出异常
        """
        try:
            obj_dict = data if isinstance(data, dict) else data.model_dump()
            obj = self.model(**obj_dict)

            # 设置字段值（只检查一次current_user）
            if self.auth.user:
                if hasattr(obj, "created_id"):
                    setattr(obj, "created_id", self.auth.user.id)
                if hasattr(obj, "updated_id"):
                    setattr(obj, "updated_id", self.auth.user.id)

            self.auth.db.add(obj)
            await self.auth.db.flush()
            await self.auth.db.refresh(obj)
            return obj
        except Exception as e:
            raise CustomException(msg=f"创建失败: {e!s}")

    async def update(self, id: int, data: UpdateSchemaType | dict) -> ModelType:
        """
        更新对象

        参数:
        - id (int): 对象ID
        - data (Union[UpdateSchemaType, Dict]): 更新的属性及值

        返回:
        - ModelType: 更新后的对象实例

        异常:
        - CustomException: 更新失败时抛出异常
        """
        try:
            obj_dict = (
                data
                if isinstance(data, dict)
                else data.model_dump(exclude_unset=True, exclude={"id"})
            )
            # 获取对象时不自动预加载关系，避免循环依赖
            obj = await self.get(id=id, preload=[])
            if not obj:
                raise CustomException(msg="更新对象不存在")

            # 设置字段值（只检查一次current_user）
            if self.auth.user and hasattr(obj, "updated_id"):
                setattr(obj, "updated_id", self.auth.user.id)

            for key, value in obj_dict.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)

            await self.auth.db.flush()
            # 刷新对象时不自动预加载关系
            await self.auth.db.refresh(obj)

            # 权限二次确认：flush后再次验证对象仍在权限范围内
            # 防止并发修改导致的权限逃逸（如其他事务修改了created_id）
            # 验证时也不自动预加载关系
            verify_obj = await self.get(id=id, preload=[])
            if not verify_obj:
                # 对象已被删除或权限已失效
                raise CustomException(msg="更新失败，对象不存在或无权限访问")

            return obj
        except Exception as e:
            raise CustomException(msg=f"更新失败: {e!s}")

    async def delete(self, ids: builtins.list[int]) -> None:
        """
        删除对象

        参数:
        - ids (List[int]): 对象ID列表

        异常:
        - CustomException: 删除失败时抛出异常
        """
        try:
            mapper = sa_inspect(self.model)
            pk_cols = list(getattr(mapper, "primary_key", []))
            if not pk_cols:
                raise CustomException(msg="模型缺少主键，无法删除")
            if len(pk_cols) > 1:
                raise CustomException(msg="暂不支持复合主键的批量删除")

            # 只删除有权限的数据
            sql = delete(self.model).where(pk_cols[0].in_(ids))
            await self.auth.db.execute(sql)
            await self.auth.db.flush()
        except Exception as e:
            raise CustomException(msg=f"删除失败: {e!s}")

    async def clear(self) -> None:
        """
        清空对象表

        异常:
        - CustomException: 清空失败时抛出异常
        """
        try:
            sql = delete(self.model)
            await self.auth.db.execute(sql)
            await self.auth.db.flush()
        except Exception as e:
            raise CustomException(msg=f"清空失败: {e!s}")

    async def set(self, ids: builtins.list[int], **kwargs) -> None:
        """
        批量更新对象

        参数:
        - ids (List[int]): 对象ID列表
        - **kwargs: 更新的属性及值

        异常:
        - CustomException: 更新失败时抛出异常
        """
        try:
            mapper = sa_inspect(self.model)
            pk_cols = list(getattr(mapper, "primary_key", []))
            if not pk_cols:
                raise CustomException(msg="模型缺少主键，无法更新")
            if len(pk_cols) > 1:
                raise CustomException(msg="暂不支持复合主键的批量更新")

            # 只更新有权限的数据
            sql = update(self.model).where(pk_cols[0].in_(ids)).values(**kwargs)
            await self.auth.db.execute(sql)
            await self.auth.db.flush()
        except CustomException:
            raise
        except Exception as e:
            raise CustomException(msg=f"批量更新失败: {e!s}")

    async def __filter_permissions(self, sql: Select) -> Select:
        """
        过滤数据权限（仅用于Select）。
        """
        filter = Permission(model=self.model, auth=self.auth)
        return await filter.filter_query(sql)

    async def __build_conditions(self, **kwargs) -> builtins.list[ColumnElement]:
        """
        构建查询条件

        参数:
        - **kwargs: 查询参数

        返回:
        - List[ColumnElement]: SQL条件表达式列表

        异常:
        - CustomException: 查询参数不存在时抛出异常
        """
        conditions = []
        for key, value in kwargs.items():
            if value is None or value == "":
                continue

            attr = getattr(self.model, key)
            if isinstance(value, tuple):
                seq, val = value
                if seq == "None":
                    conditions.append(attr.is_(None))
                elif seq == "not None":
                    conditions.append(attr.isnot(None))
                elif seq == "date" and val:
                    conditions.append(func.date_format(attr, "%Y-%m-%d") == val)
                elif seq == "month" and val:
                    conditions.append(func.date_format(attr, "%Y-%m") == val)
                elif seq == "like" and val:
                    conditions.append(attr.like(f"%{val}%"))
                elif seq == "in" and val:
                    conditions.append(attr.in_(val))
                elif seq == "between" and isinstance(val, (list, tuple)) and len(val) == 2:
                    conditions.append(attr.between(val[0], val[1]))
                elif seq == "!=" or (seq == "ne" and val):
                    conditions.append(attr != val)
                elif seq == ">" or (seq == "gt" and val):
                    conditions.append(attr > val)
                elif seq == ">=" or (seq == "ge" and val):
                    conditions.append(attr >= val)
                elif seq == "<" or (seq == "lt" and val):
                    conditions.append(attr < val)
                elif seq == "<=" or (seq == "le" and val):
                    conditions.append(attr <= val)
                elif seq == "==" or (seq == "eq" and val):
                    conditions.append(attr == val)
            else:
                conditions.append(attr == value)
        return conditions

    def __order_by(self, order_by: builtins.list[dict[str, str]]) -> builtins.list[ColumnElement]:
        """
        获取排序字段

        参数:
        - order_by (List[Dict[str, str]]): 排序字段列表,格式为 [{'id': 'asc'}, {'name': 'desc'}]

        返回:
        - List[ColumnElement]: 排序字段列表

        异常:
        - CustomException: 排序字段不存在时抛出异常
        """
        columns = []
        for order in order_by:
            for field, direction in order.items():
                column = getattr(self.model, field)
                columns.append(desc(column) if direction.lower() == "desc" else asc(column))
        return columns

    def __loader_options(
        self, preload: builtins.list[str | Any] | None = None
    ) -> builtins.list[Any]:
        """
        构建预加载选项

        参数:
        - preload (Optional[List[Union[str, Any]]]): 预加载关系，支持关系名字符串或SQLAlchemy loader option

        返回:
        - List[Any]: 预加载选项列表
        """
        options = []
        # 获取模型定义的默认加载选项
        model_loader_options = getattr(self.model, "__loader_options__", [])
     
        # # 合并所有需要预加载的选项
        # all_preloads = set(model_loader_options)
        # if preload:
        #     for opt in preload:
        #         if isinstance(opt, str):
        #             all_preloads.add(opt)
        # elif preload == []:
        #     # 如果明确指定空列表，则不使用任何预加载
        #     all_preloads = set()

        # # 处理所有预加载选项
        # for opt in all_preloads:
        #     if isinstance(opt, str):
        #         # 使用selectinload来避免在异步环境中的MissingGreenlet错误
        #         if hasattr(self.model, opt):
        #             options.append(selectinload(getattr(self.model, opt)))
        #     else:
        #         # 直接使用非字符串的加载选项
        #         options.append(opt)

         # 合并所有需要预加载的选项
        all_preloads = set()
        
        # 1. 添加模型默认的预加载选项
        for opt in model_loader_options:
            if isinstance(opt, str):
                all_preloads.add(opt)
            else:
                options.append(opt)  # 直接添加非字符串的loader选项
        
        # 2. 添加调用方指定的预加载选项
        if preload:
            for opt in preload:
                if isinstance(opt, str):
                    all_preloads.add(opt)
                else:
                    options.append(opt)
        
        # 🔥 修复：确保所有字符串类型的关系都使用selectinload
        for opt in all_preloads:
            if hasattr(self.model, opt):
                # 获取关系的属性
                rel_attr = getattr(self.model, opt)
                # 使用selectinload，这是异步环境中最安全的选择
                options.append(selectinload(rel_attr))

        return options
