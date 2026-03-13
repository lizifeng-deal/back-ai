"""
交易日志蓝图 - 处理交易记录相关功能
"""
from flask import Blueprint, request, jsonify
from app.models.deallog import DealLog
from app import db
from app.utils.deallog_ops import (
    list_deallog_records,
    get_deallog_record,
    create_deallog_record,
    update_deallog_record,
    delete_deallog_record,
    sum_delivery_pnl
)

# 创建交易日志蓝图
deallog_bp = Blueprint("deallog", __name__)

@deallog_bp.route("/dealLog", methods=["GET"])
def list_deallog():
    """获取所有交易日志"""
    payload, code = list_deallog_records(DealLog)
    return jsonify(payload), code

@deallog_bp.route("/dealLog/<string:entry_id>", methods=["GET"])
def get_deallog(entry_id):
    """根据ID获取单个交易日志"""
    payload, code = get_deallog_record(DealLog, entry_id)
    return jsonify(payload), code

@deallog_bp.route("/dealLog", methods=["POST"])
def create_deallog():
    """创建新的交易日志"""
    data = request.get_json(silent=True) or {}
    payload, code = create_deallog_record(DealLog, db, data)
    return jsonify(payload), code

@deallog_bp.route("/dealLog/<string:entry_id>", methods=["PUT", "PATCH"])
def update_deallog(entry_id):
    """更新交易日志"""
    data = request.get_json(silent=True) or {}
    payload, code = update_deallog_record(DealLog, db, entry_id, data)
    return jsonify(payload), code

@deallog_bp.route("/dealLog/<string:entry_id>", methods=["DELETE"])
def delete_deallog(entry_id):
    """删除交易日志"""
    payload, code = delete_deallog_record(DealLog, db, entry_id)
    return jsonify(payload), code

@deallog_bp.route("/dealLog/summary/delivery_pnl", methods=["GET"])
def summary_delivery_pnl():
    """获取交割盈亏汇总"""
    payload, code = sum_delivery_pnl(DealLog, db)
    return jsonify(payload), code