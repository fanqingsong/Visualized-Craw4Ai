# 🛠️ 开发环境设置指南

## 虚拟环境设置（重要！）

### 为什么需要虚拟环境？
- **隔离依赖**：避免不同项目之间的包冲突
- **版本管理**：确保每个项目使用正确的包版本
- **环境一致性**：团队成员使用相同的依赖版本

### 1. 创建虚拟环境

```bash
# 方法一：使用 venv（推荐）
python -m venv venv

# 方法二：使用 conda
conda create -n crawl4ai-env python=3.9

# 方法三：使用 virtualenv
pip install virtualenv
virtualenv venv
```

### 2. 激活虚拟环境

```bash
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate

# conda
conda activate crawl4ai-env
```

### 3. 安装依赖

```bash
# 确保虚拟环境已激活
pip install -r requirements.txt

# 或者安装开发版本的依赖
pip install -r backend/requirements.txt
```

### 4. 验证安装

```bash
# 检查 Python 路径
which python
# 应该显示: /path/to/your/project/venv/bin/python

# 检查已安装的包
pip list
```

### 5. 退出虚拟环境

```bash
deactivate
```

## 开发工作流

### 每次开始开发时：

```bash
# 1. 激活虚拟环境
source venv/bin/activate  # macOS/Linux
# 或 venv\Scripts\activate  # Windows

# 2. 启动项目
python scripts/start.py
```

### 添加新依赖时：

```bash
# 1. 激活虚拟环境
source venv/bin/activate

# 2. 安装新包
pip install new-package

# 3. 更新 requirements.txt
pip freeze > requirements.txt
```

## 常见问题

### Q: 为什么不把 venv/ 目录提交到 Git？
A: 因为：
- 虚拟环境包含大量二进制文件（几百MB）
- 不同操作系统的虚拟环境不兼容
- 每个开发者应该创建自己的虚拟环境

### Q: 如何确保团队使用相同的依赖？
A: 通过 `requirements.txt` 文件：
- 锁定具体的包版本
- 所有人使用相同的 requirements.txt 安装

### Q: 启动脚本会自动检查虚拟环境吗？
A: 是的，启动脚本会：
- 检查必要的包是否已安装
- 提示用户安装缺失的依赖
- 但不会自动创建虚拟环境（这应该手动完成）

## IDE 配置

### VS Code
1. 打开命令面板 (Cmd/Ctrl + Shift + P)
2. 选择 "Python: Select Interpreter"
3. 选择虚拟环境中的 Python 解释器

### PyCharm
1. File → Settings → Project → Python Interpreter
2. Add → Existing Environment
3. 选择 venv/bin/python

## 最佳实践

1. **总是使用虚拟环境**
2. **将 venv/ 添加到 .gitignore**（已完成）
3. **定期更新 requirements.txt**
4. **团队成员使用相同的 Python 版本**
5. **在 README 中说明虚拟环境设置** 