#!/usr/bin/env python3
"""
创建管理员用户的脚本
使用方法: python create_admin.py
"""

import sys
import os
from getpass import getpass

# 确保可以导入应用模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.models.user import User
from app import db

def create_admin_user():
    """创建管理员用户"""
    print("创建管理员用户")
    print("-" * 30)
    
    # 创建应用实例
    app = create_app()
    
    with app.app_context():
        # 获取用户输入
        while True:
            username = input("请输入管理员用户名 (3-80个字符，只能包含字母、数字和下划线): ").strip()
            if not username:
                print("用户名不能为空！")
                continue
            if len(username) < 3 or len(username) > 80:
                print("用户名长度必须在3-80个字符之间！")
                continue
            if not username.replace('_', '').isalnum():
                print("用户名只能包含字母、数字和下划线！")
                continue
            
            # 检查用户是否已存在
            if User.query.filter_by(username=username).first():
                print(f"用户名 '{username}' 已存在！")
                continue
            break
        
        # 获取邮箱（可选）
        email = input("请输入邮箱地址 (可选): ").strip()
        if email and '@' not in email:
            print("邮箱格式不正确，将跳过邮箱设置")
            email = None
        
        # 获取密码
        while True:
            password = getpass("请输入密码 (至少6个字符): ")
            if len(password) < 6:
                print("密码长度至少6个字符！")
                continue
            
            password_confirm = getpass("请再次输入密码确认: ")
            if password != password_confirm:
                print("两次密码输入不一致！")
                continue
            break
        
        try:
            # 创建管理员用户
            admin_user = User(
                username=username,
                email=email if email else None
            )
            admin_user.set_password(password)
            
            db.session.add(admin_user)
            db.session.commit()
            
            print(f"\n管理员用户创建成功！")
            print(f"用户名: {username}")
            if email:
                print(f"邮箱: {email}")
            print(f"用户ID: {admin_user.id}")
            print("\n您现在可以使用这个账户登录系统了。")
            
        except Exception as e:
            db.session.rollback()
            print(f"创建管理员用户失败: {str(e)}")
            return False
    
    return True

if __name__ == "__main__":
    try:
        create_admin_user()
    except KeyboardInterrupt:
        print("\n\n操作已取消。")
    except Exception as e:
        print(f"发生错误: {str(e)}")