#!/bin/bash

echo "🚀 开始测试修复后的爬虫功能..."

# 检查Python环境
echo "📋 检查Python环境..."
python3 --version
pip3 --version

# 安装依赖
echo "📦 安装依赖..."
pip3 install -r requirements.txt

# 安装playwright浏览器
echo "🌐 安装playwright浏览器..."
python3 -m playwright install

# 测试爬虫服务
echo "🧪 测试爬虫服务..."
python3 test_crawler.py

echo "✅ 测试完成！"
echo ""
echo "如果测试成功，可以启动简化服务："
echo "python3 run_simple.py"
echo ""
echo "然后访问："
echo "- http://localhost:8000/ - 根路径"
echo "- http://localhost:8000/test - 测试爬虫连接"
echo "- http://localhost:8000/docs - API文档"
