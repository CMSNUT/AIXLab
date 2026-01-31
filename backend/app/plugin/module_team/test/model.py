# -*- coding: utf-8 -*-

import datetime
from sqlalchemy import Integer, String, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixinModify, UserMixin


class TeamTestModel(ModelMixinModify, UserMixin):
    """
    团队测试表
    """
    __tablename__: str = 'team_test'
    __table_args__: dict[str, str] = {'comment': '团队测试'}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    name: Mapped[str | None] = mapped_column(String(255), nullable=True, comment='课题名称')
    content: Mapped[str | None] = mapped_column(Text, nullable=True, comment='课题简介(富文本)')
    file_path: Mapped[str | None] = mapped_column(Text, nullable=True, comment='本地文件路径')
    imgage_path: Mapped[str | None] = mapped_column(Text, nullable=True, comment='本地图片路径')

