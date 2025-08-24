"""
爬虫相关的 API 路由 - 简化版本
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List
import uuid
import time
import asyncio
from datetime import datetime

from app.models.schemas import (
    SingleCrawlRequest, BatchCrawlRequest, StructuredExtractionRequest,
    CrawlResult, CrawlResponse, TaskResponse, TaskInfo, CrawlStatus
)
from app.services.crawler_service import CrawlerService
from app.services.task_service import TaskService
from app.utils.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)

# 初始化服务
crawler_service = CrawlerService()
task_service = TaskService()

@router.post("/single", response_model=CrawlResponse)
async def crawl_single_url(request: SingleCrawlRequest):
    """
    爬取单个URL - 简化版本
    """
    try:
        logger.info(f"开始爬取单个URL: {request.url}")
        start_time = time.time()
        
        # 调用爬虫服务
        result = await crawler_service.crawl_single(
            url=str(request.url),
            config=request.config
        )
        
        execution_time = time.time() - start_time
        result.execution_time = execution_time
        
        logger.info(f"单个URL爬取完成: {request.url}, 耗时: {execution_time:.2f}s")
        
        return CrawlResponse(
            success=True,
            message="爬取成功",
            data=result
        )
        
    except Exception as e:
        logger.error(f"单个URL爬取失败: {request.url}, 错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"爬取失败: {str(e)}")

@router.post("/batch", response_model=TaskResponse)
async def crawl_batch_urls(request: BatchCrawlRequest, background_tasks: BackgroundTasks):
    """
    批量爬取URLs (异步)
    """
    try:
        # 创建任务
        task_id = str(uuid.uuid4())
        task_info = TaskInfo(
            task_id=task_id,
            status=CrawlStatus.PENDING,
            total_urls=len(request.urls),
            created_at=datetime.now()
        )
        
        # 保存任务信息
        await task_service.create_task(task_info)
        
        # 启动后台任务
        background_tasks.add_task(
            _process_batch_crawl,
            task_id=task_id,
            urls=[str(url) for url in request.urls],
            config=request.config,
            concurrent_limit=request.concurrent_limit
        )
        
        logger.info(f"批量爬取任务已创建: {task_id}, URLs数量: {len(request.urls)}")
        
        return TaskResponse(
            success=True,
            message="批量爬取任务已创建",
            data=task_info
        )
        
    except Exception as e:
        logger.error(f"创建批量爬取任务失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"创建任务失败: {str(e)}")

@router.post("/extract", response_model=CrawlResponse)
async def extract_structured_data(request: StructuredExtractionRequest):
    """
    结构化数据提取 - 简化版本
    """
    try:
        logger.info(f"开始结构化数据提取: {request.url}")
        start_time = time.time()
        
        # 调用爬虫服务进行结构化提取
        result = await crawler_service.extract_structured_data(
            url=str(request.url),
            extraction_prompt=request.extraction_prompt,
            config=request.config
        )
        
        execution_time = time.time() - start_time
        result.execution_time = execution_time
        
        logger.info(f"结构化数据提取完成: {request.url}, 耗时: {execution_time:.2f}s")
        
        return CrawlResponse(
            success=True,
            message="结构化数据提取成功",
            data=result
        )
        
    except Exception as e:
        logger.error(f"结构化数据提取失败: {request.url}, 错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"提取失败: {str(e)}")

@router.get("/test-connection")
async def test_crawler_connection():
    """
    测试爬虫连接
    """
    try:
        # 测试一个简单的爬取
        test_result = await crawler_service.test_connection()
        
        return {
            "success": True,
            "message": "爬虫连接正常",
            "details": test_result
        }
        
    except Exception as e:
        logger.error(f"爬虫连接测试失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"连接测试失败: {str(e)}")

async def _process_batch_crawl(
    task_id: str, 
    urls: List[str], 
    config, 
    concurrent_limit: int
):
    """
    处理批量爬取的后台任务
    """
    try:
        # 更新任务状态为运行中
        await task_service.update_task_status(task_id, CrawlStatus.RUNNING)
        
        logger.info(f"开始处理批量爬取任务: {task_id}")
        
        # 执行批量爬取
        results = await crawler_service.crawl_batch(
            urls=urls,
            config=config,
            concurrent_limit=concurrent_limit,
            progress_callback=lambda completed, total: asyncio.create_task(
                task_service.update_task_progress(task_id, completed, total)
            )
        )
        
        # 统计结果
        completed_urls = sum(1 for r in results if r.success)
        failed_urls = len(results) - completed_urls
        
        # 更新任务完成状态
        await task_service.complete_task(
            task_id=task_id,
            results=results,
            completed_urls=completed_urls,
            failed_urls=failed_urls
        )
        
        logger.info(f"批量爬取任务完成: {task_id}, 成功: {completed_urls}, 失败: {failed_urls}")
        
    except Exception as e:
        logger.error(f"批量爬取任务失败: {task_id}, 错误: {str(e)}")
        await task_service.fail_task(task_id, str(e)) 