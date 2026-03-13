"""
持仓模型
"""
from app import db

class Position(db.Model):
    """持仓模型"""
    __tablename__ = "positions"
    
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    quantity = db.Column(db.Numeric(18, 8), nullable=False)
    market_value = db.Column(db.Numeric(18, 8), nullable=False)
    open_price = db.Column(db.Numeric(18, 8), nullable=False)
    pnl = db.Column(db.Numeric(18, 8), nullable=False)
    leverage = db.Column(db.Numeric(18, 8))
    side = db.Column(db.Enum("long", "short", name="position_side"), nullable=False)
    margin = db.Column(db.Numeric(18, 8))
    currency = db.Column(db.String(16))

    def to_dict(self):
        """转换为字典格式"""
        return {
            "id": self.id,
            "name": self.name,
            "quantity": float(self.quantity),
            "market_value": float(self.market_value),
            "open_price": float(self.open_price),
            "pnl": float(self.pnl),
            "leverage": float(self.leverage) if self.leverage is not None else None,
            "side": self.side,
            "margin": float(self.margin) if self.margin is not None else None,
            "currency": self.currency or "",
        }
    
    def __repr__(self):
        return f'<Position {self.id} - {self.name}>'