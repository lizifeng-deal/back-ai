from flask import Blueprint, request, jsonify
import deallog_ops as ops

def create_deallog_blueprint(db, DealLog):
    bp = Blueprint("deallog", __name__)

    @bp.route("/dealLog", methods=["GET"])
    def list_deallog():
        payload, code = ops.list_rows(DealLog)
        return jsonify(payload), code

    @bp.route("/dealLog/<string:entry_id>", methods=["GET"])
    def get_deallog(entry_id):
        payload, code = ops.get_row(DealLog, entry_id)
        return jsonify(payload), code

    @bp.route("/dealLog", methods=["POST"])
    def create_deallog():
        data = request.get_json(silent=True) or {}
        payload, code = ops.create_row(DealLog, db, data)
        return jsonify(payload), code

    @bp.route("/dealLog/<string:entry_id>", methods=["PUT", "PATCH"])
    def update_deallog(entry_id):
        data = request.get_json(silent=True) or {}
        payload, code = ops.update_row(DealLog, db, entry_id, data)
        return jsonify(payload), code

    @bp.route("/dealLog/<string:entry_id>", methods=["DELETE"])
    def delete_deallog(entry_id):
        payload, code = ops.delete_row(DealLog, db, entry_id)
        return payload, code

    @bp.route("/dealLog/summary/delivery_pnl", methods=["GET"])
    def summary_delivery_pnl():
        payload, code = ops.sum_delivery_pnl(DealLog, db)
        return jsonify(payload), code

    return bp
