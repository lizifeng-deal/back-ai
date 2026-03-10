import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "vendor"))
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect, text
from deallog_blueprint import create_deallog_blueprint
from positions_blueprint import create_positions_blueprint

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class DealLog(db.Model):
    __tablename__ = "dealLog"
    id = db.Column(db.String(64), primary_key=True)
    type = db.Column(db.Enum("deposit", "withdraw", "delivery_pnl", name="ledger_type"), nullable=False)
    amount = db.Column(db.Numeric(18, 8), nullable=False)
    timestamp = db.Column(db.BigInteger, nullable=False)
    remark = db.Column(db.String(255))
    free = db.Column(db.Numeric(18, 8))
    currency = db.Column(db.String(16))
    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "amount": float(self.amount),
            "timestamp": int(self.timestamp),
            "remark": self.remark or "",
            "free": float(self.free) if self.free is not None else None,
            "currency": self.currency or "",
        }

class Position(db.Model):
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

with app.app_context():
    db.create_all()
    insp = inspect(db.engine)
    tables = insp.get_table_names()
    if "dealLog" in tables:
        cols = [c["name"] for c in insp.get_columns("dealLog")]
        if "currency" not in cols:
            db.session.execute(text("ALTER TABLE dealLog ADD COLUMN currency VARCHAR(16)"))
            db.session.commit()

bp = create_deallog_blueprint(db, DealLog)
app.register_blueprint(bp)
bp_pos = create_positions_blueprint(db, Position)
app.register_blueprint(bp_pos)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=True)
