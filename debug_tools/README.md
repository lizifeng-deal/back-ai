# Debug Tools 调试工具文件夹

这个文件夹包含各种调试和测试工具，用于排查项目中的问题。

## 文件夹结构

```
debug_tools/
├── README.md                    # 本说明文件
├── binance/                     # 币安相关调试工具
│   ├── diagnose_binance.py      # 币安连接诊断工具
│   ├── test_binance_debug.py    # 币安API调试脚本
│   └── BINANCE_API_GUIDE.md     # 币安API问题分析指南
└── templates/                   # 调试工具模板
    └── debug_template.py        # 通用调试脚本模板
```

## 使用规范

### 1. 文件组织
- 按功能或模块分类创建子文件夹
- 每个调试工具都应包含详细的说明文档
- 使用描述性的文件名

### 2. 命名规范
- 诊断工具：`diagnose_*.py`
- 测试工具：`test_*.py`
- 模拟工具：`mock_*.py`
- 说明文档：`*.md`

### 3. 脚本要求
- 每个脚本都应该可以独立运行
- 包含详细的输出和错误信息
- 提供清晰的使用说明
- 处理异常情况

### 4. 添加新工具
当添加新的调试工具时：
1. 在相应的子文件夹中创建脚本
2. 更新对应的README文档
3. 确保工具能够独立运行
4. 提供使用示例

## 当前工具清单

### 币安相关 (binance/)
- `diagnose_binance.py` - 全面的币安API连接诊断工具
- `test_binance_debug.py` - 币安API调用调试和测试
- `BINANCE_API_GUIDE.md` - 币安API问题分析和解决方案

## 使用示例

```bash
# 进入调试工具目录
cd debug_tools

# 运行币安诊断工具
python binance/diagnose_binance.py

# 运行币安调试测试
python binance/test_binance_debug.py
```

## 注意事项

1. **安全性**：调试工具可能包含敏感信息，注意不要将真实的API密钥提交到版本控制
2. **环境依赖**：确保调试工具的依赖与主项目保持一致
3. **文档更新**：添加新工具时记得更新相关文档
4. **清理**：定期清理过时的调试工具