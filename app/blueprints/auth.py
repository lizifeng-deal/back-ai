"""
认证蓝图 - 处理用户登录、注册等认证相关功能
"""
from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app import db
from app.utils.validators import validate_username, validate_password, validate_email

# 创建认证蓝图
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': '请提供JSON数据'}), 400
        
        username = data.get('username', '').strip()
        password = data.get('password', '')
        email = data.get('email', '').strip() if data.get('email') else None
        
        # 验证用户名
        valid, msg = validate_username(username)
        if not valid:
            return jsonify({'error': msg}), 400
        
        # 验证密码
        valid, msg = validate_password(password)
        if not valid:
            return jsonify({'error': msg}), 400
        
        # 验证邮箱
        if email:
            valid, msg = validate_email(email)
            if not valid:
                return jsonify({'error': msg}), 400
        
        # 检查用户是否已存在
        if User.query.filter_by(username=username).first():
            return jsonify({'error': '用户名已存在'}), 409
        
        if email and User.query.filter_by(email=email).first():
            return jsonify({'error': '邮箱已被注册'}), 409
        
        # 创建新用户
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': '注册成功',
            'user': user.to_dict()
        }), 201
        
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': '用户名或邮箱已存在'}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'注册失败: {str(e)}'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': '请提供JSON数据'}), 400
        
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({'error': '用户名和密码不能为空'}), 400
        
        # 查找用户
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.check_password(password):
            return jsonify({'error': '用户名或密码错误'}), 401
        
        if not user.is_active:
            return jsonify({'error': '账户已被禁用'}), 403
        
        # 登录用户
        login_user(user, remember=True)
        user.update_last_login()
        db.session.commit()
        
        return jsonify({
            'message': '登录成功',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'登录失败: {str(e)}'}), 500

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """用户登出"""
    try:
        logout_user()
        return jsonify({'message': '登出成功'}), 200
    except Exception as e:
        return jsonify({'error': f'登出失败: {str(e)}'}), 500

@auth_bp.route('/profile', methods=['GET'])
@login_required
def get_profile():
    """获取当前用户信息"""
    try:
        return jsonify({
            'user': current_user.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'error': f'获取用户信息失败: {str(e)}'}), 500

@auth_bp.route('/profile', methods=['PUT'])
@login_required
def update_profile():
    """更新用户信息"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': '请提供JSON数据'}), 400
        
        email = data.get('email', '').strip() if data.get('email') else None
        
        # 验证邮箱
        if email:
            valid, msg = validate_email(email)
            if not valid:
                return jsonify({'error': msg}), 400
            
            # 检查邮箱是否已被其他用户使用
            existing_user = User.query.filter_by(email=email).first()
            if existing_user and existing_user.id != current_user.id:
                return jsonify({'error': '邮箱已被其他用户使用'}), 409
        
        # 更新用户信息
        current_user.email = email
        db.session.commit()
        
        return jsonify({
            'message': '用户信息更新成功',
            'user': current_user.to_dict()
        }), 200
        
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': '邮箱已被使用'}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'更新失败: {str(e)}'}), 500

@auth_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    """修改密码"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': '请提供JSON数据'}), 400
        
        current_password = data.get('current_password', '')
        new_password = data.get('new_password', '')
        
        if not current_password or not new_password:
            return jsonify({'error': '当前密码和新密码不能为空'}), 400
        
        # 验证当前密码
        if not current_user.check_password(current_password):
            return jsonify({'error': '当前密码错误'}), 401
        
        # 验证新密码
        valid, msg = validate_password(new_password)
        if not valid:
            return jsonify({'error': msg}), 400
        
        # 更新密码
        current_user.set_password(new_password)
        db.session.commit()
        
        return jsonify({'message': '密码修改成功'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'修改密码失败: {str(e)}'}), 500

@auth_bp.route('/status', methods=['GET'])
def get_auth_status():
    """获取认证状态"""
    try:
        if current_user.is_authenticated:
            return jsonify({
                'authenticated': True,
                'user': current_user.to_dict()
            }), 200
        else:
            return jsonify({
                'authenticated': False,
                'user': None
            }), 200
    except Exception as e:
        return jsonify({'error': f'获取认证状态失败: {str(e)}'}), 500