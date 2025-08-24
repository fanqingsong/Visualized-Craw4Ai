#!/usr/bin/env python3
"""
简化的FastAPI应用，用于测试爬虫功能
"""

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from app.services.crawler_service import CrawlerService

# 创建FastAPI应用
app = FastAPI(title="Crawl4AI 测试", version="1.0.0")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建爬虫服务
crawler_service = CrawlerService()

# 请求模型
class CrawlRequest(BaseModel):
    url: str

class CrawlResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None

@app.get("/")
async def root():
    return {"message": "Crawl4AI 测试服务"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/crawl", response_model=CrawlResponse)
async def crawl_url(request: CrawlRequest):
    """爬取单个URL"""
    try:
        from app.models.schemas import CrawlConfig
        
        result = await crawler_service.crawl_single(
            url=request.url,
            config=CrawlConfig()
        )
        
        if result.success:
            return CrawlResponse(
                success=True,
                message="爬取成功",
                data={
                    "url": result.url,
                    "title": result.title,
                    "content_length": len(result.markdown) if result.markdown else 0,
                    "status_code": result.status_code
                }
            )
        else:
            return CrawlResponse(
                success=False,
                message=f"爬取失败: {result.error_message}"
            )
            
    except Exception as e:
        return CrawlResponse(
            success=False,
            message=f"爬取异常: {str(e)}"
        )

@app.get("/test")
async def test_crawler():
    """测试爬虫连接"""
    try:
        result = await crawler_service.test_connection()
        return {
            "success": True,
            "message": "爬虫测试成功",
            "data": result
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"爬虫测试失败: {str(e)}"
        }

if __name__ == "__main__":
    uvicorn.run(
        "run_simple:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
