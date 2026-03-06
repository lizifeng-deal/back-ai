import uuid
from decimal import Decimal

def list_rows(Position):
    rows = Position.query.all()
    return [r.to_dict() for r in rows], 200

def get_row(Position, entry_id):
    row = Position.query.get(entry_id)
    if not row:
        return {"error": "not_found"}, 404
    return row.to_dict(), 200

def create_row(Position, db, data):
    entry_id = data.get("id") or ("pos-" + uuid.uuid4().hex[:12])
    name = data.get("name") or ""
    side = data.get("side") or "long"
    if side not in {"long", "short"}:
        return {"error": "invalid_side"}, 400
    def num(name_key):
        val = data.get(name_key)
        if val is None:
            return Decimal("0")
        try:
            return Decimal(str(val))
        except Exception:
            raise ValueError(name_key)
    try:
        quantity = num("quantity")
        market_value = num("market_value")
        open_price = num("open_price")
        pnl = num("pnl")
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
    currency = data.get("currency") or ""
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

def update_row(Position, db, entry_id, data):
    row = Position.query.get(entry_id)
    if not row:
        return {"error": "not_found"}, 404
    if "name" in data:
        row.name = data["name"] or ""
    if "side" in data:
        if data["side"] not in {"long", "short"}:
            return {"error": "invalid_side"}, 400
        row.side = data["side"]
    def set_num(key, attr):
        if key in data:
            val = data[key]
            if val is None:
                setattr(row, attr, None)
            else:
                try:
                    setattr(row, attr, Decimal(str(val)))
                except Exception:
                    raise ValueError(key)
    try:
        set_num("quantity", "quantity")
        set_num("market_value", "market_value")
        set_num("open_price", "open_price")
        set_num("pnl", "pnl")
        set_num("leverage", "leverage")
        set_num("margin", "margin")
    except ValueError as e:
        return {"error": f"invalid_{str(e)}"}, 400
    if "currency" in data:
        row.currency = data["currency"] or ""
    db.session.commit()
    return row.to_dict(), 200

def delete_row(Position, db, entry_id):
    row = Position.query.get(entry_id)
    if not row:
        return {"error": "not_found"}, 404
    db.session.delete(row)
    db.session.commit()
    return "", 200
