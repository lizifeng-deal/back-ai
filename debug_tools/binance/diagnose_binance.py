import os
import sys
import time
import json
# 修正路径，因为现在在 debug_tools/binance/ 子文件夹中
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "vendor"))
from binance.api import API

def diagnose_binance_connection():
    """诊断币安连接问题"""
    print("=== 币安连接诊断工具 ===\n")
    
    # 1. 检查环境变量
    print("1. 检查环境变量:")
    api_key = os.environ.get("BINANCE_API_KEY")
    api_secret = os.environ.get("BINANCE_API_SECRET")
    
    if api_key:
        print(f"   ✅ BINANCE_API_KEY: {api_key[:10]}...{api_key[-4:]}")
    else:
        print("   ❌ BINANCE_API_KEY: 未设置")
        return
    
    if api_secret:
        print(f"   ✅ BINANCE_API_SECRET: {api_secret[:10]}...{api_secret[-4:]}")
    else:
        print("   ❌ BINANCE_API_SECRET: 未设置")
        return
    
    # 2. 测试不同的超时设置
    timeout_values = [10, 30, 60, None]
    
    for timeout in timeout_values:
        print(f"\n2. 测试超时设置: {timeout}秒" + (" (默认)" if timeout is None else ""))
        
        try:
            api = API(
                api_key=api_key, 
                api_secret=api_secret, 
                base_url="https://fapi.binance.com",
                timeout=timeout
            )
            
            start_time = time.time()
            positions = api.sign_request("GET", "/fapi/v2/positionRisk")
            end_time = time.time()
            
            print(f"   ✅ 连接成功 (耗时: {end_time - start_time:.2f}秒)")
            print(f"   📊 返回数据: {len(positions)} 个交易对")
            
            # 统计非零持仓
            non_zero_count = sum(1 for pos in positions 
                               if isinstance(pos, dict) and float(pos.get("positionAmt", 0)) != 0)
            print(f"   🎯 非零持仓: {non_zero_count} 个")
            
            # 成功后就停止测试
            print(f"\n   ✅ 最佳超时设置: {timeout}秒")
            return positions
            
        except Exception as e:
            error_type = type(e).__name__
            print(f"   ❌ 连接失败: {error_type}")
            if "timeout" in str(e).lower():
                print(f"   ⏱️ 超时错误，尝试更长的超时时间")
            elif "connection" in str(e).lower():
                print(f"   🌐 网络连接问题")
            else:
                print(f"   🔍 其他错误: {str(e)[:100]}...")
    
    print("\n❌ 所有超时设置都失败了")
    return None

def test_different_endpoints():
    """测试不同的币安端点"""
    print("\n3. 测试不同的币安端点:")
    
    api_key = os.environ.get("BINANCE_API_KEY")
    api_secret = os.environ.get("BINANCE_API_SECRET")
    
    if not api_key or not api_secret:
        print("   ❌ 缺少API密钥")
        return
    
    endpoints = [
        ("现货API", "https://api.binance.com", "/api/v3/account"),
        ("合约API", "https://fapi.binance.com", "/fapi/v2/account"),
        ("合约持仓", "https://fapi.binance.com", "/fapi/v2/positionRisk"),
    ]
    
    for name, base_url, endpoint in endpoints:
        print(f"\n   测试 {name}: {base_url}")
        try:
            api = API(
                api_key=api_key, 
                api_secret=api_secret, 
                base_url=base_url,
                timeout=10
            )
            
            result = api.sign_request("GET", endpoint)
            print(f"   ✅ {name} 连接成功")
            
        except Exception as e:
            print(f"   ❌ {name} 连接失败: {type(e).__name__}")

if __name__ == "__main__":
    positions = diagnose_binance_connection()
    test_different_endpoints()
    
    if positions:
        print(f"\n=== 连接成功汇总 ===")
        print(f"总交易对: {len(positions)}")
        
        # 保存结果到文件
        with open("binance_positions_result.json", "w", encoding="utf-8") as f:
            json.dump(positions, f, indent=2, ensure_ascii=False)
        print("结果已保存到: binance_positions_result.json")