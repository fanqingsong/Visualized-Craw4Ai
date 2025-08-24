#!/bin/bash

echo "🛑 停止 Visualized-Craw4AI 项目..."

# 停止所有服务
docker compose down

echo "🧹 清理资源..."
docker system prune -f

echo "✅ 服务已停止并清理完成！"

