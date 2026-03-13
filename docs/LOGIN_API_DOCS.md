# 登录模块API文档

本文档介绍了登录模块的所有API接口及其使用方法。

## 基础信息

- 基础URL: `http://localhost:3000`
- 认证方式: Session-based认证
- 内容类型: `application/json`

## API接口列表

### 1. 用户注册

**接口**: `POST /auth/register`

**请求体**:
```json
{
    "username": "testuser",
    "password": "password123",
    "email": "user@example.com"  // 可选
}
```

**成功响应** (201):
```json
{
    "message": "注册成功",
    "user": {
        "id": 1,
        "username": "testuser",
        "email": "user@example.com",
        "is_active": true,
        "created_at": "2024-01-01T12:00:00",
        "last_login": null
    }
}
```

**错误响应**:
- 400: 数据验证失败
- 409: 用户名或邮箱已存在

### 2. 用户登录

**接口**: `POST /auth/login`

**请求体**:
```json
{
    "username": "testuser",
    "password": "password123"
}
```

**成功响应** (200):
```json
{
    "message": "登录成功",
    "user": {
        "id": 1,
        "username": "testuser",
        "email": "user@example.com",
        "is_active": true,
        "created_at": "2024-01-01T12:00:00",
        "last_login": "2024-01-01T12:30:00"
    }
}
```

**错误响应**:
- 401: 用户名或密码错误
- 403: 账户已被禁用

### 3. 用户登出

**接口**: `POST /auth/logout`

**认证**: 需要登录

**成功响应** (200):
```json
{
    "message": "登出成功"
}
```

### 4. 获取认证状态

**接口**: `GET /auth/status`

**成功响应** (200):
```json
{
    "authenticated": true,
    "user": {
        "id": 1,
        "username": "testuser",
        "email": "user@example.com",
        "is_active": true,
        "created_at": "2024-01-01T12:00:00",
        "last_login": "2024-01-01T12:30:00"
    }
}
```

**未登录响应** (200):
```json
{
    "authenticated": false,
    "user": null
}
```

### 5. 获取用户信息

**接口**: `GET /auth/profile`

**认证**: 需要登录

**成功响应** (200):
```json
{
    "user": {
        "id": 1,
        "username": "testuser",
        "email": "user@example.com",
        "is_active": true,
        "created_at": "2024-01-01T12:00:00",
        "last_login": "2024-01-01T12:30:00"
    }
}
```

### 6. 更新用户信息

**接口**: `PUT /auth/profile`

**认证**: 需要登录

**请求体**:
```json
{
    "email": "newemail@example.com"
}
```

**成功响应** (200):
```json
{
    "message": "用户信息更新成功",
    "user": {
        "id": 1,
        "username": "testuser",
        "email": "newemail@example.com",
        "is_active": true,
        "created_at": "2024-01-01T12:00:00",
        "last_login": "2024-01-01T12:30:00"
    }
}
```

### 7. 修改密码

**接口**: `POST /auth/change-password`

**认证**: 需要登录

**请求体**:
```json
{
    "current_password": "oldpassword123",
    "new_password": "newpassword123"
}
```

**成功响应** (200):
```json
{
    "message": "密码修改成功"
}
```

## 错误代码说明

- **400 Bad Request**: 请求数据格式错误或验证失败
- **401 Unauthorized**: 认证失败，用户名或密码错误
- **403 Forbidden**: 用户账户被禁用或权限不足
- **409 Conflict**: 数据冲突，如用户名已存在
- **500 Internal Server Error**: 服务器内部错误

## 使用示例

### Python示例 (使用requests库)

```python
import requests
import json

# 基础URL
BASE_URL = "http://localhost:3000"

# 创建session以保持登录状态
session = requests.Session()

# 1. 注册用户
def register_user():
    url = f"{BASE_URL}/auth/register"
    data = {
        "username": "testuser",
        "password": "password123",
        "email": "test@example.com"
    }
    response = session.post(url, json=data)
    print(f"注册响应: {response.status_code}")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

# 2. 用户登录
def login():
    url = f"{BASE_URL}/auth/login"
    data = {
        "username": "testuser",
        "password": "password123"
    }
    response = session.post(url, json=data)
    print(f"登录响应: {response.status_code}")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    return response.status_code == 200

# 3. 获取用户信息
def get_profile():
    url = f"{BASE_URL}/auth/profile"
    response = session.get(url)
    print(f"用户信息响应: {response.status_code}")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

# 4. 检查认证状态
def check_auth_status():
    url = f"{BASE_URL}/auth/status"
    response = session.get(url)
    print(f"认证状态响应: {response.status_code}")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

# 5. 登出
def logout():
    url = f"{BASE_URL}/auth/logout"
    response = session.post(url)
    print(f"登出响应: {response.status_code}")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

# 使用示例
if __name__ == "__main__":
    # 注册用户
    register_user()
    
    # 登录
    if login():
        # 获取用户信息
        get_profile()
        
        # 检查认证状态
        check_auth_status()
        
        # 登出
        logout()
```

### JavaScript示例 (使用fetch API)

```javascript
const BASE_URL = "http://localhost:3000";

// 1. 注册用户
async function registerUser() {
    const response = await fetch(`${BASE_URL}/auth/register`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'include', // 包含cookies
        body: JSON.stringify({
            username: 'testuser',
            password: 'password123',
            email: 'test@example.com'
        })
    });
    
    const data = await response.json();
    console.log('注册响应:', data);
    return response.ok;
}

// 2. 用户登录
async function login() {
    const response = await fetch(`${BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({
            username: 'testuser',
            password: 'password123'
        })
    });
    
    const data = await response.json();
    console.log('登录响应:', data);
    return response.ok;
}

// 3. 获取用户信息
async function getProfile() {
    const response = await fetch(`${BASE_URL}/auth/profile`, {
        method: 'GET',
        credentials: 'include'
    });
    
    const data = await response.json();
    console.log('用户信息:', data);
}

// 4. 检查认证状态
async function checkAuthStatus() {
    const response = await fetch(`${BASE_URL}/auth/status`, {
        credentials: 'include'
    });
    
    const data = await response.json();
    console.log('认证状态:', data);
}

// 5. 登出
async function logout() {
    const response = await fetch(`${BASE_URL}/auth/logout`, {
        method: 'POST',
        credentials: 'include'
    });
    
    const data = await response.json();
    console.log('登出响应:', data);
}

// 使用示例
async function main() {
    await registerUser();
    
    if (await login()) {
        await getProfile();
        await checkAuthStatus();
        await logout();
    }
}

main().catch(console.error);
```

## 数据验证规则

### 用户名验证
- 长度: 3-80个字符
- 字符限制: 只能包含字母、数字和下划线
- 唯一性: 不能重复

### 密码验证
- 长度: 至少6个字符，最多128个字符
- 存储: 使用bcrypt进行哈希加密

### 邮箱验证
- 格式: 标准邮箱格式验证
- 唯一性: 不能重复（如果提供）
- 可选: 注册时邮箱字段可选

## 安全性说明

1. **密码安全**: 密码使用bcrypt进行哈希加密存储
2. **会话管理**: 使用Flask-Login进行会话管理
3. **CSRF保护**: 建议在生产环境中启用CSRF保护
4. **密钥安全**: 请在生产环境中设置强密码作为SECRET_KEY
5. **HTTPS**: 生产环境中应使用HTTPS协议

## 部署说明

1. 安装依赖:
   ```bash
   pip install -r requirements.txt
   ```

2. 设置环境变量:
   ```bash
   export SECRET_KEY="your-very-secure-secret-key-here"
   ```

3. 创建管理员用户:
   ```bash
   python create_admin.py
   ```

4. 启动应用:
   ```bash
   python app.py
   ```