import os
import sys
# 修正路径，因为现在在 debug_tools/binance/ 子文件夹中
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "vendor"))
from binance.api import API
import json

def test_binance_api():
    """测试币安 API 调用，模拟 Flask 接口的环境"""
    print("=== 测试币安 API 调用 ===")
    
    # 获取环境变量
    api_key = os.environ.get("BINANCE_API_KEY")
    api_secret = os.environ.get("BINANCE_API_SECRET")
    
    print(f"API Key: {api_key[:10] + '...' if api_key else 'None'}")
    print(f"API Secret: {api_secret[:10] + '...' if api_secret else 'None'}")
    
    if not api_key or not api_secret:
        print("❌ 缺少环境变量")
        return
    
    try:
        # 创建 API 连接
        api = API(api_key=api_key, api_secret=api_secret, base_url="https://fapi.binance.com")
        
        print("✅ API 对象创建成功")
        print(f"Base URL: {api.base_url}")
        print(f"Timeout: {api.timeout}")
        print(f"Headers: {dict(api.session.headers)}")
        
        # 查询持仓信息
        print("\n--- 开始查询持仓信息 ---")
        positions = api.sign_request("GET", "/fapi/v2/positionRisk")
        
        print("✅ 查询成功")
        print(f"返回数据类型: {type(positions)}")
        print(f"数据长度: {len(positions) if isinstance(positions, list) else '未知'}")
        
        # 处理返回的数据
        if isinstance(positions, list):
            non_zero_positions = []
            for pos in positions:
                if isinstance(pos, dict):
                    position_amt = float(pos.get("positionAmt", 0))
                    if position_amt != 0:
                        non_zero_positions.append(pos)
            
            print(f"非零持仓数量: {len(non_zero_positions)}")
            if non_zero_positions:
                for pos in non_zero_positions:
                    symbol = pos.get("symbol")
                    position_amt = float(pos.get("positionAmt", 0))
                    entry_price = float(pos.get("entryPrice", 0))
                    unrealized_pnl = float(pos.get("unRealizedProfit", 0))
                    print(f"  {symbol}: 数量={position_amt}, 开仓价={entry_price}, 盈亏={unrealized_pnl}")
        
        # 返回模拟 Flask 响应
        result = {
            "success": True,
            "data": positions,
            "total": len(positions) if isinstance(positions, list) else 0
        }
        print(f"\n--- 模拟 Flask 响应 ---")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        return result
        
    except Exception as e:
        error_msg = f"查询币安持仓失败: {str(e)}"
        print(f"❌ {error_msg}")
        
        result = {
            "success": False,
            "error": error_msg
        }
        print(f"\n--- 模拟 Flask 错误响应 ---")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        return result

if __name__ == "__main__":
    test_binance_api()