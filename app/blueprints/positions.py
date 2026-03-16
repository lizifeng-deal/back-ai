"""
持仓蓝图 - 处理持仓管理相关功能
"""
import os
import sys
import time
from flask import Blueprint, request, jsonify
from app.models.position import Position
from app import db
from app.utils.positions_ops import (
    list_position_records,
    get_position_record,
    create_position_record,
    update_position_record,
    delete_position_record
)


# 添加vendor目录到Python路径（用于第三方依赖）
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "vendor"))

# 创建持仓蓝图
positions_bp = Blueprint("positions", __name__)

@positions_bp.route("/positions", methods=["GET"])
def list_positions():
    """获取所有持仓记录"""
    payload, code = list_position_records(Position)
    return jsonify(payload), code

@positions_bp.route("/positions/<string:entry_id>", methods=["GET"])
def get_position(entry_id):
    """根据ID获取单个持仓记录"""
    payload, code = get_position_record(Position, entry_id)
    return jsonify(payload), code

@positions_bp.route("/positions", methods=["POST"])
def create_position():
    """创建新的持仓记录"""
    data = request.get_json(silent=True) or {}
    payload, code = create_position_record(Position, db, data)
    return jsonify(payload), code

@positions_bp.route("/positions/batch", methods=["POST"])
def create_positions_batch():
    """批量创建合约持仓记录"""
    data = request.get_json(silent=True) or {}
    positions_data = data.get("positions", [])
    
    if not isinstance(positions_data, list):
        return jsonify({"error": "positions 字段必须是数组"}), 400
    
    if not positions_data:
        return jsonify({"error": "positions 数组不能为空"}), 400
    
    results = []
    success_count = 0
    error_count = 0
    
    for i, position_data in enumerate(positions_data):
        try:
            payload, code = create_position_record(Position, db, position_data)
            if code == 200:
                success_count += 1
                results.append({"index": i, "success": True, "data": payload})
            else:
                error_count += 1
                results.append({"index": i, "success": False, "error": payload})
        except Exception as e:
            error_count += 1
            results.append({"index": i, "success": False, "error": {"message": str(e)}})
    
    return jsonify({
        "success_count": success_count,
        "error_count": error_count,
        "total": len(positions_data),
        "results": results
    }), 200

@positions_bp.route("/positions/from-binance", methods=["POST"])
def sync_from_binance():
    """从币安同步持仓数据到本地数据库"""
    data = request.get_json(silent=True) or {}
    
    # 获取可选参数
    clear_existing = data.get("clearExisting", False)  # 是否清空现有数据
    filter_zero = data.get("filterZero", True)  # 是否过滤零持仓
    
    try:
        # 尝试导入币安API
        try:
            from binance.api import API
        except ImportError:
            return jsonify({
                "error": "币安API模块未安装",
                "suggestion": "请检查vendor目录中的binance模块"
            }), 500
        
        # 获取环境变量中的 API 密钥
        api_key = os.environ.get("BINANCE_API_KEY")
        api_secret = os.environ.get("BINANCE_API_SECRET")
        
        if not api_key or not api_secret:
            return jsonify({
                "error": "缺少 BINANCE_API_KEY 或 BINANCE_API_SECRET 环境变量"
            }), 400
        
        # 创建 API 连接
        api = API(
            api_key=api_key, 
            api_secret=api_secret, 
            base_url="https://fapi.binance.com",
            timeout=30
        )
        
        # 获取币安持仓信息
        binance_positions = api.sign_request("GET", "/fapi/v2/positionRisk")
        
        if not isinstance(binance_positions, list):
            return jsonify({"error": "币安API返回数据格式错误"}), 500
        
        # 过滤零持仓
        active_positions = []
        if filter_zero:
            for pos in binance_positions:
                if isinstance(pos, dict) and float(pos.get("positionAmt", 0)) != 0:
                    active_positions.append(pos)
        else:
            active_positions = binance_positions
        
        # 清空现有数据（如果需要）
        if clear_existing:
            Position.query.delete()
            db.session.commit()
        
        # 转换币安数据为本地格式并保存
        success_count = 0
        error_count = 0
        errors = []
        
        for binance_pos in active_positions:
            try:
                # 映射币安数据到 ContractPosition 格式
                position_data = {
                    "symbol": binance_pos.get("symbol"),
                    "entryPrice": binance_pos.get("entryPrice"),
                    "markPrice": binance_pos.get("markPrice"),
                    "unRealizedProfit": binance_pos.get("unRealizedProfit"),
                    "liquidationPrice": binance_pos.get("liquidationPrice") if binance_pos.get("liquidationPrice") != "0" else None,
                    "breakEvenPrice": binance_pos.get("breakEvenPrice") if binance_pos.get("breakEvenPrice") else None,
                    "leverage": binance_pos.get("leverage"),
                    "positionAmt": binance_pos.get("positionAmt"),
                    "positionSide": "LONG" if float(binance_pos.get("positionAmt", 0)) > 0 else "SHORT",
                    "updateTime": int(binance_pos.get("updateTime", time.time() * 1000))
                }
                
                # 生成唯一ID
                position_data["id"] = f"binance-{binance_pos.get('symbol')}-{int(time.time() * 1000)}"
                
                payload, code = create_position_record(Position, db, position_data)
                if code == 200:
                    success_count += 1
                else:
                    error_count += 1
                    errors.append({
                        "symbol": position_data.get("symbol"),
                        "error": payload
                    })
                    
            except Exception as e:
                error_count += 1
                errors.append({
                    "symbol": binance_pos.get("symbol", "unknown"),
                    "error": str(e)
                })
        
        return jsonify({
            "message": "同步完成",
            "total_binance_positions": len(binance_positions),
            "active_positions": len(active_positions),
            "success_count": success_count,
            "error_count": error_count,
            "errors": errors[:10] if errors else [],  # 最多返回前10个错误
            "cleared_existing": clear_existing
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": f"同步失败: {str(e)}",
            "error_type": type(e).__name__
        }), 500

@positions_bp.route("/positions/<string:entry_id>", methods=["PUT", "PATCH"])
def update_position(entry_id):
    """更新持仓记录"""
    data = request.get_json(silent=True) or {}
    payload, code = update_position_record(Position, db, entry_id, data)
    return jsonify(payload), code

@positions_bp.route("/positions/<string:entry_id>", methods=["DELETE"])
def delete_position(entry_id):
    """删除持仓记录"""
    payload, code = delete_position_record(Position, db, entry_id)
    return jsonify(payload), code

@positions_bp.route("/positions/binance", methods=["GET"])
def get_binance_positions():
    """获取币安合约持仓信息"""
    try:
        # 尝试导入币安API
        try:
            from binance.api import API
        except ImportError:
            return jsonify({
                "error": "币安API模块未安装",
                "suggestion": "请检查vendor目录中的binance模块"
            }), 500
        
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

@positions_bp.route("/positions/binance/test", methods=["GET"])
def test_binance_connection():
    """测试币安连接状态"""
    try:
        # 尝试导入币安API
        try:
            from binance.api import API
        except ImportError:
            return jsonify({
                "success": False,
                "error": "币安API模块未安装",
                "suggestion": "请检查vendor目录中的binance模块"
            }), 500
        
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