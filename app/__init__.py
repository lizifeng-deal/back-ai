"""
Flask应用初始化模块
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os

# 初始化扩展
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app(config_name='default'):
    """应用工厂函数"""
    app = Flask(__name__)
    
    # 加载配置
    from config.config import config
    app.config.from_object(config[config_name])
    
    # 初始化扩展
    db.init_app(app)
    bcrypt.init_app(app)
    
    # 配置Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = '请先登录'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        """加载用户回调函数"""
        from app.models.user import User
        return User.query.get(int(user_id))
    
    # 注册蓝图
    from app.blueprints.auth import auth_bp
    from app.blueprints.deallog import deallog_bp
    from app.blueprints.positions import positions_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(deallog_bp)
    app.register_blueprint(positions_bp)
    
    # 创建数据库表
    with app.app_context():
        db.create_all()
        
        # 处理数据库迁移
        from sqlalchemy import inspect, text
        insp = inspect(db.engine)
        tables = insp.get_table_names()
        if "dealLog" in tables:
            cols = [c["name"] for c in insp.get_columns("dealLog")]
            if "currency" not in cols:
                db.session.execute(text("ALTER TABLE dealLog ADD COLUMN currency VARCHAR(16)"))
                db.session.commit()
    
    return app