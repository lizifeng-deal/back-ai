# 项目结构说明

本文档描述了重新组织后的Flask项目结构，采用了清晰的模块化设计。

## 📁 项目目录结构

```
back-ai/
├── app/                        # 应用核心模块
│   ├── __init__.py            # 应用工厂函数
│   ├── models/                # 数据模型
│   │   ├── __init__.py
│   │   ├── user.py           # 用户模型
│   │   ├── deallog.py        # 交易日志模型
│   │   └── position.py       # 持仓模型
│   ├── blueprints/            # 路由蓝图
│   │   ├── __init__.py
│   │   ├── auth.py           # 认证相关路由
│   │   ├── deallog.py        # 交易日志路由
│   │   └── positions.py      # 持仓管理路由
│   └── utils/                 # 工具函数
│       ├── __init__.py
│       ├── validators.py      # 数据验证器
│       ├── deallog_ops.py     # 交易日志业务逻辑
│       └── positions_ops.py   # 持仓业务逻辑
├── config/                    # 配置文件
│   └── config.py             # 应用配置
├── scripts/                   # 脚本文件
│   └── create_admin.py       # 创建管理员脚本
├── tests/                     # 测试文件
│   └── test_auth.py          # 认证模块测试
├── docs/                      # 文档
│   ├── LOGIN_API_DOCS.md     # API文档
│   ├── LOGIN_README.md       # 登录模块说明
│   └── PROJECT_STRUCTURE.md  # 项目结构说明（本文件）
├── debug_tools/               # 调试工具（保持原有结构）
├── instance/                  # 实例文件夹
│   └── app.db                # SQLite数据库
├── vendor/                    # 第三方依赖（如存在）
├── run.py                     # 应用启动文件
├── requirements.txt           # Python依赖
└── README.md                 # 项目说明
```

## 🏗️ 架构设计

### 应用工厂模式
- `app/__init__.py` - 使用应用工厂函数 `create_app()` 创建Flask应用实例
- 支持多环境配置（开发、测试、生产）
- 扩展初始化集中管理

### 数据模型层 (Models)
- `app/models/` - 所有数据模型统一管理
- 每个模型独立文件，便于维护
- 包含模型定义和相关方法

### 路由蓝图层 (Blueprints)
- `app/blueprints/` - 按功能模块组织路由
- 每个蓝图负责特定业务领域
- 路由和视图函数分离

### 业务逻辑层 (Utils)
- `app/utils/` - 业务逻辑和工具函数
- 数据验证、业务操作等功能
- 可复用的通用功能

### 配置管理 (Config)
- `config/` - 统一的配置管理
- 支持多环境配置
- 敏感信息通过环境变量管理

## 📋 功能模块

### 🔐 认证模块 (Auth)
- **模型**: `app/models/user.py` - 用户数据模型
- **路由**: `app/blueprints/auth.py` - 认证相关API
- **验证**: `app/utils/validators.py` - 数据验证功能

**功能特性**:
- 用户注册和登录
- 密码加密存储
- 会话管理
- 用户信息管理

### 💰 交易日志模块 (DealLog)
- **模型**: `app/models/deallog.py` - 交易记录数据模型
- **路由**: `app/blueprints/deallog.py` - 交易日志API
- **逻辑**: `app/utils/deallog_ops.py` - 业务逻辑处理

**功能特性**:
- 交易记录CRUD操作
- 交割盈亏统计
- 多币种支持

### 📊 持仓管理模块 (Positions)
- **模型**: `app/models/position.py` - 持仓数据模型
- **路由**: `app/blueprints/positions.py` - 持仓管理API
- **逻辑**: `app/utils/positions_ops.py` - 业务逻辑处理

**功能特性**:
- 持仓记录管理
- 币安API集成
- 实时持仓查询

## 🚀 启动方式

### 开发环境
```bash
# 直接启动
python run.py

# 或设置环境变量
set FLASK_ENV=development
set FLASK_DEBUG=True
python run.py
```

### 生产环境
```bash
# 设置生产环境
set FLASK_ENV=production
set SECRET_KEY=your-secret-key
python run.py

# 或使用WSGI服务器
gunicorn -w 4 -b 0.0.0.0:3000 run:app
```

## 🛠️ 管理脚本

### 创建管理员用户
```bash
cd scripts
python create_admin.py
```

### 运行测试
```bash
cd tests
python test_auth.py
```

## 🔧 配置说明

### 环境变量
- `FLASK_ENV` - 运行环境 (development/production/testing)
- `FLASK_HOST` - 监听地址 (默认: 0.0.0.0)
- `FLASK_PORT` - 监听端口 (默认: 3000)
- `FLASK_DEBUG` - 调试模式 (默认: True)
- `SECRET_KEY` - 会话密钥 (生产环境必须设置)
- `DATABASE_URL` - 数据库连接字符串

### 数据库配置
- 开发环境: SQLite (`sqlite:///app.db`)
- 生产环境: 可通过 `DATABASE_URL` 环境变量配置
- 支持PostgreSQL、MySQL等数据库

## 📚 扩展开发

### 添加新功能模块

1. **创建数据模型**
   ```python
   # app/models/new_model.py
   from app import db
   
   class NewModel(db.Model):
       # 模型定义
   ```

2. **创建路由蓝图**
   ```python
   # app/blueprints/new_module.py
   from flask import Blueprint
   
   new_bp = Blueprint('new_module', __name__)
   
   @new_bp.route('/new-endpoint')
   def new_endpoint():
       # 路由处理
   ```

3. **注册蓝图**
   ```python
   # app/__init__.py
   from app.blueprints.new_module import new_bp
   app.register_blueprint(new_bp)
   ```

4. **添加业务逻辑**
   ```python
   # app/utils/new_module_ops.py
   def new_operation():
       # 业务逻辑
   ```

### 数据库迁移
使用Flask-Migrate进行数据库版本控制:
```bash
pip install Flask-Migrate
flask db init
flask db migrate -m "Add new table"
flask db upgrade
```

## 🔒 安全考虑

1. **生产环境配置**:
   - 设置强密码作为 `SECRET_KEY`
   - 使用HTTPS协议
   - 配置安全的会话设置

2. **数据库安全**:
   - 定期备份数据库
   - 使用环境变量管理敏感信息
   - 限制数据库访问权限

3. **API安全**:
   - 输入验证和清理
   - 访问频率限制
   - 错误信息脱敏

## 📝 开发规范

### 代码组织
- 按功能模块组织代码
- 单一职责原则
- 接口与实现分离

### 命名规范
- 文件名: 小写字母和下划线
- 类名: 驼峰命名
- 函数名: 小写字母和下划线
- 常量: 大写字母和下划线

### 文档规范
- 每个模块都有说明文档
- API接口详细文档
- 重要函数添加注释

## 🤝 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 创建Pull Request
5. 代码审查和合并

## 📞 技术支持

如有问题或建议，请：
1. 查看文档
2. 检查测试用例
3. 提交Issue
4. 联系开发团队