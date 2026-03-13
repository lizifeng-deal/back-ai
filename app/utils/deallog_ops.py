"""
交易日志业务逻辑操作函数
"""
import time
import uuid
from decimal import Decimal
from sqlalchemy import func

def list_deallog_records(DealLog):
    """获取所有交易日志记录"""
    rows = DealLog.query.order_by(DealLog.timestamp.desc()).all()
    return [r.to_dict() for r in rows], 200

def get_deallog_record(DealLog, entry_id):
    """根据ID获取单个交易日志记录"""
    row = DealLog.query.get(entry_id)
    if not row:
        return {"error": "not_found"}, 404
    return row.to_dict(), 200

def create_deallog_record(DealLog, db, data):
    """创建新的交易日志记录"""
    # 验证交易类型
    trade_type = data.get("type") or "deposit"
    if trade_type not in {"deposit", "withdraw", "delivery_pnl"}:
        return {"error": "invalid_type"}, 400
    
    # 生成或使用提供的ID
    entry_id = data.get("id") or ("dl-" + uuid.uuid4().hex[:12])
    
    # 处理币种和金额
    currency = data.get("currency") or ""
    amount_val = data.get("amount")
    amount_unit = Decimal("1")
    
    # USDT汇率处理
    if currency == "USDT":
        amount_unit = Decimal("6.92")
    
    if amount_val is None:
        amt = Decimal("0")
    else:
        try:
            amt = Decimal(str(amount_val)) * amount_unit
        except Exception:
            return {"error": "invalid_amount"}, 400
    
    # 处理时间戳
    ts = data.get("timestamp")
    ts_val = int(ts) if ts is not None else int(time.time() * 1000)
    
    # 处理可用金额
    free_val = data.get("free")
    free_num = None
    if free_val is not None:
        try:
            free_num = Decimal(str(free_val))
        except Exception:
            return {"error": "invalid_free"}, 400
    
    # 获取备注
    remark = data.get("remark")
    
    # 创建记录
    row = DealLog(
        id=entry_id,
        type=trade_type,
        amount=amt,
        timestamp=ts_val,
        remark=remark,
        free=free_num,
        currency=currency
    )
    
    db.session.add(row)
    db.session.commit()
    return row.to_dict(), 200

def update_deallog_record(DealLog, db, entry_id, data):
    """更新交易日志记录"""
    row = DealLog.query.get(entry_id)
    if not row:
        return {"error": "not_found"}, 404
    
    # 更新交易类型
    if "type" in data:
        if data["type"] not in {"deposit", "withdraw", "delivery_pnl"}:
            return {"error": "invalid_type"}, 400
        row.type = data["type"]
    
    # 更新金额
    if "amount" in data:
        try:
            row.amount = Decimal(str(data["amount"]))
        except Exception:
            return {"error": "invalid_amount"}, 400
    
    # 更新时间戳
    if "timestamp" in data and data["timestamp"] is not None:
        row.timestamp = int(data["timestamp"])
    
    # 更新备注
    if "remark" in data:
        row.remark = data["remark"]
    
    # 更新可用金额
    if "free" in data:
        if data["free"] is None:
            row.free = None
        else:
            try:
                row.free = Decimal(str(data["free"]))
            except Exception:
                return {"error": "invalid_free"}, 400
    
    # 更新币种
    if "currency" in data:
        row.currency = data["currency"]
    
    db.session.commit()
    return row.to_dict(), 200

def delete_deallog_record(DealLog, db, entry_id):
    """删除交易日志记录"""
    row = DealLog.query.get(entry_id)
    if not row:
        return {"error": "not_found"}, 404
    
    db.session.delete(row)
    db.session.commit()
    return {"message": "deleted"}, 200

def sum_delivery_pnl(DealLog, db):
    """计算交割盈亏汇总"""
    total = db.session.query(func.sum(DealLog.amount)).filter(
        DealLog.type == "delivery_pnl"
    ).scalar()
    
    if total is None:
        total = Decimal("0")
    
    return {"type": "delivery_pnl", "total": float(total)}, 200