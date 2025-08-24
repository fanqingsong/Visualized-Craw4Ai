#!/bin/bash

echo "🚀 启动 Visualized-Craw4AI 项目..."

# 检查Docker是否运行
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker未运行，请先启动Docker"
    exit 1
fi

# 检查docker compose是否可用
if ! docker compose version > /dev/null 2>&1; then
    echo "❌ docker compose不可用，请检查安装"
    exit 1
fi

echo "📦 构建并启动服务..."
docker compose up --build -d

echo "⏳ 等待服务启动..."
sleep 10

# 检查服务状态
echo "🔍 检查服务状态..."
docker compose ps

echo "✅ 服务启动完成！"
echo ""
echo "🌐 访问地址："
echo "   - 前端应用: http://localhost"
echo "   - 后端API: http://localhost:8000"
echo "   - 数据库: localhost:5432"
echo "   - Redis: localhost:6379"
echo ""
echo "📋 常用命令："
echo "   - 查看日志: docker compose logs -f"
echo "   - 停止服务: docker compose down"
echo "   - 重启服务: docker compose restart"
echo "   - 查看状态: docker compose ps"

