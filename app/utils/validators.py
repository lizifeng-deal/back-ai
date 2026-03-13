"""
数据验证工具函数
"""
import re

def validate_username(username):
    """验证用户名格式"""
    if not username or len(username) < 3 or len(username) > 80:
        return False, "用户名长度必须在3-80个字符之间"
    
    # 只允许字母、数字、下划线
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "用户名只能包含字母、数字和下划线"
    
    return True, ""

def validate_password(password):
    """验证密码格式"""
    if not password or len(password) < 6:
        return False, "密码长度至少6个字符"
    
    if len(password) > 128:
        return False, "密码长度不能超过128个字符"
    
    return True, ""

def validate_email(email):
    """验证邮箱格式"""
    if not email:
        return True, ""  # 邮箱可选
    
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        return False, "邮箱格式不正确"
    
    return True, ""