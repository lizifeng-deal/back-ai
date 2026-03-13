@echo off
echo ======================================
echo        Debug Tools 调试工具集
echo ======================================
echo.

:MENU
echo 请选择要运行的调试工具:
echo.
echo [1] 币安连接诊断 (diagnose_binance.py)
echo [2] 币安API测试 (test_binance_debug.py)
echo [3] 查看币安API指南
echo [4] 运行调试模板示例
echo [0] 退出
echo.

set /p choice=请输入选择 (0-4): 

if "%choice%"=="0" goto EXIT
if "%choice%"=="1" goto BINANCE_DIAGNOSE
if "%choice%"=="2" goto BINANCE_TEST
if "%choice%"=="3" goto BINANCE_GUIDE
if "%choice%"=="4" goto TEMPLATE_TEST

echo 无效选择，请重新输入
echo.
goto MENU

:BINANCE_DIAGNOSE
echo.
echo === 运行币安连接诊断工具 ===
cd debug_tools\binance
python diagnose_binance.py
cd ..\..
goto CONTINUE

:BINANCE_TEST
echo.
echo === 运行币安API测试 ===
cd debug_tools\binance
python test_binance_debug.py
cd ..\..
goto CONTINUE

:BINANCE_GUIDE
echo.
echo === 查看币安API指南 ===
type debug_tools\binance\BINANCE_API_GUIDE.md | more
goto CONTINUE

:TEMPLATE_TEST
echo.
echo === 运行调试模板示例 ===
cd debug_tools\templates
python debug_template.py
cd ..\..
goto CONTINUE

:CONTINUE
echo.
echo 按任意键返回主菜单...
pause >nul
echo.
goto MENU

:EXIT
echo.
echo 感谢使用调试工具集！
exit /b 0