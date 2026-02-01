# -*- coding: utf-8 -*-

import datetime
from sqlalchemy import DateTime, String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixinModify, UserMixin


class TeamTest22Model(ModelMixinModify, UserMixin):
    """
    测试22表
    """
    __tablename__: str = 'team_test22'
    __table_args__: dict[str, str] = {'comment': '测试22'}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    name: Mapped[str | None] = mapped_column(String(255), nullable=True, comment='课题名称')
    content: Mapped[str | None] = mapped_column(Text, nullable=True, comment='课题简介')
    file_path: Mapped[str | None] = mapped_column(Text, nullable=True, comment='本地文件')
    image_path: Mapped[str | None] = mapped_column(Text, nullable=True, comment='本地图片')

