# gencode
## 代码生成/基础配置/保存配置
1. backend/app/plugin/module_generator/gencode/model.py 
- class GenTableModel

原始：
```python
    # 关联关系
    columns: Mapped[list["GenTableColumnModel"]] = relationship(
        order_by="GenTableColumnModel.sort",
        back_populates="table",
        cascade="all, delete-orphan",
        primaryjoin="GenTableModel.id == GenTableColumnModel.table_id"
    )

    ......
```
修改后：指定异步安全的加载策略
```python
    # 关联关系
    # 指定异步安全的加载策略
    columns: Mapped[list["GenTableColumnModel"]] = relationship(
        "GenTableColumnModel", # 增加
        order_by="GenTableColumnModel.sort",
        back_populates="table",
        cascade="all, delete-orphan",
        lazy="selectin",  # 增加：使用异步安全的selectin加载
        primaryjoin="GenTableModel.id == GenTableColumnModel.table_id"
    )
```

2. backend/app/plugin/module_generator/gencode/model.py 
- class GenTableColumnModel
原始：
```python
    # 关联关系
    table: Mapped["GenTableModel"] = relationship(
        back_populates="columns",
        primaryjoin="GenTableColumnModel.table_id == GenTableModel.id",
    )
```
修改后：指定异步安全的加载策略
```python
    # 关联关系
    # table: Mapped["GenTableModel"] = relationship(back_populates="columns")
    table: Mapped["GenTableModel"] = relationship(
        "GenTableModel", # 增加
        back_populates="columns",
        lazy="selectin",  # 增加：使用异步安全的selectin加载
        primaryjoin="GenTableColumnModel.table_id == GenTableModel.id",
    )
```

3. backend/app/plugin/module_generator/gencode/service.py 
```python
# async def get_gen_table_list_service
gen_table_list_result = await GenTableCRUD(auth=auth).get_gen_table_list(search)

# 修改为：指定预加载
gen_table_list_result = await GenTableCRUD(auth=auth).get_gen_table_list(
    search, 
    preload=["columns"]  # 指定预加载
)
```

## 代码生成
1. 生成代码，需更改 backend/app/plugin/module_generator/gencode/templates/python/controller.py.j2

- 增加: 
```python
......
from app.core.router_class import OperationLogRoute
......
```

- 修改: 
```python
{{ class_name }}Router = APIRouter(prefix='/{{ business_name }}', tags=["{{ function_name }}模块"]) 

# 改为： 
{{ class_name }}Router = APIRouter(route_class=OperationLogRoute, prefix='/{{ business_name }}', tags=["{{ function_name }}模块"])

```