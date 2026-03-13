"""
持仓业务逻辑操作函数
"""
import uuid
from decimal import Decimal

def list_position_records(Position):
    """获取所有持仓记录"""
    rows = Position.query.all()
    return [r.to_dict() for r in rows], 200

def get_position_record(Position, entry_id):
    """根据ID获取单个持仓记录"""
    row = Position.query.get(entry_id)
    if not row:
        return {"error": "not_found"}, 404
    return row.to_dict(), 200

def create_position_record(Position, db, data):
    """创建新的持仓记录"""
    # 生成或使用提供的ID
    entry_id = data.get("id") or ("pos-" + uuid.uuid4().hex[:12])
    
    # 基本信息
    name = data.get("name") or ""
    side = data.get("side") or "long"
    
    # 验证持仓方向
    if side not in {"long", "short"}:
        return {"error": "invalid_side"}, 400
    
    def parse_decimal(field_name):
        """解析数值字段"""
        val = data.get(field_name)
        if val is None:
            return Decimal("0")
        try:
            return Decimal(str(val))
        except Exception:
            raise ValueError(field_name)
    
    try:
        # 解析所有数值字段
        quantity = parse_decimal("quantity")
        market_value = parse_decimal("market_value")
        open_price = parse_decimal("open_price")
        pnl = parse_decimal("pnl")
        
        # 处理可选的数值字段
        leverage = data.get("leverage")
        leverage_num = None
        if leverage is not None:
            leverage_num = Decimal(str(leverage))
        
        margin = data.get("margin")
        margin_num = None
        if margin is not None:
            margin_num = Decimal(str(margin))
    
    except ValueError as e:
        return {"error": f"invalid_{str(e)}"}, 400
    
    # 币种信息
    currency = data.get("currency") or ""
    
    # 创建持仓记录
    row = Position(
        id=entry_id,
        name=name,
        quantity=quantity,
        market_value=market_value,
        open_price=open_price,
        pnl=pnl,
        leverage=leverage_num,
        side=side,
        margin=margin_num,
        currency=currency,
    )
    
    db.session.add(row)
    db.session.commit()
    return row.to_dict(), 200

def update_position_record(Position, db, entry_id, data):
    """更新持仓记录"""
    row = Position.query.get(entry_id)
    if not row:
        return {"error": "not_found"}, 404
    
    # 更新名称
    if "name" in data:
        row.name = data["name"] or ""
    
    # 更新持仓方向
    if "side" in data:
        if data["side"] not in {"long", "short"}:
            return {"error": "invalid_side"}, 400
        row.side = data["side"]
    
    def update_decimal_field(field_name, attr_name):
        """更新数值字段"""
        if field_name in data:
            val = data[field_name]
            if val is None:
                setattr(row, attr_name, None)
            else:
                try:
                    setattr(row, attr_name, Decimal(str(val)))
                except Exception:
                    raise ValueError(field_name)
    
    try:
        # 更新所有数值字段
        update_decimal_field("quantity", "quantity")
        update_decimal_field("market_value", "market_value")
        update_decimal_field("open_price", "open_price")
        update_decimal_field("pnl", "pnl")
        update_decimal_field("leverage", "leverage")
        update_decimal_field("margin", "margin")
    
    except ValueError as e:
        return {"error": f"invalid_{str(e)}"}, 400
    
    # 更新币种
    if "currency" in data:
        row.currency = data["currency"] or ""
    
    db.session.commit()
    return row.to_dict(), 200

def delete_position_record(Position, db, entry_id):
    """删除持仓记录"""
    row = Position.query.get(entry_id)
    if not row:
        return {"error": "not_found"}, 404
    
    db.session.delete(row)
    db.session.commit()
    return {"message": "deleted"}, 200