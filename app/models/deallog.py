"""
交易日志模型
"""
from app import db

class DealLog(db.Model):
    """交易日志模型"""
    __tablename__ = "dealLog"
    
    id = db.Column(db.String(64), primary_key=True)
    type = db.Column(db.Enum("deposit", "withdraw", "delivery_pnl", name="ledger_type"), nullable=False)
    amount = db.Column(db.Numeric(18, 8), nullable=False)
    timestamp = db.Column(db.BigInteger, nullable=False)
    remark = db.Column(db.String(255))
    free = db.Column(db.Numeric(18, 8))
    currency = db.Column(db.String(16))
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            "id": self.id,
            "type": self.type,
            "amount": float(self.amount),
            "timestamp": int(self.timestamp),
            "remark": self.remark or "",
            "free": float(self.free) if self.free is not None else None,
            "currency": self.currency or "",
        }
    
    def __repr__(self):
        return f'<DealLog {self.id}>'