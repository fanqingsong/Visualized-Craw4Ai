#!/usr/bin/env python3
"""
Crawl4AI 可视化工具 - 前端启动脚本
"""

import sys
import subprocess
import webbrowser
import time
import threading
from pathlib import Path

# 获取项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"

def check_node_modules():
    """检查并安装前端依赖"""
    if not (FRONTEND_DIR / "node_modules").exists():
        print("📦 安装前端依赖...")
        try:
            subprocess.run(["npm", "install"], cwd=FRONTEND_DIR, check=True)
            print("✅ 前端依赖安装完成")
        except subprocess.CalledProcessError:
            print("❌ 前端依赖安装失败")
            sys.exit(1)
    else:
        print("✅ 前端依赖已存在")

def open_browser():
    """延迟打开浏览器"""
    time.sleep(3)  # 等待 Vite 服务启动
    try:
        webbrowser.open("http://localhost:5173")
        print("🌐 浏览器已打开: http://localhost:5173")
    except Exception as e:
        print(f"⚠️ 无法自动打开浏览器: {e}")
        print("请手动访问: http://localhost:5173")

def main():
    """启动前端服务"""
    print("🌐 启动 Crawl4AI 前端服务...")
    print("=" * 40)
    
    # 检查前端目录
    if not FRONTEND_DIR.exists():
        print(f"❌ 前端目录不存在: {FRONTEND_DIR}")
        sys.exit(1)
    
    # 检查并安装依赖
    check_node_modules()
    
    print(f"📍 前端服务地址: http://localhost:5173")
    print("按 Ctrl+C 停止服务")
    print("=" * 40)
    
    try:
        # 启动浏览器 (在新线程中)
        browser_thread = threading.Thread(target=open_browser, daemon=True)
        browser_thread.start()
        
        # 启动 Vite 开发服务器
        subprocess.run(["npm", "run", "dev"], cwd=FRONTEND_DIR)
        
    except KeyboardInterrupt:
        print("\n🛑 前端服务已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 