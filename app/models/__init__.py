"""
数据模型模块初始化
"""
from app import db

# 导入所有模型
from .user import User
from .deallog import DealLog
from .position import Position

__all__ = ['User', 'DealLog', 'Position', 'db']