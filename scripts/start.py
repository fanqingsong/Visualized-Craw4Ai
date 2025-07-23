#!/usr/bin/env python3
"""
Crawl4AI 可视化工具 - 一键启动脚本

这个脚本会自动启动后端和前端服务
"""

import os
import sys
import subprocess
import time
import threading
import webbrowser
from pathlib import Path

# 获取项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
FRONTEND_DIR = PROJECT_ROOT / "frontend"

def check_dependencies():
    """检查依赖是否已安装"""
    print("🔍 检查依赖...")
    
    # 检查是否在虚拟环境中
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    if not in_venv:
        print("⚠️  警告: 未检测到虚拟环境")
        print("强烈建议使用虚拟环境:")
        print("  python -m venv venv")
        print("  source venv/bin/activate  # macOS/Linux")
        print("  # 或 venv\\Scripts\\activate  # Windows")
        print("")
    else:
        print("✅ 检测到虚拟环境")
    
    # 检查 Python 依赖
    try:
        import crawl4ai
        import fastapi
        import uvicorn
        print("✅ Python 依赖已安装")
    except ImportError as e:
        print(f"❌ 缺少 Python 依赖: {e}")
        print("请运行: pip install -r requirements.txt")
        if not in_venv:
            print("提示: 建议先激活虚拟环境")
        sys.exit(1)
    
    # 检查 Node.js 依赖
    if not (FRONTEND_DIR / "node_modules").exists():
        print("📦 安装前端依赖...")
        try:
            subprocess.run(["npm", "install"], cwd=FRONTEND_DIR, check=True)
            print("✅ 前端依赖安装完成")
        except subprocess.CalledProcessError:
            print("❌ 前端依赖安装失败")
            sys.exit(1)
    else:
        print("✅ 前端依赖已安装")

def start_backend():
    """启动后端服务"""
    print("🚀 启动后端服务...")
    try:
        # 切换到后端目录并启动 FastAPI
        env = os.environ.copy()
        env["PYTHONPATH"] = str(PROJECT_ROOT)
        
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
        print(f"❌ 后端启动失败: {e}")

def start_frontend():
    """启动前端服务"""
    print("🌐 启动前端服务...")
    try:
        subprocess.run(["npm", "run", "dev"], cwd=FRONTEND_DIR)
    except KeyboardInterrupt:
        print("\n🛑 前端服务已停止")
    except Exception as e:
        print(f"❌ 前端启动失败: {e}")

def open_browser():
    """延迟打开浏览器"""
    time.sleep(3)  # 等待服务启动
    try:
        webbrowser.open("http://localhost:5173")
        print("🌐 浏览器已打开: http://localhost:5173")
    except Exception as e:
        print(f"⚠️ 无法自动打开浏览器: {e}")
        print("请手动访问: http://localhost:5173")

def main():
    """主函数"""
    print("🤖 Crawl4AI 可视化工具启动中...")
    print("=" * 50)
    
    # 检查依赖
    check_dependencies()
    
    print("\n📍 服务地址:")
    print("  前端: http://localhost:5173")
    print("  后端: http://localhost:8000")
    print("  API 文档: http://localhost:8000/docs")
    print("\n按 Ctrl+C 停止所有服务")
    print("=" * 50)
    
    try:
        # 启动后端服务 (在新线程中)
        backend_thread = threading.Thread(target=start_backend, daemon=True)
        backend_thread.start()
        
        # 等待后端启动
        time.sleep(2)
        
        # 启动浏览器 (在新线程中)
        browser_thread = threading.Thread(target=open_browser, daemon=True)
        browser_thread.start()
        
        # 启动前端服务 (主线程)
        start_frontend()
        
    except KeyboardInterrupt:
        print("\n\n🛑 正在停止所有服务...")
        print("👋 再见!")
        sys.exit(0)

if __name__ == "__main__":
    main() 