"""
持仓业务逻辑操作函数 - 基于合约持仓接口重构
"""
import uuid
import time

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
    """创建新的合约持仓记录"""
    # 生成或使用提供的ID
    entry_id = data.get("id") or ("pos-" + uuid.uuid4().hex[:12])
    
    # 验证必需字段
    required_fields = ["symbol", "entryPrice", "markPrice", "unRealizedProfit", 
                      "leverage", "positionAmt", "positionSide"]
    
    for field in required_fields:
        if field not in data or data[field] is None:
            return {"error": f"missing_field_{field}"}, 400
    
    # 验证持仓方向
    position_side = data.get("positionSide", "").upper()
    if position_side not in {"LONG", "SHORT"}:
        return {"error": "invalid_position_side", "allowed": ["LONG", "SHORT"]}, 400
    
    # 验证数值字段格式（确保可以作为字符串存储）
    price_fields = ["entryPrice", "markPrice", "unRealizedProfit", "positionAmt"]
    optional_price_fields = ["liquidationPrice", "breakEvenPrice"]
    
    def validate_price_field(field_name, value, required=True):
        """验证价格字段"""
        if value is None:
            if required:
                raise ValueError(f"{field_name}_required")
            return None
        try:
            # 确保可以转换为浮点数（验证格式）
            float(str(value))
            return str(value)
        except (ValueError, TypeError):
            raise ValueError(f"{field_name}_invalid_format")
    
    try:
        # 验证必需的价格字段
        validated_data = {}
        for field in price_fields:
            validated_data[field] = validate_price_field(field, data.get(field), required=True)
        
        # 验证可选的价格字段
        for field in optional_price_fields:
            validated_data[field] = validate_price_field(field, data.get(field), required=False)
        
        # 验证杠杆倍数
        leverage = data.get("leverage")
        if leverage is not None:
            validated_data["leverage"] = str(leverage)
        else:
            return {"error": "leverage_required"}, 400
            
    except ValueError as e:
        return {"error": str(e)}, 400
    
    # 获取更新时间戳（毫秒）
    update_time = data.get("updateTime")
    if update_time is None:
        update_time = int(time.time() * 1000)  # 当前时间戳（毫秒）
    
    # 创建持仓记录
    row = Position(
        id=entry_id,
        symbol=data.get("symbol"),
        entry_price=validated_data["entryPrice"],
        mark_price=validated_data["markPrice"],
        unrealized_profit=validated_data["unRealizedProfit"],
        liquidation_price=validated_data["liquidationPrice"],
        break_even_price=validated_data["breakEvenPrice"],
        leverage=validated_data["leverage"],
        position_amt=validated_data["positionAmt"],
        position_side=position_side,
        update_time=update_time
    )
    
    db.session.add(row)
    db.session.commit()
    return row.to_dict(), 200

def update_position_record(Position, db, entry_id, data):
    """更新合约持仓记录"""
    row = Position.query.get(entry_id)
    if not row:
        return {"error": "not_found"}, 404
    
    # 更新交易对符号
    if "symbol" in data:
        row.symbol = data["symbol"] or ""
    
    # 更新持仓方向
    if "positionSide" in data:
        position_side = data["positionSide"].upper()
        if position_side not in {"LONG", "SHORT"}:
            return {"error": "invalid_position_side", "allowed": ["LONG", "SHORT"]}, 400
        row.position_side = position_side
    
    def validate_and_update_price_field(field_name, attr_name):
        """验证并更新价格字段"""
        if field_name in data:
            val = data[field_name]
            if val is None:
                setattr(row, attr_name, None)
            else:
                try:
                    # 验证可以转换为浮点数
                    float(str(val))
                    setattr(row, attr_name, str(val))
                except (ValueError, TypeError):
                    raise ValueError(f"{field_name}_invalid_format")
    
    try:
        # 更新价格相关字段
        validate_and_update_price_field("entryPrice", "entry_price")
        validate_and_update_price_field("markPrice", "mark_price")
        validate_and_update_price_field("unRealizedProfit", "unrealized_profit")
        validate_and_update_price_field("liquidationPrice", "liquidation_price")
        validate_and_update_price_field("breakEvenPrice", "break_even_price")
        validate_and_update_price_field("positionAmt", "position_amt")
        
        # 更新杠杆倍数
        if "leverage" in data:
            val = data["leverage"]
            if val is not None:
                row.leverage = str(val)
            else:
                return {"error": "leverage_cannot_be_null"}, 400
    
    except ValueError as e:
        return {"error": str(e)}, 400
    
    # 更新时间戳
    if "updateTime" in data:
        update_time = data["updateTime"]
        if update_time is not None:
            row.update_time = int(update_time)
        else:
            row.update_time = int(time.time() * 1000)
    else:
        # 如果没有提供新的时间戳，使用当前时间
        row.update_time = int(time.time() * 1000)
    
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