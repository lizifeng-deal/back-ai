"""
持仓模型 - 基于合约持仓接口重构
"""
from app import db
from datetime import datetime

class Position(db.Model):
    """合约持仓模型"""
    __tablename__ = "positions"
    
    id = db.Column(db.String(64), primary_key=True)
    
    # 基本信息
    symbol = db.Column(db.String(128), nullable=False, comment="交易对符号")
    
    # 价格相关字段（使用字符串存储以保持精度）
    entry_price = db.Column(db.String(32), nullable=False, comment="开仓均价")
    mark_price = db.Column(db.String(32), nullable=False, comment="标记价格")
    liquidation_price = db.Column(db.String(32), nullable=True, comment="强平价格")
    break_even_price = db.Column(db.String(32), nullable=True, comment="保本价格")
    
    # 盈亏相关
    unrealized_profit = db.Column(db.String(32), nullable=False, comment="未实现盈亏")
    
    # 持仓信息
    leverage = db.Column(db.String(16), nullable=False, comment="杠杆倍数")
    position_amt = db.Column(db.String(32), nullable=False, comment="持仓数量")
    position_side = db.Column(db.Enum("LONG", "SHORT", name="contract_position_side"), nullable=False, comment="持仓方向")
    
    # 时间戳
    update_time = db.Column(db.BigInteger, nullable=False, comment="数据更新时间戳（毫秒）")
    
    # 币种信息
    currency = db.Column(db.String(16), nullable=False, default="USDT", comment="计价货币")
    
    # 创建和修改时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment="记录创建时间")
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="记录更新时间")

    def to_dict(self):
        """转换为字典格式，符合 ContractPosition 接口"""
        return {
            "id": self.id,
            "symbol": self.symbol,
            "entryPrice": self.entry_price,
            "markPrice": self.mark_price,
            "unRealizedProfit": self.unrealized_profit,
            "liquidationPrice": self.liquidation_price,
            "breakEvenPrice": self.break_even_price,
            "leverage": self.leverage,
            "positionAmt": self.position_amt,
            "positionSide": self.position_side,
            "updateTime": self.update_time,
            "currency": self.currency,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "updatedAt": self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_contract_position(self):
        """转换为 ContractPosition 接口格式"""
        return {
            "entryPrice": self.entry_price,
            "markPrice": self.mark_price,
            "unRealizedProfit": self.unrealized_profit,
            "liquidationPrice": self.liquidation_price,
            "breakEvenPrice": self.break_even_price,
            "leverage": self.leverage,
            "positionAmt": self.position_amt,
            "positionSide": self.position_side,
            "updateTime": self.update_time
        }
    
    def __repr__(self):
        return f'<Position {self.id} - {self.symbol} {self.position_side}>'
