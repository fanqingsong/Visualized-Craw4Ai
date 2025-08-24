"""
Crawl4AI 可视化工具 - FastAPI 后端
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
import sys
from pathlib import Path

from app.routers import crawler, tasks, projects
from app.models.database import init_db
from app.utils.logging import setup_logging

# 设置日志
logger = setup_logging()

# 创建 FastAPI 应用
app = FastAPI(
    title="Crawl4AI 可视化工具",
    description="基于 crawl4ai 的专业级网页内容提取工具",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(crawler.router, prefix="/api/v1/crawler", tags=["爬虫"])
app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["任务管理"])
app.include_router(projects.router, prefix="/api/v1/projects", tags=["项目管理"])

@app.on_event("startup")
async def startup_event():
    """应用启动时的初始化"""
    logger.info("启动 Crawl4AI 可视化工具后端...")
    await init_db()
    logger.info("数据库初始化完成")

@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时的清理"""
    logger.info("关闭 Crawl4AI 可视化工具后端...")

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "Crawl4AI 可视化工具 API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """健康检查"""
    try:
        # 这里可以添加更多的健康检查逻辑
        # 比如检查数据库连接、Redis 连接等
        return {
            "status": "healthy",
            "message": "服务运行正常"
        }
    except Exception as e:
        logger.error(f"健康检查失败: {e}")
        raise HTTPException(status_code=500, detail="服务异常")

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """全局异常处理"""
    logger.error(f"未处理的异常: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "服务器内部错误"}
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 