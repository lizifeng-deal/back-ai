from flask import Blueprint, request, jsonify
import positions_ops as ops

def create_positions_blueprint(db, Position):
    bp = Blueprint("positions", __name__)

    @bp.route("/positions", methods=["GET"])
    def list_positions():
        payload, code = ops.list_rows(Position)
        return jsonify(payload), code

    @bp.route("/positions/<string:entry_id>", methods=["GET"])
    def get_position(entry_id):
        payload, code = ops.get_row(Position, entry_id)
        return jsonify(payload), code

    @bp.route("/positions", methods=["POST"])
    def create_position():
        data = request.get_json(silent=True) or {}
        payload, code = ops.create_row(Position, db, data)
        return jsonify(payload), code

    @bp.route("/positions/<string:entry_id>", methods=["PUT", "PATCH"])
    def update_position(entry_id):
        data = request.get_json(silent=True) or {}
        payload, code = ops.update_row(Position, db, entry_id, data)
        return jsonify(payload), code

    @bp.route("/positions/<string:entry_id>", methods=["DELETE"])
    def delete_position(entry_id):
        payload, code = ops.delete_row(Position, db, entry_id)
        return payload, code

    return bp
