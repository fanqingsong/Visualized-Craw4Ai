# 🤖 Crawl4AI 可视化工具

一个基于 Crawl4AI 的专业级可视化网页内容提取工具，采用现代化的前后端分离架构。

## ✨ 功能特性

### 🚀 核心功能
- **单个/批量 URL 爬取**: 支持单个网址或批量处理多个网址
- **智能内容提取**: 基于 AI 的结构化数据提取
- **深度爬取**: 支持多层链接跟踪和智能过滤
- **异步任务管理**: 后台任务处理，实时进度追踪
- **多种导出格式**: Markdown、JSON、CSV 等格式

### 🎯 高级配置
- **爬取策略**: 广度优先(BFF)、深度优先(DFS)、最佳优先等
- **内容过滤**: 智能内容筛选和相关性评分
- **自定义提取**: 通过自然语言描述提取特定数据
- **代理支持**: 代理轮换和反爬虫机制
- **浏览器配置**: 无头模式、用户代理、地理位置等

### 📊 可视化界面
- **直观配置面板**: 可视化设置爬取参数
- **实时监控**: 任务进度和状态实时更新
- **结果预览**: 内置 Markdown 渲染和数据表格
- **项目管理**: 多项目组织和历史记录

## 🏗️ 技术架构

```
┌─────────────────┐    HTTP/REST API    ┌─────────────────┐
│   React 前端     │ ←──────────────────→ │  FastAPI 后端    │
│   (端口 5173)    │                     │   (端口 8000)    │
└─────────────────┘                     └─────────────────┘
         │                                        │
         │                                        │
    ┌─────────┐                              ┌─────────┐
    │ Antd UI │                              │Crawl4AI │
    │ 组件库   │                              │ 引擎    │
    └─────────┘                              └─────────┘
```

### 后端技术栈
- **FastAPI** - 现代化 Python Web 框架
- **Pydantic** - 数据验证和序列化
- **AsyncIO** - 异步编程支持
- **Crawl4AI** - 核心爬虫引擎
- **Uvicorn** - ASGI 服务器

### 前端技术栈
- **React 18** - 用户界面库
- **TypeScript** - 类型安全
- **Vite** - 现代化构建工具
- **Ant Design** - UI 组件库
- **React Query** - 数据获取和缓存
- **React Router** - 路由管理

## 📁 项目结构

```
crawl4ai-visual-tool/
├── 📂 backend/                    # FastAPI 后端
│   ├── 📂 app/
│   │   ├── 📂 models/            # 数据模型
│   │   ├── 📂 routers/           # API 路由
│   │   ├── 📂 services/          # 业务逻辑
│   │   ├── 📂 utils/             # 工具函数
│   │   └── main.py              # 应用入口
│   └── requirements.txt         # Python 依赖
├── 📂 frontend/                  # React 前端
│   ├── 📂 src/
│   │   ├── 📂 components/       # 组件
│   │   ├── 📂 pages/           # 页面
│   │   ├── 📂 services/        # API 服务
│   │   ├── 📂 types/           # 类型定义
│   │   └── main.tsx           # 应用入口
│   ├── package.json           # Node.js 依赖
│   └── vite.config.ts         # Vite 配置
├── 📂 scripts/                  # 启动脚本
│   ├── start.py              # 一键启动
│   ├── start-backend.py      # 后端启动
│   └── start-frontend.py     # 前端启动
├── 📂 docs/                    # 项目文档
├── 📂 tests/                   # 测试文件
├── .gitignore                 # Git 忽略文件
├── README.md                  # 项目文档
└── requirements.txt           # 根级别依赖
```

## 🚦 快速开始

### 环境要求
- Python 3.8+
- Node.js 16+
- npm 或 yarn

### 首次设置（重要！）

```bash
# 1. 创建虚拟环境
python -m venv venv

# 2. 激活虚拟环境
source venv/bin/activate  # macOS/Linux
# 或 venv\Scripts\activate  # Windows

# 3. 安装依赖
pip install -r requirements.txt
```

### 一键启动 (推荐)

```bash
# 确保虚拟环境已激活
source venv/bin/activate  # 如果还没激活

# 启动项目
python scripts/start.py
```

这会自动：
- 检查运行环境
- 安装前端依赖
- 启动后端和前端服务
- 在浏览器中打开应用

### 手动启动

1. **安装 Python 依赖**
```bash
pip install -r requirements.txt
```

2. **启动后端**
```bash
python scripts/start-backend.py
```

3. **启动前端** (新终端)
```bash
python scripts/start-frontend.py
```

### 访问应用
- 🌐 前端应用: http://localhost:5173
- 📚 后端 API 文档: http://localhost:8000/docs
- ⚡ 健康检查: http://localhost:8000/health

## 📚 文档

- [首次设置指南](docs/first-time-setup.md) - **必读！完整设置流程**
- [开发环境设置](docs/development-setup.md) - 虚拟环境详细说明
- [快速启动指南](QUICKSTART.md) - 简化版启动步骤
- [可视化设计方案](docs/visualization-design.md)
- [数据分析工具](docs/data-analysis.md)
- [API 文档](http://localhost:8000/docs) (启动后端后访问)

## 🛠️ 开发

### 开发环境设置

```bash
# 安装后端依赖
pip install -r backend/requirements.txt

# 安装前端依赖
cd frontend && npm install
```

### 运行测试

```bash
# 运行后端测试
python -m pytest tests/

# 运行前端测试
cd frontend && npm test
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🙏 致谢

- [Crawl4AI](https://github.com/unclecode/crawl4ai) - 强大的网页爬取引擎
- [FastAPI](https://fastapi.tiangolo.com/) - 现代化 Python Web 框架
- [React](https://reactjs.org/) - 用户界面库
- [Ant Design](https://ant.design/) - 企业级 UI 设计语言 