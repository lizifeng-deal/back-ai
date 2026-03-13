"""
蓝图模块初始化
"""
from .auth import auth_bp
from .deallog import deallog_bp
from .positions import positions_bp

__all__ = ['auth_bp', 'deallog_bp', 'positions_bp']