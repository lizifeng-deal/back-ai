"""
通用调试脚本模板
用于创建新的调试工具时参考

使用方法：
1. 复制此模板到相应的子文件夹
2. 修改脚本名称和功能描述
3. 实现具体的调试逻辑
4. 更新相关文档
"""

import os
import sys
import time
import json
from datetime import datetime

# 根据脚本位置调整路径
# 如果在 debug_tools/ 根目录：
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "vendor"))
# 如果在 debug_tools/子文件夹/ 中：
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "vendor"))

class DebugTool:
    """调试工具基类"""
    
    def __init__(self, name="通用调试工具"):
        self.name = name
        self.start_time = time.time()
        print(f"=== {self.name} ===")
        print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    def log(self, message, level="INFO"):
        """统一的日志输出格式"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        icons = {
            "INFO": "ℹ️",
            "SUCCESS": "✅", 
            "ERROR": "❌",
            "WARNING": "⚠️",
            "DEBUG": "🔍"
        }
        icon = icons.get(level, "📝")
        print(f"[{timestamp}] {icon} {message}")
    
    def check_environment(self, required_vars=None):
        """检查环境变量"""
        self.log("检查环境变量", "INFO")
        
        if not required_vars:
            required_vars = []
        
        missing_vars = []
        for var in required_vars:
            value = os.environ.get(var)
            if value:
                # 隐藏敏感信息，只显示前后几位
                if "key" in var.lower() or "secret" in var.lower():
                    display_value = f"{value[:6]}...{value[-4:]}" if len(value) > 10 else "***"
                else:
                    display_value = value
                self.log(f"   {var}: {display_value}", "SUCCESS")
            else:
                self.log(f"   {var}: 未设置", "ERROR")
                missing_vars.append(var)
        
        return len(missing_vars) == 0
    
    def test_with_timeout(self, test_func, timeouts=None, *args, **kwargs):
        """使用不同超时设置测试功能"""
        if not timeouts:
            timeouts = [5, 10, 30, 60]
        
        self.log("测试不同超时设置", "INFO")
        
        for timeout in timeouts:
            self.log(f"测试超时: {timeout}秒", "INFO")
            try:
                start_time = time.time()
                result = test_func(timeout=timeout, *args, **kwargs)
                end_time = time.time()
                
                self.log(f"测试成功 (耗时: {end_time - start_time:.2f}秒)", "SUCCESS")
                self.log(f"最佳超时设置: {timeout}秒", "SUCCESS")
                return result
                
            except Exception as e:
                error_type = type(e).__name__
                self.log(f"测试失败: {error_type}", "ERROR")
                if "timeout" in str(e).lower():
                    self.log("超时错误，尝试更长的超时时间", "WARNING")
                else:
                    self.log(f"错误详情: {str(e)[:100]}...", "DEBUG")
        
        self.log("所有超时设置都失败了", "ERROR")
        return None
    
    def save_results(self, data, filename=None):
        """保存结果到文件"""
        if not filename:
            filename = f"{self.name.lower().replace(' ', '_')}_result_{int(time.time())}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.log(f"结果已保存到: {filename}", "SUCCESS")
            return True
        except Exception as e:
            self.log(f"保存失败: {str(e)}", "ERROR")
            return False
    
    def finish(self):
        """结束调试，输出总结信息"""
        end_time = time.time()
        duration = end_time - self.start_time
        print(f"\n=== 调试完成 ===")
        print(f"总耗时: {duration:.2f}秒")
        print(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


# 使用示例
def example_test_function(timeout=30, **kwargs):
    """示例测试函数"""
    # 模拟一些测试逻辑
    time.sleep(1)  # 模拟耗时操作
    
    # 返回一些测试结果
    return {
        "status": "success",
        "timeout": timeout,
        "timestamp": datetime.now().isoformat(),
        "data": ["item1", "item2", "item3"]
    }


def main():
    """主函数 - 调试脚本的入口"""
    # 创建调试工具实例
    debug = DebugTool("示例调试工具")
    
    try:
        # 1. 检查环境变量
        required_vars = ["EXAMPLE_API_KEY", "EXAMPLE_SECRET"]  # 根据需要修改
        if not debug.check_environment(required_vars):
            debug.log("环境变量检查失败", "ERROR")
            return
        
        # 2. 执行测试
        debug.log("开始执行测试", "INFO")
        result = debug.test_with_timeout(example_test_function)
        
        if result:
            debug.log(f"测试结果: {result}", "SUCCESS")
            # 3. 保存结果
            debug.save_results(result)
        else:
            debug.log("测试失败", "ERROR")
    
    except KeyboardInterrupt:
        debug.log("用户中断", "WARNING")
    except Exception as e:
        debug.log(f"未预期的错误: {str(e)}", "ERROR")
    finally:
        debug.finish()


if __name__ == "__main__":
    main()