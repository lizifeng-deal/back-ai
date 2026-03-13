#!/usr/bin/env python3
"""
Debug Tools 调试工具集启动器
用于方便地运行各种调试工具
"""

import os
import sys
import subprocess

def clear_screen():
    """清屏"""
    os.system('cls' if os.name == 'nt' else 'clear')

def run_script(script_path, working_dir=None):
    """运行Python脚本"""
    try:
        if working_dir:
            original_cwd = os.getcwd()
            os.chdir(working_dir)
        
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=False, 
                              text=True)
        
        if working_dir:
            os.chdir(original_cwd)
            
        return result.returncode == 0
    except Exception as e:
        print(f"运行脚本失败: {e}")
        return False

def show_file(file_path):
    """显示文件内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print(content)
        return True
    except Exception as e:
        print(f"读取文件失败: {e}")
        return False

def main_menu():
    """主菜单"""
    while True:
        clear_screen()
        print("=" * 50)
        print("        Debug Tools 调试工具集")
        print("=" * 50)
        print()
        print("请选择要运行的调试工具:")
        print()
        print("[1] 币安连接诊断 (diagnose_binance.py)")
        print("[2] 币安API测试 (test_binance_debug.py)")  
        print("[3] 查看币安API指南")
        print("[4] 运行调试模板示例")
        print("[5] 显示debug_tools文件夹结构")
        print("[0] 退出")
        print()
        
        choice = input("请输入选择 (0-5): ").strip()
        
        if choice == '0':
            print("\n感谢使用调试工具集！")
            break
        elif choice == '1':
            print("\n=== 运行币安连接诊断工具 ===")
            run_script("diagnose_binance.py", "debug_tools/binance")
        elif choice == '2':
            print("\n=== 运行币安API测试 ===")
            run_script("test_binance_debug.py", "debug_tools/binance")
        elif choice == '3':
            print("\n=== 币安API指南 ===")
            show_file("debug_tools/binance/BINANCE_API_GUIDE.md")
        elif choice == '4':
            print("\n=== 运行调试模板示例 ===")
            run_script("debug_template.py", "debug_tools/templates")
        elif choice == '5':
            print("\n=== Debug Tools 文件夹结构 ===")
            show_directory_tree("debug_tools")
        else:
            print("\n无效选择，请重新输入")
        
        if choice != '0':
            input("\n按Enter键返回主菜单...")

def show_directory_tree(path, prefix="", max_depth=3, current_depth=0):
    """显示目录树结构"""
    if current_depth >= max_depth:
        return
        
    try:
        items = sorted(os.listdir(path))
        dirs = [item for item in items if os.path.isdir(os.path.join(path, item))]
        files = [item for item in items if os.path.isfile(os.path.join(path, item))]
        
        # 显示文件夹
        for i, dirname in enumerate(dirs):
            is_last_dir = (i == len(dirs) - 1) and len(files) == 0
            print(f"{prefix}{'└── ' if is_last_dir else '├── '}{dirname}/")
            
            extension = "    " if is_last_dir else "│   "
            show_directory_tree(
                os.path.join(path, dirname), 
                prefix + extension, 
                max_depth, 
                current_depth + 1
            )
        
        # 显示文件
        for i, filename in enumerate(files):
            is_last = i == len(files) - 1
            print(f"{prefix}{'└── ' if is_last else '├── '}{filename}")
            
    except PermissionError:
        print(f"{prefix}[权限不足]")
    except Exception as e:
        print(f"{prefix}[错误: {e}]")

if __name__ == "__main__":
    # 确保在项目根目录运行
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    os.chdir(project_root)
    
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n用户中断，退出程序")
    except Exception as e:
        print(f"\n程序出错: {e}")
        input("按Enter键退出...")