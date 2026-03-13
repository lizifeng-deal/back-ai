import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "vendor"))
from binance.api import API

# 获取环境变量
api_key = os.environ.get("BINANCE_API_KEY")
api_secret = os.environ.get("BINANCE_API_SECRET")

if not api_key or not api_secret:
    raise RuntimeError("missing BINANCE_API_KEY/BINANCE_API_SECRET")

print(f"API Key: {api_key[:10]}...")
print(f"API Secret: {api_secret[:10]}...")

# 使用更长的超时时间，与接口一致
api = API(
    api_key=api_key, 
    api_secret=api_secret, 
    base_url="https://fapi.binance.com",
    timeout=30  # 30秒超时
)

print(f"API Base URL: {api.base_url}")
print(f"API Timeout: {api.timeout}")

try:
    print("\n--- 开始查询币安合约持仓 ---")
    positions = api.sign_request("GET", "/fapi/v2/positionRisk")
    
    print("✅ 查询成功")
    print(f"返回数据类型: {type(positions)}")
    print(f"总symbol数量: {len(positions) if isinstance(positions, list) else 0}")
    
    # 统计非零持仓
    non_zero_count = 0
    if isinstance(positions, list):
        for pos in positions:
            if isinstance(pos, dict):
                position_amt = float(pos.get("positionAmt", 0))
                if position_amt != 0:
                    non_zero_count += 1
                    symbol = pos.get("symbol")
                    entry_price = float(pos.get("entryPrice", 0))
                    unrealized_pnl = float(pos.get("unRealizedProfit", 0))
                    print(f"{symbol}: 持仓数量={position_amt}, 开仓价={entry_price}, 未实现盈亏={unrealized_pnl}")
    
    if non_zero_count == 0:
        print("无持仓或所有持仓数量为零")
    
    print(f"\n--- 汇总信息 ---")
    print(f"总交易对数量: {len(positions) if isinstance(positions, list) else 0}")
    print(f"非零持仓数量: {non_zero_count}")
    
except Exception as e:
    print(f"❌ 查询持仓失败: {e}")
    print(f"错误类型: {type(e).__name__}")