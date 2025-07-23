# 🚀 快速启动指南

## ⚠️ 首次使用必读

**必须先创建虚拟环境！** 详细说明请看：[开发环境设置](docs/development-setup.md)

```bash
# 1. 创建虚拟环境（仅首次）
python -m venv venv

# 2. 激活虚拟环境
source venv/bin/activate  # macOS/Linux
# 或 venv\Scripts\activate  # Windows

# 3. 安装依赖（仅首次）
pip install -r requirements.txt
```

## 一键启动（推荐）

```bash
# 确保虚拟环境已激活
source venv/bin/activate  # 如果还没激活

# 启动项目
python scripts/start.py
```

## 分步启动

### 1. 安装依赖

```bash
# 安装 Python 依赖
pip install -r requirements.txt

# 安装前端依赖
cd frontend && npm install && cd ..
```

### 2. 启动服务

```bash
# 启动后端（终端1）
python scripts/start-backend.py

# 启动前端（终端2）
python scripts/start-frontend.py
```

### 3. 访问应用

- 前端应用: http://localhost:5173
- 后端 API: http://localhost:8000
- API 文档: http://localhost:8000/docs

## 故障排除

### 端口被占用
如果端口被占用，可以：
- 杀死占用进程：`lsof -ti:8000 | xargs kill -9`
- 或修改配置文件中的端口号

### 依赖问题
- Python 依赖：`pip install -r requirements.txt`
- Node.js 依赖：`cd frontend && npm install`
- Crawl4AI 设置：`crawl4ai-setup`

### 浏览器未自动打开
手动访问：http://localhost:5173 