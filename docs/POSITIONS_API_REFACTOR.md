# Positions API 重构文档

## 概述

已根据 `ContractPosition` 接口重构了 positions 表和相关API，以支持合约交易持仓管理。

## 新的数据结构

### ContractPosition 接口

```typescript
interface ContractPosition {
  /** 开仓均价 */
  entryPrice: string; 
  /** 标记价格（交易所用于计算盈亏/强平的参考价格） */
  markPrice: string;
  /** 未实现盈亏（浮动盈亏，正数盈利/负数亏损） */
  unRealizedProfit: string;
  /** 强平价格（爆仓价，价格触及该值会被强制平仓） */
  liquidationPrice: string;
  /** 保本价格（盈亏平衡价，覆盖手续费/滑点等成本） */
  breakEvenPrice: string;
  /** 杠杆倍数（如"10"表示10倍杠杆） */
  leverage: string;
  /** 持仓数量（合约数量，如"0.019"） */
  positionAmt: string;
  /** 持仓方向（LONG=做多，SHORT=做空） */
  positionSide: 'LONG' | 'SHORT';
  /** 数据更新时间戳（毫秒级） */
  updateTime: number;
}
```

### 数据库表结构

```sql
CREATE TABLE positions (
    id VARCHAR(64) PRIMARY KEY,
    symbol VARCHAR(128) NOT NULL,                -- 交易对符号
    entry_price VARCHAR(32) NOT NULL,            -- 开仓均价
    mark_price VARCHAR(32) NOT NULL,             -- 标记价格
    unrealized_profit VARCHAR(32) NOT NULL,      -- 未实现盈亏
    liquidation_price VARCHAR(32),               -- 强平价格
    break_even_price VARCHAR(32),                -- 保本价格
    leverage VARCHAR(16) NOT NULL,               -- 杠杆倍数
    position_amt VARCHAR(32) NOT NULL,           -- 持仓数量
    position_side ENUM('LONG', 'SHORT') NOT NULL,-- 持仓方向
    update_time BIGINT NOT NULL,                 -- 数据更新时间戳（毫秒）
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

## API 端点

### 1. 获取所有持仓记录
- **GET** `/positions`
- **响应**: 返回所有持仓记录数组

### 2. 获取单个持仓记录
- **GET** `/positions/{id}`
- **响应**: 返回指定ID的持仓记录

### 3. 创建持仓记录
- **POST** `/positions`
- **请求体**: ContractPosition 接口数据
- **响应**: 创建的持仓记录

### 4. 批量创建持仓记录
- **POST** `/positions/batch`
- **请求体**: 
```json
{
  "positions": [ContractPosition, ...]
}
```
- **响应**: 批量处理结果统计

### 5. 从币安同步持仓数据
- **POST** `/positions/from-binance`
- **请求体**:
```json
{
  "clearExisting": false,  // 是否清空现有数据
  "filterZero": true       // 是否过滤零持仓
}
```
- **响应**: 同步结果统计

### 6. 更新持仓记录
- **PUT/PATCH** `/positions/{id}`
- **请求体**: 部分或完整的 ContractPosition 数据
- **响应**: 更新后的持仓记录

### 7. 删除持仓记录
- **DELETE** `/positions/{id}`
- **响应**: 删除确认消息

### 8. 获取币安持仓信息（只读）
- **GET** `/positions/binance`
- **查询参数**:
  - `timeout`: 超时时间（秒），默认30
  - `show_all`: 是否显示所有持仓，默认false（只显示非零持仓）
- **响应**: 币安API原始数据

### 9. 测试币安连接
- **GET** `/positions/binance/test`
- **响应**: 连接状态信息

## 数据迁移

### 自动迁移脚本

运行以下脚本来迁移现有的 positions 表：

```bash
python scripts/migrate_positions_table.py
```

该脚本会：
1. 备份现有数据
2. 删除旧表结构
3. 创建新表结构
4. 尝试迁移兼容的数据字段

### 字段映射

旧字段 → 新字段：
- `name` → `symbol`
- `open_price` → `entry_price`
- `market_value` → `mark_price`（临时映射）
- `pnl` → `unrealized_profit`
- `quantity` → `position_amt`
- `side` → `position_side`（转换为大写）
- `leverage` → `leverage`

新增字段（旧数据中设为 NULL）：
- `liquidation_price`
- `break_even_price`
- `update_time`（使用当前时间戳）

## 注意事项

1. **精度问题**: 价格和数量字段使用字符串存储以保持精度
2. **时间戳**: `updateTime` 使用毫秒级时间戳
3. **持仓方向**: 使用大写 `LONG`/`SHORT`
4. **环境变量**: 币安API功能需要设置 `BINANCE_API_KEY` 和 `BINANCE_API_SECRET`
5. **数据验证**: 所有数值字段在存储前会进行格式验证

## 示例用法

### 创建持仓记录

```bash
curl -X POST http://localhost:5000/positions \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "BTCUSDT",
    "entryPrice": "45000.50",
    "markPrice": "45100.25",
    "unRealizedProfit": "100.75",
    "leverage": "10",
    "positionAmt": "0.01",
    "positionSide": "LONG",
    "updateTime": 1647389123000
  }'
```

### 从币安同步数据

```bash
curl -X POST http://localhost:5000/positions/from-binance \
  -H "Content-Type: application/json" \
  -d '{
    "clearExisting": true,
    "filterZero": true
  }'
```