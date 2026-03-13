# 登录模块

为您的Flask应用添加了完整的用户认证功能。

## 新增文件

- `models.py` - 数据模型定义（用户、交易日志、持仓）
- `auth_blueprint.py` - 认证相关的API端点
- `create_admin.py` - 创建管理员用户的脚本
- `test_auth.py` - 登录模块功能测试脚本
- `LOGIN_API_DOCS.md` - 详细的API文档

## 功能特性

### 🔐 用户认证
- 用户注册和登录
- 密码加密存储（bcrypt）
- 会话管理（Flask-Login）
- 用户状态检查

### 👤 用户管理
- 用户信息管理
- 密码修改
- 邮箱更新
- 账户状态控制

### 🔒 安全特性
- 密码强度验证
- 用户名格式验证
- 邮箱格式验证
- 会话安全管理

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 创建管理员用户
```bash
python create_admin.py
```

### 3. 启动应用
```bash
python app.py
```

### 4. 测试功能
```bash
python test_auth.py
```

## API端点

| 方法 | 端点 | 功能 | 认证要求 |
|------|------|------|----------|
| POST | `/auth/register` | 用户注册 | ❌ |
| POST | `/auth/login` | 用户登录 | ❌ |
| POST | `/auth/logout` | 用户登出 | ✅ |
| GET | `/auth/status` | 获取认证状态 | ❌ |
| GET | `/auth/profile` | 获取用户信息 | ✅ |
| PUT | `/auth/profile` | 更新用户信息 | ✅ |
| POST | `/auth/change-password` | 修改密码 | ✅ |

## 使用示例

### 注册用户
```bash
curl -X POST http://localhost:3000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123","email":"test@example.com"}'
```

### 登录
```bash
curl -X POST http://localhost:3000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}' \
  -c cookies.txt
```

### 获取用户信息
```bash
curl -X GET http://localhost:3000/auth/profile \
  -b cookies.txt
```

### 登出
```bash
curl -X POST http://localhost:3000/auth/logout \
  -b cookies.txt
```

## 配置说明

### 环境变量
- `SECRET_KEY`: Flask会话密钥（生产环境必须设置）

### 数据库
- 使用SQLite数据库（`app.db`）
- 自动创建用户表
- 支持数据库迁移

## 数据验证

### 用户名
- 长度：3-80个字符
- 字符：字母、数字、下划线
- 唯一性：不能重复

### 密码
- 长度：至少6个字符
- 加密：bcrypt哈希

### 邮箱
- 格式：标准邮箱格式
- 唯一性：不能重复
- 可选：注册时可不提供

## 目录结构

```
项目根目录/
├── app.py                 # 主应用文件（已更新）
├── models.py              # 数据模型（新增）
├── auth_blueprint.py      # 认证蓝图（新增）
├── create_admin.py        # 创建管理员脚本（新增）
├── test_auth.py          # 测试脚本（新增）
├── LOGIN_API_DOCS.md     # API文档（新增）
├── requirements.txt       # 依赖列表（已更新）
└── instance/
    └── app.db            # SQLite数据库
```

## 注意事项

1. **生产环境安全**：
   - 设置强密码作为 `SECRET_KEY`
   - 使用HTTPS协议
   - 定期更新依赖包

2. **数据备份**：
   - 定期备份数据库文件
   - 考虑使用其他数据库（PostgreSQL/MySQL）

3. **日志记录**：
   - 监控登录失败尝试
   - 记录重要的用户操作

4. **扩展功能**：
   - 可添加角色权限管理
   - 可集成第三方认证（OAuth）
   - 可添加密码重置功能

## 故障排除

### 常见问题

1. **无法连接数据库**：检查数据库文件权限
2. **导入错误**：确保所有依赖都已安装
3. **认证失败**：检查会话配置和密钥设置

### 调试模式

启用调试模式可获得详细错误信息：
```python
app.run(debug=True)
```

## 更多信息

详细的API使用说明请参考 `LOGIN_API_DOCS.md` 文件。