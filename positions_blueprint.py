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
            
            # 获取可选的配置参数
            timeout = int(request.args.get('timeout', 30))  # 默认30秒超时
            show_all = request.args.get('show_all', 'false').lower() == 'true'
            mock_mode = request.args.get('mock', 'false').lower() == 'true'
            
            # 如果启用mock模式，返回模拟数据
            if mock_mode:
                mock_positions = [
                    {
                        "symbol": "BTCUSDT",
                        "positionAmt": "0.001",
                        "entryPrice": "45000.0",
                        "unRealizedProfit": "50.0",
                        "markPrice": "50000.0",
                        "liquidationPrice": "0",
                        "marginType": "isolated",
                        "isolatedMargin": "45.0",
                        "isAutoAddMargin": "false",
                        "positionSide": "LONG",
                        "percentage": "1.11111",
                        "updateTime": 1773382800000
                    },
                    {
                        "symbol": "ETHUSDT",
                        "positionAmt": "0.0",
                        "entryPrice": "0.0",
                        "unRealizedProfit": "0.0",
                        "markPrice": "3500.0",
                        "liquidationPrice": "0",
                        "marginType": "cross",
                        "isolatedMargin": "0.0",
                        "isAutoAddMargin": "false",
                        "positionSide": "BOTH",
                        "percentage": "0.0",
                        "updateTime": 1773382800000
                    }
                ]
                
                # 如果不显示全部，只返回非零持仓
                filtered_positions = mock_positions
                if not show_all:
                    filtered_positions = [pos for pos in mock_positions 
                                        if float(pos.get("positionAmt", 0)) != 0]
                
                return jsonify({
                    "success": True,
                    "data": filtered_positions,
                    "total": len(filtered_positions),
                    "total_symbols": len(mock_positions),
                    "config": {
                        "timeout": timeout,
                        "show_all": show_all,
                        "mock_mode": True,
                        "api_base_url": "https://fapi.binance.com"
                    }
                }), 200
            
            # 创建 API 连接，设置超时时间
            api = API(
                api_key=api_key, 
                api_secret=api_secret, 
                base_url="https://fapi.binance.com",
                timeout=timeout
            )
            
            # 查询持仓信息，返回完整原始数据
            positions = api.sign_request("GET", "/fapi/v2/positionRisk")
            
            # 如果不显示全部，只返回非零持仓
            filtered_positions = positions
            if not show_all and isinstance(positions, list):
                filtered_positions = []
                for pos in positions:
                    if isinstance(pos, dict):
                        position_amt = float(pos.get("positionAmt", 0))
                        if position_amt != 0:
                            filtered_positions.append(pos)
            
            return jsonify({
                "success": True,
                "data": filtered_positions,
                "total": len(filtered_positions) if isinstance(filtered_positions, list) else 0,
                "total_symbols": len(positions) if isinstance(positions, list) else 0,
                "config": {
                    "timeout": timeout,
                    "show_all": show_all,
                    "mock_mode": False,
                    "api_base_url": api.base_url
                }
            }), 200
            
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"查询币安持仓失败: {str(e)}",
                "error_type": type(e).__name__
            }), 500

    @bp.route("/positions/binance/test", methods=["GET"])
    def test_binance_connection():
        """测试币安连接状态"""
        try:
            api_key = os.environ.get("BINANCE_API_KEY")
            api_secret = os.environ.get("BINANCE_API_SECRET")
            
            if not api_key or not api_secret:
                return jsonify({
                    "success": False,
                    "error": "缺少环境变量",
                    "has_api_key": bool(api_key),
                    "has_api_secret": bool(api_secret)
                }), 400
            
            # 创建API实例进行连接测试
            api = API(
                api_key=api_key, 
                api_secret=api_secret, 
                base_url="https://fapi.binance.com",
                timeout=10  # 短超时用于测试
            )
            
            # 尝试获取账户信息（比持仓信息更轻量）
            account_info = api.sign_request("GET", "/fapi/v2/account")
            
            return jsonify({
                "success": True,
                "message": "币安连接正常",
                "account_balance_count": len(account_info.get("assets", [])) if isinstance(account_info, dict) else 0,
                "can_trade": account_info.get("canTrade", False) if isinstance(account_info, dict) else False
            }), 200
            
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"连接测试失败: {str(e)}",
                "error_type": type(e).__name__
            }), 500

    return bp