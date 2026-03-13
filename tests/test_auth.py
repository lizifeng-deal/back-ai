#!/usr/bin/env python3
"""
登录模块测试脚本
使用方法: python test_auth.py
"""

import requests
import json
import sys
import time

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 测试配置
BASE_URL = "http://localhost:3000"
TEST_USERNAME = "testuser"
TEST_PASSWORD = "password123"
TEST_EMAIL = "test@example.com"

class AuthTester:
    """认证功能测试器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.test_results = []
        
    def log_test(self, test_name, success, message=""):
        """记录测试结果"""
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status} - {test_name}")
        if message:
            print(f"      {message}")
        self.test_results.append({
            'name': test_name,
            'success': success,
            'message': message
        })
        
    def test_server_running(self):
        """测试服务器是否运行"""
        try:
            response = self.session.get(f"{BASE_URL}/auth/status")
            success = response.status_code == 200
            self.log_test("服务器连接测试", success, 
                         f"响应状态码: {response.status_code}")
            return success
        except requests.exceptions.ConnectionError:
            self.log_test("服务器连接测试", False, 
                         "无法连接到服务器，请确保应用正在运行")
            return False
        except Exception as e:
            self.log_test("服务器连接测试", False, f"连接错误: {str(e)}")
            return False
    
    def test_user_registration(self):
        """测试用户注册"""
        try:
            # 先尝试删除可能存在的测试用户（通过登录失败来确认）
            url = f"{BASE_URL}/auth/register"
            data = {
                "username": TEST_USERNAME,
                "password": TEST_PASSWORD,
                "email": TEST_EMAIL
            }
            
            response = self.session.post(url, json=data)
            
            if response.status_code == 201:
                self.log_test("用户注册测试", True, "注册成功")
                return True
            elif response.status_code == 409:
                # 用户已存在，这也算正常情况
                self.log_test("用户注册测试", True, "用户已存在（正常）")
                return True
            else:
                self.log_test("用户注册测试", False, 
                             f"注册失败: {response.json().get('error', '未知错误')}")
                return False
                
        except Exception as e:
            self.log_test("用户注册测试", False, f"请求异常: {str(e)}")
            return False
    
    def test_user_login(self):
        """测试用户登录"""
        try:
            url = f"{BASE_URL}/auth/login"
            data = {
                "username": TEST_USERNAME,
                "password": TEST_PASSWORD
            }
            
            response = self.session.post(url, json=data)
            
            if response.status_code == 200:
                data = response.json()
                if 'user' in data:
                    self.log_test("用户登录测试", True, 
                                 f"登录成功，用户ID: {data['user']['id']}")
                    return True
                else:
                    self.log_test("用户登录测试", False, "响应数据格式错误")
                    return False
            else:
                error_msg = response.json().get('error', '未知错误')
                self.log_test("用户登录测试", False, f"登录失败: {error_msg}")
                return False
                
        except Exception as e:
            self.log_test("用户登录测试", False, f"请求异常: {str(e)}")
            return False
    
    def test_auth_status(self):
        """测试认证状态检查"""
        try:
            url = f"{BASE_URL}/auth/status"
            response = self.session.get(url)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('authenticated'):
                    self.log_test("认证状态测试", True, 
                                 f"用户已认证: {data['user']['username']}")
                    return True
                else:
                    self.log_test("认证状态测试", False, "用户未认证")
                    return False
            else:
                self.log_test("认证状态测试", False, 
                             f"请求失败: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("认证状态测试", False, f"请求异常: {str(e)}")
            return False
    
    def test_get_profile(self):
        """测试获取用户信息"""
        try:
            url = f"{BASE_URL}/auth/profile"
            response = self.session.get(url)
            
            if response.status_code == 200:
                data = response.json()
                if 'user' in data:
                    user = data['user']
                    self.log_test("获取用户信息测试", True, 
                                 f"用户: {user['username']}, 邮箱: {user.get('email', 'N/A')}")
                    return True
                else:
                    self.log_test("获取用户信息测试", False, "响应数据格式错误")
                    return False
            else:
                error_msg = response.json().get('error', '未知错误')
                self.log_test("获取用户信息测试", False, f"请求失败: {error_msg}")
                return False
                
        except Exception as e:
            self.log_test("获取用户信息测试", False, f"请求异常: {str(e)}")
            return False
    
    def test_update_profile(self):
        """测试更新用户信息"""
        try:
            url = f"{BASE_URL}/auth/profile"
            new_email = "updated@example.com"
            data = {"email": new_email}
            
            response = self.session.put(url, json=data)
            
            if response.status_code == 200:
                response_data = response.json()
                if response_data['user']['email'] == new_email:
                    self.log_test("更新用户信息测试", True, 
                                 f"邮箱更新成功: {new_email}")
                    return True
                else:
                    self.log_test("更新用户信息测试", False, "邮箱更新失败")
                    return False
            else:
                error_msg = response.json().get('error', '未知错误')
                self.log_test("更新用户信息测试", False, f"更新失败: {error_msg}")
                return False
                
        except Exception as e:
            self.log_test("更新用户信息测试", False, f"请求异常: {str(e)}")
            return False
    
    def test_change_password(self):
        """测试修改密码"""
        try:
            url = f"{BASE_URL}/auth/change-password"
            data = {
                "current_password": TEST_PASSWORD,
                "new_password": TEST_PASSWORD + "_new"
            }
            
            response = self.session.post(url, json=data)
            
            if response.status_code == 200:
                self.log_test("修改密码测试", True, "密码修改成功")
                
                # 使用新密码重新登录
                login_url = f"{BASE_URL}/auth/login"
                login_data = {
                    "username": TEST_USERNAME,
                    "password": TEST_PASSWORD + "_new"
                }
                
                login_response = self.session.post(login_url, json=login_data)
                if login_response.status_code == 200:
                    self.log_test("新密码登录测试", True, "使用新密码登录成功")
                    return True
                else:
                    self.log_test("新密码登录测试", False, "使用新密码登录失败")
                    return False
            else:
                error_msg = response.json().get('error', '未知错误')
                self.log_test("修改密码测试", False, f"修改失败: {error_msg}")
                return False
                
        except Exception as e:
            self.log_test("修改密码测试", False, f"请求异常: {str(e)}")
            return False
    
    def test_logout(self):
        """测试用户登出"""
        try:
            url = f"{BASE_URL}/auth/logout"
            response = self.session.post(url)
            
            if response.status_code == 200:
                # 验证登出是否成功
                status_url = f"{BASE_URL}/auth/status"
                status_response = self.session.get(status_url)
                
                if status_response.status_code == 200:
                    status_data = status_response.json()
                    if not status_data.get('authenticated'):
                        self.log_test("用户登出测试", True, "登出成功")
                        return True
                    else:
                        self.log_test("用户登出测试", False, "登出后仍处于认证状态")
                        return False
                else:
                    self.log_test("用户登出测试", False, "无法验证登出状态")
                    return False
            else:
                error_msg = response.json().get('error', '未知错误')
                self.log_test("用户登出测试", False, f"登出失败: {error_msg}")
                return False
                
        except Exception as e:
            self.log_test("用户登出测试", False, f"请求异常: {str(e)}")
            return False
    
    def run_all_tests(self):
        """运行所有测试"""
        print("=" * 50)
        print("登录模块功能测试")
        print("=" * 50)
        
        # 测试列表
        tests = [
            ("服务器连接", self.test_server_running),
            ("用户注册", self.test_user_registration),
            ("用户登录", self.test_user_login),
            ("认证状态", self.test_auth_status),
            ("获取用户信息", self.test_get_profile),
            ("更新用户信息", self.test_update_profile),
            ("修改密码", self.test_change_password),
            ("用户登出", self.test_logout),
        ]
        
        # 运行测试
        for test_name, test_func in tests:
            try:
                test_func()
            except Exception as e:
                self.log_test(f"{test_name}异常", False, f"测试异常: {str(e)}")
            time.sleep(0.5)  # 短暂延迟
        
        # 统计结果
        print("\n" + "=" * 50)
        print("测试结果统计")
        print("=" * 50)
        
        total_tests = len(self.test_results)
        passed_tests = len([t for t in self.test_results if t['success']])
        failed_tests = total_tests - passed_tests
        
        print(f"总测试数: {total_tests}")
        print(f"通过测试: {passed_tests}")
        print(f"失败测试: {failed_tests}")
        print(f"通过率: {passed_tests/total_tests*100:.1f}%")
        
        if failed_tests > 0:
            print("\n失败的测试:")
            for test in self.test_results:
                if not test['success']:
                    print(f"  - {test['name']}: {test['message']}")
        
        return passed_tests == total_tests

def main():
    """主函数"""
    print("开始测试登录模块...")
    print(f"测试目标: {BASE_URL}")
    print(f"测试用户: {TEST_USERNAME}")
    
    tester = AuthTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 所有测试通过！登录模块工作正常。")
        sys.exit(0)
    else:
        print("\n❌ 部分测试失败，请检查问题。")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n测试被用户中断。")
        sys.exit(1)
    except Exception as e:
        print(f"\n测试过程发生异常: {str(e)}")
        sys.exit(1)