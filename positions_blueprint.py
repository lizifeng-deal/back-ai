import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "vendor"))
from flask import Blueprint, request, jsonify
import positions_ops as ops
from binance.api import API

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

    @bp.route("/positions/binance", methods=["GET"])
    def get_binance_positions():
        """获取币安合约持仓信息"""
        try:
            # 获取环境变量中的 API 密钥
            api_key = os.environ.get("BINANCE_API_KEY")
            api_secret = os.environ.get("BINANCE_API_SECRET")
            
            if not api_key or not api_secret:
                return jsonify({
                    "error": "缺少 BINANCE_API_KEY 或 BINANCE_API_SECRET 环境变量"
                }), 400
            
            # 创建 API 连接
            api = API(api_key=api_key, api_secret=api_secret, base_url="https://fapi.binance.com")
            
            # 查询持仓信息，返回完整原始数据
            positions = api.sign_request("GET", "/fapi/v2/positionRisk")
            
            return jsonify({
                "success": True,
                "data": positions,
                "total": len(positions)
            }), 200
            
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"查询币安持仓失败: {str(e)}"
            }), 500

    return bp
