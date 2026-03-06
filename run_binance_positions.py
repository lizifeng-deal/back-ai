import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "vendor"))
from binance.api import API

api_key = os.environ.get("BINANCE_API_KEY")
api_secret = os.environ.get("BINANCE_API_SECRET")
if not api_key or not api_secret:
    raise RuntimeError("missing BINANCE_API_KEY/BINANCE_API_SECRET")

# 使用 binance-connector 的 API 基类连接 USDT 合约
api = API(api_key=api_key, api_secret=api_secret, base_url="https://fapi.binance.com")
try:
    positions = api.sign_request("GET", "/fapi/v2/positionRisk")
    for pos in positions:
        symbol = pos.get("symbol")
        position_amt = float(pos.get("positionAmt", 0))
        entry_price = float(pos.get("entryPrice", 0))
        unrealized_pnl = float(pos.get("unRealizedProfit", 0))
        if position_amt != 0:
            print(f"{symbol}: 持仓数量={position_amt}, 开仓价={entry_price}, 未实现盈亏={unrealized_pnl}")
    if not positions:
        print("无持仓或返回为空")
except Exception as e:
    print("查询持仓失败:", e)
