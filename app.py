import os
import sys
import time
from decimal import Decimal
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "vendor"))
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

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

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "amount": float(self.amount),
            "timestamp": int(self.timestamp),
            "remark": self.remark or "",
            "free": float(self.free) if self.free is not None else None,
        }

with app.app_context():
    db.create_all()

@app.route("/dealLog", methods=["GET"])
def list_deallog():
    rows = DealLog.query.order_by(DealLog.timestamp.desc()).all()
    return jsonify([r.to_dict() for r in rows])

@app.route("/dealLog/<string:entry_id>", methods=["GET"])
def get_deallog(entry_id):
    row = DealLog.query.get(entry_id)
    if not row:
        return jsonify({"error": "not_found"}), 404
    return jsonify(row.to_dict())

@app.route("/dealLog", methods=["POST"])
def create_deallog():
    data = request.get_json(silent=True) or {}
    t = data.get("type")
    if t not in {"deposit", "withdraw", "delivery_pnl"}:
        return jsonify({"error": "invalid_type"}), 400
    entry_id = data.get("id")
    if not entry_id:
        return jsonify({"error": "id_required"}), 400
    try:
        amt = Decimal(str(data.get("amount")))
    except Exception:
        return jsonify({"error": "invalid_amount"}), 400
    ts = data.get("timestamp")
    ts_val = int(ts) if ts is not None else int(time.time() * 1000)
    free_val = data.get("free")
    free_num = None
    if free_val is not None:
        try:
            free_num = Decimal(str(free_val))
        except Exception:
            return jsonify({"error": "invalid_free"}), 400
    remark = data.get("remark")
    row = DealLog(id=entry_id, type=t, amount=amt, timestamp=ts_val, remark=remark, free=free_num)
    db.session.add(row)
    db.session.commit()
    return jsonify(row.to_dict()), 201

@app.route("/dealLog/<string:entry_id>", methods=["PUT", "PATCH"])
def update_deallog(entry_id):
    row = DealLog.query.get(entry_id)
    if not row:
        return jsonify({"error": "not_found"}), 404
    data = request.get_json(silent=True) or {}
    if "type" in data:
        if data["type"] not in {"deposit", "withdraw", "delivery_pnl"}:
            return jsonify({"error": "invalid_type"}), 400
        row.type = data["type"]
    if "amount" in data:
        try:
            row.amount = Decimal(str(data["amount"]))
        except Exception:
            return jsonify({"error": "invalid_amount"}), 400
    if "timestamp" in data and data["timestamp"] is not None:
        row.timestamp = int(data["timestamp"])
    if "remark" in data:
        row.remark = data["remark"]
    if "free" in data:
        if data["free"] is None:
            row.free = None
        else:
            try:
                row.free = Decimal(str(data["free"]))
            except Exception:
                return jsonify({"error": "invalid_free"}), 400
    db.session.commit()
    return jsonify(row.to_dict())

@app.route("/dealLog/<string:entry_id>", methods=["DELETE"])
def delete_deallog(entry_id):
    row = DealLog.query.get(entry_id)
    if not row:
        return jsonify({"error": "not_found"}), 404
    db.session.delete(row)
    db.session.commit()
    return "", 204

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
