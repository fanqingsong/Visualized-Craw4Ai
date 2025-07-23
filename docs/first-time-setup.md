# 🚀 首次设置完整指南

## 📋 系统要求

- **Python 3.8+** (推荐 3.9 或更高版本)
- **Node.js 16+** 和 npm
- **macOS/Linux/Windows** 系统

## 🔧 首次设置步骤

### 1. 检查 Python 版本

在 macOS 系统中，通常需要使用 `python3` 而不是 `python`：

```bash
# 检查 Python 版本
python3 --version
# 应该显示 Python 3.8+ 版本

# 查找 Python 位置
which python3
```

### 2. 创建虚拟环境

**⚠️ 重要：在 macOS 上使用 `python3` 命令**

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 验证虚拟环境
which python
# 应该显示: /path/to/your/project/venv/bin/python

python --version
# 现在应该可以使用 python 命令了
```

### 3. 安装 Python 依赖

```bash
# 确保虚拟环境已激活 (命令提示符应显示 (venv))
pip install -r requirements.txt
```

### 4. 设置 Crawl4AI 浏览器环境

```bash
# 安装 Playwright 浏览器
crawl4ai-setup
```

看到以下信息表示成功：
```
[COMPLETE] ● Playwright installation completed successfully.
[COMPLETE] ● Database initialization completed successfully.
[COMPLETE] ● Post-installation setup completed!
```

### 5. 安装前端依赖

```bash
# 进入前端目录
cd frontend

# 安装 Node.js 依赖
npm install

# 返回根目录
cd ..
```

### 6. 启动项目

```bash
# 确保虚拟环境已激活
source venv/bin/activate  # 如果还没激活

# 一键启动
python scripts/start.py
```

## 📍 访问地址

启动成功后，访问以下地址：

- **前端应用**: http://localhost:5173
- **后端 API**: http://localhost:8000  
- **API 文档**: http://localhost:8000/docs

## 🔍 常见问题解决

### Q1: `python: command not found`

**解决方案**: 在 macOS 上使用 `python3`
```bash
python3 -m venv venv
source venv/bin/activate
# 激活后就可以使用 python 命令了
```

### Q2: 依赖安装失败

**解决方案**: 确保虚拟环境已激活
```bash
# 检查是否在虚拟环境中
which python
# 应该指向 venv/bin/python

# 如果不是，重新激活
source venv/bin/activate
```

### Q3: 端口被占用

**解决方案**: 
```bash
# 查看占用端口的进程
lsof -ti:8000
lsof -ti:5173

# 杀死进程
kill -9 <PID>
```

### Q4: Crawl4AI 浏览器设置失败

**解决方案**: 
```bash
# 重新运行设置
crawl4ai-setup

# 或者手动安装 Playwright
pip install playwright
playwright install
```

### Q5: 前端启动失败

**解决方案**: 
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

## 🎯 验证安装

运行以下命令验证所有组件正常：

```bash
# 1. 检查虚拟环境
which python
python --version

# 2. 检查关键依赖
python -c "import crawl4ai; print('Crawl4AI OK')"
python -c "import fastapi; print('FastAPI OK')"

# 3. 检查前端依赖
cd frontend && npm list react && cd ..

# 4. 启动项目
python scripts/start.py
```

## 💡 开发提示

1. **每次开发前都要激活虚拟环境**：
   ```bash
   source venv/bin/activate
   ```

2. **检查命令提示符**：
   - 激活虚拟环境后应该看到 `(venv)`
   - 例如：`(venv) user@computer project %`

3. **添加新依赖时**：
   ```bash
   pip install new-package
   pip freeze > requirements.txt  # 更新依赖文件
   ```

4. **项目结构**：
   ```
   项目根目录/
   ├── venv/          # 虚拟环境 (不提交到Git)
   ├── backend/       # 后端代码
   ├── frontend/      # 前端代码
   ├── scripts/       # 启动脚本
   └── requirements.txt
   ```

## 🚀 快速命令参考

```bash
# 完整的首次设置流程
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
crawl4ai-setup
cd frontend && npm install && cd ..
python scripts/start.py

# 日常开发启动
source venv/bin/activate
python scripts/start.py
```

现在你的 Crawl4AI 可视化工具已经准备就绪！🎉 