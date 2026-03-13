#!/usr/bin/env python3
"""
Flask应用启动文件
"""
import os
import sys

# 添加vendor目录到Python路径（用于第三方依赖）
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "vendor"))

from app import create_app

# 创建应用实例
app = create_app(os.environ.get('FLASK_ENV', 'development'))

if __name__ == "__main__":
    # 开发环境启动配置
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 3000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"启动Flask应用...")
    print(f"地址: http://{host}:{port}")
    print(f"调试模式: {debug}")
    print(f"环境: {os.environ.get('FLASK_ENV', 'development')}")
    
    app.run(
        host=host,
        port=port,
        debug=debug,
        use_reloader=True
    )