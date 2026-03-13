# 项目调试工具使用说明

## Debug Tools 文件夹

已创建 `debug_tools/` 文件夹，包含各种调试和测试工具，用于排查项目中的问题。

### 快速启动

#### 方法1：使用Python启动器（推荐）
```bash
python debug_tools/run_debug.py
```

#### 方法2：使用批处理脚本（Windows）
```bash
debug_tools/run_debug.bat
```

#### 方法3：直接运行特定工具
```bash
# 币安连接诊断
python debug_tools/binance/diagnose_binance.py

# 币安API测试
python debug_tools/binance/test_binance_debug.py

# 查看调试模板示例
python debug_tools/templates/debug_template.py
```

### 文件夹结构

```
debug_tools/
├── README.md                    # 详细说明文档
├── run_debug.py                 # Python启动器（推荐）
├── run_debug.bat                # Windows批处理启动器
├── binance/                     # 币安相关调试工具
│   ├── diagnose_binance.py      # 币安连接诊断工具
│   ├── test_binance_debug.py    # 币安API调试脚本
│   └── BINANCE_API_GUIDE.md     # 币安API问题分析指南
└── templates/                   # 调试工具模板
    └── debug_template.py        # 通用调试脚本模板
```

### 添加新的调试工具

1. 根据功能创建相应的子文件夹
2. 使用 `debug_tools/templates/debug_template.py` 作为模板
3. 更新相关的README文档
4. 如需要，更新启动脚本

### 规范

- 诊断工具：`diagnose_*.py`
- 测试工具：`test_*.py`
- 模拟工具：`mock_*.py`
- 说明文档：`*.md`

所有调试工具生成的临时文件都会被 `.gitignore` 忽略。