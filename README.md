# 交易管理系统 (Trading Management System)

一个基于Flask的交易管理系统，提供用户认证、交易日志记录、持仓管理等功能。

## 🌟 主要功能

### 🔐 用户认证系统
- 用户注册和登录
- 密码加密存储 (bcrypt)
- 会话管理 (Flask-Login)
- 用户信息管理

### 💰 交易日志管理
- 交易记录CRUD操作
- 存款、提款、交割盈亏记录
- 多币种支持 (USDT汇率转换)
- 交割盈亏统计

### 📊 持仓管理
- 持仓记录管理
- 币安API集成
- 实时持仓查询
- 多空持仓支持

### 🛠️ 调试工具
- 币安API诊断工具
- 系统状态检查
- API连接测试

## 🏗️ 项目结构

```
back-ai/
├── app/                    # 应用核心模块
│   ├── models/            # 数据模型
│   ├── blueprints/        # 路由蓝图
│   └── utils/             # 工具函数
├── config/                # 配置文件
├── scripts/               # 管理脚本
├── tests/                 # 测试文件
├── docs/                  # 项目文档
├── debug_tools/           # 调试工具
└── instance/              # 数据库文件
```

详细的项目结构说明请参考 [PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md)

## 🚀 快速开始

### 环境要求
- Python 3.7+
- SQLite 3
- 可选: 币安API账户

### 安装步骤

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd back-ai
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **配置环境变量** (可选)
   ```bash
   # Windows
   set SECRET_KEY=your-secret-key-here
   set BINANCE_API_KEY=your-binance-api-key
   set BINANCE_API_SECRET=your-binance-api-secret
   
   # Linux/Mac
   export SECRET_KEY=your-secret-key-here
   export BINANCE_API_KEY=your-binance-api-key
   export BINANCE_API_SECRET=your-binance-api-secret
   ```

4. **创建管理员用户**
   ```bash
   cd scripts
   python create_admin.py
   ```

5. **启动应用**
   ```bash
   python run.py
   ```

6. **访问应用**
   - API地址: `http://localhost:3000`
   - 认证状态: `http://localhost:3000/auth/status`

## 📡 API接口

### 认证接口
- `POST /auth/register` - 用户注册
- `POST /auth/login` - 用户登录
- `POST /auth/logout` - 用户登出
- `GET /auth/status` - 获取认证状态
- `GET /auth/profile` - 获取用户信息
- `PUT /auth/profile` - 更新用户信息
- `POST /auth/change-password` - 修改密码

### 交易日志接口
- `GET /dealLog` - 获取所有交易日志
- `GET /dealLog/{id}` - 获取特定交易日志
- `POST /dealLog` - 创建交易日志
- `PUT /dealLog/{id}` - 更新交易日志
- `DELETE /dealLog/{id}` - 删除交易日志
- `GET /dealLog/summary/delivery_pnl` - 交割盈亏统计

### 持仓管理接口
- `GET /positions` - 获取所有持仓记录
- `GET /positions/{id}` - 获取特定持仓记录
- `POST /positions` - 创建持仓记录
- `PUT /positions/{id}` - 更新持仓记录
- `DELETE /positions/{id}` - 删除持仓记录
- `GET /positions/binance` - 获取币安实时持仓
- `GET /positions/binance/test` - 测试币安连接

详细的API文档请参考 [LOGIN_API_DOCS.md](docs/LOGIN_API_DOCS.md)

## 🧪 测试

### 运行认证模块测试
```bash
cd tests
python test_auth.py
```

### 使用调试工具
```bash
cd debug_tools
python run_debug.py
```

## 🔧 配置说明

### 环境变量
| 变量名 | 描述 | 默认值 | 必需 |
|--------|------|--------|------|
| `SECRET_KEY` | Flask会话密钥 | auto-generated | 生产环境必需 |
| `FLASK_ENV` | 运行环境 | development | 否 |
| `FLASK_HOST` | 监听地址 | 0.0.0.0 | 否 |
| `FLASK_PORT` | 监听端口 | 3000 | 否 |
| `FLASK_DEBUG` | 调试模式 | True | 否 |
| `DATABASE_URL` | 数据库连接 | sqlite:///app.db | 否 |
| `BINANCE_API_KEY` | 币安API密钥 | - | 币安功能需要 |
| `BINANCE_API_SECRET` | 币安API密钥 | - | 币安功能需要 |

### 数据库配置
- 默认使用SQLite数据库
- 数据库文件位置: `instance/app.db`
- 支持MySQL、PostgreSQL等其他数据库
- 自动创建数据库表

## 📚 使用示例

### 用户注册和登录
```python
import requests

# 注册用户
response = requests.post('http://localhost:3000/auth/register', json={
    'username': 'myuser',
    'password': 'mypassword',
    'email': 'user@example.com'
})

# 登录用户
session = requests.Session()
response = session.post('http://localhost:3000/auth/login', json={
    'username': 'myuser',
    'password': 'mypassword'
})

# 获取用户信息
profile = session.get('http://localhost:3000/auth/profile')
print(profile.json())
```

### 创建交易记录
```python
# 创建存款记录
deallog = session.post('http://localhost:3000/dealLog', json={
    'type': 'deposit',
    'amount': 1000,
    'currency': 'USDT',
    'remark': '初始存款'
})
```

### 查询持仓信息
```python
# 获取本地持仓记录
positions = session.get('http://localhost:3000/positions')

# 获取币安实时持仓 (需要配置API密钥)
binance_positions = session.get('http://localhost:3000/positions/binance')
```

## 🛠️ 开发

### 添加新功能模块
1. 在 `app/models/` 中创建数据模型
2. 在 `app/blueprints/` 中创建路由蓝图
3. 在 `app/utils/` 中添加业务逻辑
4. 在 `app/__init__.py` 中注册蓝图

### 代码规范
- 使用Python类型提示
- 遵循PEP 8代码风格
- 为函数添加文档字符串
- 编写单元测试

### 数据库迁移
```bash
# 安装迁移工具
pip install Flask-Migrate

# 初始化迁移
flask db init

# 创建迁移脚本
flask db migrate -m "Add new table"

# 执行迁移
flask db upgrade
```

## 🔒 安全注意事项

1. **生产环境**:
   - 设置强密码作为 `SECRET_KEY`
   - 使用HTTPS协议
   - 配置防火墙和访问控制

2. **API安全**:
   - 实施访问频率限制
   - 验证和清理用户输入
   - 记录和监控异常访问

3. **数据安全**:
   - 定期备份数据库
   - 加密敏感信息
   - 限制数据库访问权限

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🤝 贡献

欢迎贡献代码！请遵循以下步骤：

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 📞 支持

如果您遇到任何问题或有任何建议，请：

1. 查看 [文档](docs/)
2. 检查 [常见问题](#)
3. 提交 [Issue](../../issues)
4. 联系开发团队

---

⭐ 如果这个项目对您有帮助，请考虑给它一个 star！