我来逐句解读这段代码：

## 1. 导入和类定义

```python
from typing import Any
```
导入 Python 的类型提示模块，`Any` 表示任意类型。

```python
from sqlalchemy import select
```
导入 SQLAlchemy 的查询构造器。

```python
from sqlalchemy.sql.elements import ColumnElement
```
导入 SQLAlchemy 的列表达式元素类型，用于类型提示。

```python
from app.api.v1.module_system.auth.schema import AuthSchema
```
导入认证模式的 Schema 类，用于类型验证和序列化。

```python
from app.api.v1.module_system.dept.model import DeptModel
from app.api.v1.module_system.user.model import UserModel
```
导入部门和用户的数据库模型。

```python
from app.utils.common_util import get_child_id_map, get_child_recursion
```
导入工具函数，用于获取子节点映射和递归获取子节点。

```python
class Permission:
    """
    为业务模型提供数据权限过滤功能
    """
```
定义 `Permission` 类，用于处理数据权限过滤。

## 2. 数据权限常量定义

```python
    DATA_SCOPE_SELF = 1  # 仅本人数据
    DATA_SCOPE_DEPT = 2  # 本部门数据
    DATA_SCOPE_DEPT_AND_CHILD = 3  # 本部门及以下数据
    DATA_SCOPE_ALL = 4  # 全部数据
    DATA_SCOPE_CUSTOM = 5  # 自定义数据
```
定义数据权限范围的常量，提高代码可读性。

## 3. 初始化方法

```python
    def __init__(self, model: Any, auth: AuthSchema) -> None:
```
初始化方法，接收数据模型和认证信息。

```python
        """
        初始化权限过滤器实例

        Args:
            db: 数据库会话
            model: 数据模型类
            current_user: 当前用户对象
            auth: 认证信息对象
        """
```
方法文档字符串（注意：参数描述中有 db 和 current_user，但实际参数只有 model 和 auth，可能存在文档错误）。

```python
        self.model = model
        self.auth = auth
        self.conditions: list[ColumnElement] = []  # 权限条件列表
```
初始化实例变量：
- `self.model`: 要查询的数据模型
- `self.auth`: 认证信息对象
- `self.conditions`: 权限条件列表（虽然定义了，但后面代码中并未使用这个列表）

## 4. 查询过滤方法

```python
    async def filter_query(self, query: Any) -> Any:
        """
        异步过滤查询对象

        Args:
            query: SQLAlchemy查询对象

        Returns:
            过滤后的查询对象
        """
```
异步方法，用于过滤查询对象。

```python
        condition = await self.__permission_condition()
```
调用私有方法获取权限条件（异步）。

```python
        return query.where(condition) if condition is not None else query
```
如果有条件，添加到查询的 where 子句中；否则返回原查询。

## 5. 核心权限条件生成方法

```python
    async def __permission_condition(self) -> ColumnElement | None:
```
私有异步方法，生成权限过滤条件，返回 SQLAlchemy 列表达式或 None。

```python
        """
        应用数据范围权限隔离
        基于角色的五种数据权限范围过滤
        支持五种权限类型：
        1. 仅本人数据权限 - 只能查看自己创建的数据
        2. 本部门数据权限 - 只能查看同部门的数据
        3. 本部门及以下数据权限 - 可以查看本部门及所有子部门的数据
        4. 全部数据权限 - 可以查看所有数据
        5. 自定义数据权限 - 通过role_dept_relation表定义可访问的部门列表

        权限处理原则：
        - 多个角色的权限取并集（最宽松原则）
        - 优先级：全部数据 > 部门权限（2、3、5的并集） > 仅本人
        - 构造权限过滤表达式，返回None表示不限制
        """
```
详细说明权限处理逻辑。

## 6. 基础检查

```python
        # 如果不需要检查数据权限,则不限制
        if not self.auth.user:
            return None
```
如果没有用户信息，不限制。

```python
        # 如果检查数据权限为False,则不限制
        if not self.auth.check_data_scope:
            return None
```
如果配置为不检查数据权限，不限制。

```python
        # 如果模型没有创建人created_id字段,则不限制
        if not hasattr(self.model, "created_id"):
            return None
```
如果数据模型没有 `created_id` 字段，无法进行权限过滤，不限制。

```python
        # 超级管理员可以查看所有数据
        if self.auth.user.is_superuser:
            return None
```
超级管理员拥有所有数据权限，不限制。

## 7. 处理无角色用户

```python
        # 如果用户没有角色,则只能查看自己的数据
        roles = getattr(self.auth.user, "roles", []) or []
        if not roles:
            created_id_attr = getattr(self.model, "created_id", None)
            if created_id_attr is not None:
                return created_id_attr == self.auth.user.id
            return None
```
如果用户没有分配角色，只能查看自己创建的数据。

## 8. 收集角色权限信息

```python
        # 获取用户所有角色的权限范围
        data_scopes = set()
        custom_dept_ids = set()  # 自定义权限（data_scope=5）关联的部门ID集合

        for role in roles:
            data_scopes.add(role.data_scope)
            # 收集自定义权限（data_scope=5）关联的部门ID
            if role.data_scope == self.DATA_SCOPE_CUSTOM and hasattr(role, "depts") and role.depts:
                custom_dept_ids.update(dept.id for dept in role.depts)
```
遍历用户所有角色：
- 收集所有数据权限类型
- 收集自定义权限关联的部门 ID

## 9. 处理最高权限级别

```python
        # 权限优先级处理：全部数据权限最高优先级
        if self.DATA_SCOPE_ALL in data_scopes:
            return None
```
如果用户有任意角色拥有"全部数据"权限，不限制（最高优先级）。

## 10. 处理部门相关权限

```python
        # 收集所有可访问的部门ID（2、3、5权限的并集）
        accessible_dept_ids = set()
        user_dept_id = getattr(self.auth.user, "dept_id", None)
```
初始化可访问部门 ID 集合，获取用户所属部门 ID。

```python
        # 处理自定义数据权限（5）
        if self.DATA_SCOPE_CUSTOM in data_scopes:
            accessible_dept_ids.update(custom_dept_ids)
```
添加自定义权限的部门 ID。

```python
        # 处理本部门数据权限（2）
        if self.DATA_SCOPE_DEPT in data_scopes and user_dept_id is not None:
            accessible_dept_ids.add(user_dept_id)
```
添加本部门权限的部门 ID。

```python
        # 处理本部门及以下数据权限（3）
        if self.DATA_SCOPE_DEPT_AND_CHILD in data_scopes and user_dept_id is not None:
            try:
                # 查询所有部门并递归获取子部门
                dept_sql = select(DeptModel)
                dept_result = await self.auth.db.execute(dept_sql)
                dept_objs = dept_result.scalars().all()
                id_map = get_child_id_map(dept_objs)
                # get_child_recursion返回的结果已包含自身ID和所有子部门ID
                dept_with_children_ids = get_child_recursion(id=user_dept_id, id_map=id_map)
                accessible_dept_ids.update(dept_with_children_ids)
            except Exception:
                # 查询失败时降级到本部门
                accessible_dept_ids.add(user_dept_id)
```
处理本部门及以下权限：
1. 查询所有部门数据
2. 构建部门父子关系映射
3. 递归获取用户部门的所有子部门 ID
4. 失败时降级为仅本部门权限

## 11. 根据部门权限构建查询条件

```python
        # 如果有部门权限（2、3、5任一），使用部门过滤
        if accessible_dept_ids:
            creator_rel = getattr(self.model, "created_by", None)
            # 优先使用关系过滤（性能更好）
            if creator_rel is not None and hasattr(UserModel, "dept_id"):
                return creator_rel.has(UserModel.dept_id.in_(list(accessible_dept_ids)))
            # 降级方案：如果模型没有created_by关系但有created_id，则只能查看自己的数据
            created_id_attr = getattr(self.model, "created_id", None)
            if created_id_attr is not None:
                return created_id_attr == self.auth.user.id
            return None
```
如果有可访问的部门 ID：
- 优先使用模型关系过滤（通过 `created_by` 关系找到创建者，再过滤其部门）
- 如果没有关系，降级为仅能查看自己的数据

## 12. 处理仅本人权限

```python
        # 处理仅本人数据权限（1）
        if self.DATA_SCOPE_SELF in data_scopes:
            created_id_attr = getattr(self.model, "created_id", None)
            if created_id_attr is not None:
                return created_id_attr == self.auth.user.id
            return None
```
如果只有"仅本人"权限，返回条件：创建者 ID 等于当前用户 ID。

## 13. 默认情况

```python
        # 默认情况：如果用户有角色但没有任何有效权限范围，只能查看自己的数据
        created_id_attr = getattr(self.model, "created_id", None)
        if created_id_attr is not None:
            return created_id_attr == self.auth.user.id
        return None
```
默认安全策略：如果用户有角色但没有匹配的权限范围，只能查看自己的数据。

## 总结

这个类实现了基于角色的数据权限过滤系统，特点包括：
1. **多角色权限合并**：用户多个角色的权限取并集
2. **权限优先级**：全部权限 > 部门相关权限 > 仅本人权限
3. **灵活的部门权限**：支持本部门、本部门及子部门、自定义部门
4. **优雅降级**：在查询失败或模型不支持时，降级为更安全的权限策略
5. **异步支持**：支持异步数据库查询

这是一个典型的企业级权限管理系统组件，常用于多租户、多部门的数据隔离场景。

### 一、代码整体架构说明
上传的代码涵盖**前端权限配置组件**、**后端接口/模型/CRUD/权限过滤逻辑**，实现了「菜单权限（功能权限）」和「数据权限（范围权限）」的完整闭环。核心逻辑分为：
- 菜单权限：控制用户能访问哪些菜单/按钮（功能层面）；
- 数据权限：控制用户能查看/操作哪些业务数据（范围层面）。

### 二、菜单权限（功能权限）实现
菜单权限核心是「角色-菜单」多对多关联，前端可视化配置、后端持久化存储并在查询时校验。

#### 1. 数据层：角色-菜单关联（model.py）
定义多对多关联表，存储角色与菜单的绑定关系：
```python
# 角色-菜单关联表（多对多）
class RoleMenusModel(MappedBase):
    __tablename__ = "sys_role_menus"
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("sys_role.id"), primary_key=True)
    menu_id: Mapped[int] = mapped_column(Integer, ForeignKey("sys_menu.id"), primary_key=True)

# 角色模型关联菜单
class RoleModel(ModelMixin):
    menus: Mapped[list["MenuModel"]] = relationship(
        secondary="sys_role_menus",  # 指定关联表
        back_populates="roles",
        lazy="selectin"  # 懒加载菜单数据
    )
```

#### 2. 操作层：菜单权限赋值（crud.py）
`set_role_menus_crud` 实现角色菜单权限的「清空-重绑」逻辑：
```python
async def set_role_menus_crud(self, role_ids: list[int], menu_ids: list[int]) -> None:
    # 1. 查询目标角色和菜单
    roles = await self.list(search={"id": ("in", role_ids)})
    menus = await MenuCRUD(self.auth).get_list_crud(search={"id": ("in", menu_ids)})
    # 2. 清空原有菜单关联，绑定新菜单
    for obj in roles:
        obj.menus.clear()  # 清空旧权限
        obj.menus.extend(menus)  # 绑定新权限
    await self.auth.db.flush()  # 刷入数据库
```

#### 3. 接口层：权限配置接口（controller.py）
暴露 `PATCH /role/permission/setting` 接口，接收前端配置的菜单权限：
```python
@RoleRouter.patch("/permission/setting", summary="角色授权")
async def set_role_permission_controller(
    data: RolePermissionSettingSchema,  # 包含menu_ids/role_ids
    auth: Annotated[AuthSchema, Depends(AuthPermission(["module_system:role:permission"]))],
) -> JSONResponse:
    await RoleService.set_role_permission_service(data=data, auth=auth)
    return SuccessResponse(msg="授权角色成功")
```

#### 4. 前端层：可视化配置（PermissonDrawer.vue）
- 加载菜单树：通过 `MenuAPI.listMenu()` 获取所有菜单，渲染成可勾选的树形结构；
- 回显已有权限：打开抽屉时，通过 `RoleAPI.detailRole(roleId)` 获取角色已绑定的 `menu_ids`，用 `setCheckedKeys` 回显勾选状态；
- 提交配置：收集勾选的菜单ID，调用 `RoleAPI.setPermission` 提交：
```typescript
async function handleDrawerSave() {
  const submitData: permissionDataType = {
    role_ids: [props.roleId],
    menu_ids: (permTreeRef.value?.getCheckedKeys() || []).map(Number), // 选中的菜单ID
    data_scope: permissionState.value.data_scope,
    dept_ids: (deptTreeRef.value?.getCheckedKeys() || []).map(Number),
  };
  await RoleAPI.setPermission(submitData); // 提交菜单/数据权限配置
}
```

### 三、数据权限（范围权限）实现
数据权限控制用户能访问**哪些范围的业务数据**（如仅本人、本部门、自定义部门），核心是 `data_scope` 字段 + 动态查询过滤。

#### 1. 核心字段：data_scope（model.py/schema.py）
- 角色表 `sys_role` 的 `data_scope` 字段定义权限范围：
  ```python
  # model.py 角色模型
  data_scope: Mapped[int] = mapped_column(
      Integer, default=1, comment="1:仅本人 2:本部门 3:本部门及以下 4:全部 5:自定义"
  )

  # schema.py 数据权限配置模型
  class RolePermissionSettingSchema(BaseModel):
      data_scope: int = Field(description="数据权限范围(1-5)")
      dept_ids: list[int] = Field(description="自定义部门ID（仅data_scope=5时生效）")
  ```
- 自定义数据权限依赖 `RoleDeptsModel`（角色-部门多对多表），仅 `data_scope=5` 时存储角色可访问的部门：
  ```python
  class RoleDeptsModel(MappedBase):
      __tablename__ = "sys_role_depts"
      role_id: Mapped[int] = mapped_column(Integer, ForeignKey("sys_role.id"), primary_key=True)
      dept_id: Mapped[int] = mapped_column(Integer, ForeignKey("sys_dept.id"), primary_key=True)
  ```

#### 2. 权限赋值：data_scope + 自定义部门（crud.py/service.py）
- `set_role_data_scope_crud`：批量更新角色的 `data_scope` 字段；
- `set_role_depts_crud`：仅 `data_scope=5` 时，绑定角色与自定义部门：
  ```python
  # service.py 核心逻辑
  @classmethod
  async def set_role_permission_service(cls, auth: AuthSchema, data: RolePermissionSettingSchema) -> None:
      # 1. 设置菜单权限
      await RoleCRUD(auth).set_role_menus_crud(role_ids=data.role_ids, menu_ids=data.menu_ids)
      # 2. 设置数据权限范围（data_scope）
      await RoleCRUD(auth).set_role_data_scope_crud(role_ids=data.role_ids, data_scope=data.data_scope)
      # 3. 自定义数据权限：绑定部门（非5则清空）
      if data.data_scope == 5 and data.dept_ids:
          await RoleCRUD(auth).set_role_depts_crud(role_ids=data.role_ids, dept_ids=data.dept_ids)
      else:
          await RoleCRUD(auth).set_role_depts_crud(role_ids=data.role_ids, dept_ids=[])
  ```

#### 3. 核心过滤：动态数据权限（permission.py）
`Permission` 类是数据权限的核心，会**自动为业务查询添加过滤条件**：
```python
class Permission:
    async def filter_query(self, query: Any) -> Any:
        """为查询对象添加数据权限过滤条件"""
        condition = await self.__permission_condition()
        return query.where(condition) if condition is not None else query

    async def __permission_condition(self) -> ColumnElement | None:
        # 超级管理员：无过滤
        if self.auth.user.is_superuser:
            return None
        
        # 提取用户角色的data_scope
        roles = self.auth.user.roles or []
        data_scopes = {role.data_scope for role in roles}
        
        # 1. data_scope=1（仅本人）：过滤created_id=当前用户ID
        if self.DATA_SCOPE_SELF in data_scopes:
            return getattr(self.model, "created_id") == self.auth.user.id
        
        # 2. data_scope=2（本部门）：过滤创建人部门=当前用户部门
        if self.DATA_SCOPE_DEPT in data_scopes:
            return creator_rel.has(UserModel.dept_id == self.auth.user.dept_id)
        
        # 3. data_scope=3（本部门及以下）：递归获取子部门并过滤
        if self.DATA_SCOPE_DEPT_AND_CHILD in data_scopes:
            dept_with_children_ids = get_child_recursion(id=user_dept_id, id_map=id_map)
            return creator_rel.has(UserModel.dept_id.in_(dept_with_children_ids))
        
        # 4. data_scope=4（全部）：无过滤
        if self.DATA_SCOPE_ALL in data_scopes:
            return None
        
        # 5. data_scope=5（自定义）：过滤创建人部门在角色绑定的dept_ids中
        if self.DATA_SCOPE_CUSTOM in data_scopes:
            custom_dept_ids = {dept.id for role in roles for dept in role.depts}
            return creator_rel.has(UserModel.dept_id.in_(custom_dept_ids))
        
        # 默认：仅本人
        return getattr(self.model, "created_id") == self.auth.user.id
```

#### 4. 前端配置：数据权限选择（PermissonDrawer.vue）
- 下拉选择 `data_scope`（仅本人/本部门/自定义等）；
- 当 `data_scope=5` 时，渲染部门树，支持勾选自定义部门：
  ```vue
  <el-select v-model="permissionState.data_scope">
    <el-option :key="1" label="仅本人数据权限" :value="1" />
    <el-option :key="5" label="自定义数据权限" :value="5" />
  </el-select>
  <!-- 自定义部门树（仅data_scope=5时显示） -->
  <el-tree
    v-if="permissionState.data_scope === 5"
    ref="deptTreeRef"
    show-checkbox
    :data="deptTreeData"
    @check="deptTreeCheck"
  />
  ```

### 四、核心流程总结
| 权限类型 | 配置流程                                                                 | 生效逻辑                                                                 |
|----------|--------------------------------------------------------------------------|--------------------------------------------------------------------------|
| 菜单权限 | 前端勾选菜单 → 提交menu_ids → 后端更新sys_role_menus表                   | 前端路由/按钮根据菜单权限控制显示，后端接口校验权限码                     |
| 数据权限 | 前端选择data_scope → （自定义时勾选部门）→ 后端更新data_scope/dept_ids   | 业务查询时，Permission类自动生成过滤条件，仅返回权限范围内的数据         |

### 关键亮点
1. **权限解耦**：菜单权限（功能）和数据权限（范围）分离，可独立配置；
2. **动态过滤**：数据权限无需修改业务代码，通过Permission类自动注入过滤条件；
3. **多角色兼容**：多角色权限取「并集」（最宽松原则），符合业务实际场景；
4. **前端可视化**：树形结构+父子联动+筛选，降低配置复杂度。

# 修改方案
## 1. 首页数据
- 确保首页路由不校验登录、首页数据模型`无权限拦截`。
- 在首页对应的接口路由中，移除AuthPermission依赖（或配置匿名访问）
### 需求
- 打开网站后，进入首页，首页中没有菜单，相当于门户网站页
- 登录后，根据角色+部门+岗位，进入不同的界面，菜单不同