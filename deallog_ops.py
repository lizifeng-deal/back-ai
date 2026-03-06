import time
import uuid
from decimal import Decimal
from sqlalchemy import func

def list_rows(DealLog):
    rows = DealLog.query.order_by(DealLog.timestamp.desc()).all()
    return [r.to_dict() for r in rows], 200

def get_row(DealLog, entry_id):
    row = DealLog.query.get(entry_id)
    if not row:
        return {"error": "not_found"}, 404
    return row.to_dict(), 200

def create_row(DealLog, db, data):
    t = data.get("type") or "deposit"
    if t not in {"deposit", "withdraw", "delivery_pnl"}:
        return {"error": "invalid_type"}, 400
    entry_id = data.get("id") or ("dl-" + uuid.uuid4().hex[:12])
    currency = data.get("currency") or ""
    amount_val = data.get("amount")
    amount_unit = Decimal("1")
    if currency == "USDT":
        amount_unit = Decimal("6.92")
    if amount_val is None:
        amt = Decimal("0")
    else:
        try:
            amt = Decimal(str(amount_val)) * amount_unit
        except Exception:
            return {"error": "invalid_amount"}, 400
    ts = data.get("timestamp")
    ts_val = int(ts) if ts is not None else int(time.time() * 1000)
    free_val = data.get("free")
    free_num = None
    if free_val is not None:
        try:
            free_num = Decimal(str(free_val))
        except Exception:
            return {"error": "invalid_free"}, 400
    remark = data.get("remark")
    row = DealLog(id=entry_id, type=t, amount=amt, timestamp=ts_val, remark=remark, free=free_num, currency=currency)
    db.session.add(row)
    db.session.commit()
    return row.to_dict(), 200

def update_row(DealLog, db, entry_id, data):
    row = DealLog.query.get(entry_id)
    if not row:
        return {"error": "not_found"}, 404
    if "type" in data:
        if data["type"] not in {"deposit", "withdraw", "delivery_pnl"}:
            return {"error": "invalid_type"}, 400
        row.type = data["type"]
    if "amount" in data:
        try:
            row.amount = Decimal(str(data["amount"]))
        except Exception:
            return {"error": "invalid_amount"}, 400
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
                return {"error": "invalid_free"}, 400
    if "currency" in data:
        row.currency = data["currency"]
    db.session.commit()
    return row.to_dict(), 200

def delete_row(DealLog, db, entry_id):
    row = DealLog.query.get(entry_id)
    if not row:
        return {"error": "not_found"}, 404
    db.session.delete(row)
    db.session.commit()
    return "", 200

def sum_delivery_pnl(DealLog, db):
    total = db.session.query(func.sum(DealLog.amount)).filter(DealLog.type == "delivery_pnl").scalar()
    if total is None:
        total = Decimal("0")
    return {"type": "delivery_pnl", "total": float(total)}, 200
