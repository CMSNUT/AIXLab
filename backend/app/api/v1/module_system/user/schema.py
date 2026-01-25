from urllib.parse import urlparse
import re

from fastapi import Query
from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
    model_validator,
)

from app.api.v1.module_system.menu.schema import MenuOutSchema
from app.api.v1.module_system.role.schema import RoleOutSchema
from app.core.base_schema import BaseSchema, CommonSchema, UserBySchema
from app.core.validator import DateTimeStr, email_validator, mobile_validator

# 抽离通用的username验证逻辑，避免重复代码
def validate_username_common(value: str) -> str:
    """通用的账号（学号/工号）验证函数"""
    v = value.strip()
    if not v:
        raise ValueError("账号不能为空")
    
    # 🌟 超管账号白名单：需要豁免数字校验的账号加在这里！
    ADMIN_WHITELIST = {"admin"}  # 可添加其他超管，如{"admin", "root", "super"}
    if v in ADMIN_WHITELIST:
        return v  # 白名单账号直接通过，跳过后续数字校验
    
    # 普通账号：严格校验6-12位纯数字、以0/1/2开头
    pattern = r"^[0-2]\d{5,11}$"
    if not re.fullmatch(pattern, v):
        if not re.fullmatch(r"^\d+$", v):
            raise ValueError("账号是学号或工号，仅允许输入数字（不能包含汉字、字母、符号等）")
        else:
            raise ValueError("账号是学号或工号，需6-12位数字且以0/1/2开头")
    return v


class CurrentUserUpdateSchema(BaseModel):
    """基础用户信息"""

    name: str | None = Field(default=None, description="名称")
    mobile: str | None = Field(default=None, description="手机号")
    email: EmailStr | None = Field(default=None, description="邮箱")
    gender: str | None = Field(default=None, description="性别")
    avatar: str | None = Field(default=None, description="头像")

    @field_validator("mobile")
    @classmethod
    def validate_mobile(cls, value: str | None):
        return mobile_validator(value)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str | None):
        if not value:
            return value
        return email_validator(value)

    @field_validator("avatar")
    @classmethod
    def validate_avatar(cls, value: str | None):
        if not value:
            return value
        parsed = urlparse(value)
        if parsed.scheme in ("http", "https") and parsed.netloc:
            return value
        raise ValueError("头像地址需为有效的HTTP/HTTPS URL")

    @model_validator(mode="after")
    def check_model(self):
        if self.name and len(self.name) > 20:
            raise ValueError("名称长度不能超过20个字符")
        return self


class UserRegisterSchema(BaseModel):
    """注册"""

    name: str | None = Field(default=None, description="真实姓名")
    mobile: str | None = Field(default=None, description="手机号")
    username: str = Field(..., description="账号，工号或学号")
    password: str = Field(..., description="密码哈希值")
    role_ids: list[int] | None = Field(default=[2], description="角色ID，默认普通用户(role_id=2)")
    created_id: int | None = Field(default=1, description="创建人ID")
    description: str | None = Field(default=None, max_length=255, description="备注")

    @field_validator("mobile")
    @classmethod
    def validate_mobile(cls, value: str | None):
        return mobile_validator(value)

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str):
        return validate_username_common(value)  # 复用通用验证逻辑

    @model_validator(mode="after")
    def check_model(self):
        if self.name and len(self.name) > 20:
            raise ValueError("名称长度不能超过20个字符")
        if self.username and len(self.username) > 12:
            raise ValueError("账号长度不能超过12个字符")
        if self.description and len(self.description) > 255:
            raise ValueError("备注长度不能超过255个字符")
        if self.password and len(self.password) > 128:
            raise ValueError("密码长度不能超过128个字符")
        return self


class UserForgetPasswordSchema(BaseModel):
    """忘记密码"""

    username: str = Field(..., max_length=12, description="账号，工号或学号")
    new_password: str = Field(..., max_length=128, description="新密码")
    mobile: str | None = Field(default=None, description="手机号")

    @field_validator("mobile")
    @classmethod
    def validate_mobile(cls, value: str | None):
        return mobile_validator(value)
    
    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str):
        return validate_username_common(value)


class UserChangePasswordSchema(BaseModel):
    """修改密码"""

    old_password: str = Field(..., max_length=128, description="旧密码")
    new_password: str = Field(..., max_length=128, description="新密码")


class ResetPasswordSchema(BaseModel):
    """重置密码"""

    id: int = Field(..., description="主键ID")
    password: str = Field(..., min_length=6, max_length=128, description="新密码")


class UserCreateSchema(CurrentUserUpdateSchema):
    """新增"""

    model_config = ConfigDict(from_attributes=True)

    username: str | None = Field(default=None, max_length=12, description="账号，工号或学号")
    password: str | None = Field(default=None, max_length=128, description="密码哈希值")
    status: str = Field(default="0", description="是否可用")
    description: str | None = Field(default=None, max_length=255, description="备注")
    is_superuser: bool | None = Field(default=False, description="是否超管")
    dept_id: int | None = Field(default=None, description="部门ID")
    role_ids: list[int] | None = Field(default=[2], description="角色ID，默认普通用户(role_id=2)")
    position_ids: list[int] | None = Field(default=[], description="岗位ID")

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str | None):
        if not value:  # 允许None（因为字段是可选的），但有值时必须验证
            return value
        return validate_username_common(value)


class UserUpdateSchema(UserCreateSchema):
    """更新"""

    model_config = ConfigDict(from_attributes=True)

    last_login: DateTimeStr | None = Field(default=None, description="最后登录时间")


class UserOutSchema(UserUpdateSchema, BaseSchema, UserBySchema):
    """响应"""

    model_config = ConfigDict(arbitrary_types_allowed=True, from_attributes=True)
    gitee_login: str | None = Field(default=None, max_length=32, description="Gitee登录")
    github_login: str | None = Field(default=None, max_length=32, description="Github登录")
    wx_login: str | None = Field(default=None, max_length=32, description="微信登录")
    qq_login: str | None = Field(default=None, max_length=32, description="QQ登录")
    dept_name: str | None = Field(default=None, description="部门名称")
    dept: CommonSchema | None = Field(default=None, description="部门")
    positions: list[CommonSchema] | None = Field(default=[], description="岗位")
    roles: list[RoleOutSchema] | None = Field(default=[], description="角色")
    menus: list[MenuOutSchema] | None = Field(default=[], description="菜单")


class UserQueryParam:
    """用户管理查询参数"""

    def __init__(
        self,
        username: str | None = Query(None, description="账号，工号或学号"),
        name: str | None = Query(None, description="真实姓名"),
        mobile: str | None = Query(None, description="手机号", pattern=r"^1[3-9]\d{9}$"),
        email: str | None = Query(
            None,
            description="邮箱",
            pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
        ),
        dept_id: int | None = Query(None, description="部门ID"),
        status: str | None = Query(None, description="是否可用"),
        created_time: list[DateTimeStr] | None = Query(
            None,
            description="创建时间范围",
            examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"],
        ),
        updated_time: list[DateTimeStr] | None = Query(
            None,
            description="更新时间范围",
            examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"],
        ),
        created_id: int | None = Query(None, description="创建人"),
        updated_id: int | None = Query(None, description="更新人"),
    ) -> None:

        # 模糊查询字段
        self.username = ("like", username)
        self.name = ("like", name)
        self.mobile = ("like", mobile)
        self.email = ("like", email)

        # 精确查询字段
        self.dept_id = dept_id
        self.created_id = created_id
        self.updated_id = updated_id
        self.status = status

        # 时间范围查询
        if created_time and len(created_time) == 2:
            self.created_time = ("between", (created_time[0], created_time[1]))
        if updated_time and len(updated_time) == 2:
            self.updated_time = ("between", (updated_time[0], updated_time[1]))
