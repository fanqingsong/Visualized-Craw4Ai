#!/usr/bin/env python3
"""
Crawl4AI 可视化工具 - 后端启动脚本
"""

import os
import sys
import subprocess
from pathlib import Path

# 获取项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"

def main():
    """启动后端服务"""
    print("🚀 启动 Crawl4AI 后端服务...")
    print("=" * 40)
    
    # 检查后端目录
    if not BACKEND_DIR.exists():
        print(f"❌ 后端目录不存在: {BACKEND_DIR}")
        sys.exit(1)
    
    # 检查依赖
    try:
        import crawl4ai
        import fastapi
        import uvicorn
        print("✅ 依赖检查通过")
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print(f"请运行: pip install -r {BACKEND_DIR}/requirements.txt")
        sys.exit(1)
    
    print(f"📍 后端服务地址: http://localhost:8000")
    print(f"📚 API 文档: http://localhost:8000/docs")
    print("按 Ctrl+C 停止服务")
    print("=" * 40)
    
    try:
        # 设置环境变量
        env = os.environ.copy()
        env["PYTHONPATH"] = str(PROJECT_ROOT)
        
        # 启动 FastAPI 服务
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "app.main:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ], cwd=BACKEND_DIR, env=env)
        
    except KeyboardInterrupt:
        print("\n🛑 后端服务已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 