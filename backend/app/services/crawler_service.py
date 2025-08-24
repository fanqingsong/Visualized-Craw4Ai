"""
爬虫服务 - 基于成功的crawl4ai-fastapi项目实现
"""

import asyncio
import gc
import logging
from asyncio import TimeoutError, wait_for
from typing import List, Optional, Dict, Any
from urllib.parse import urlparse

from crawl4ai import AsyncWebCrawler
from app.models.schemas import CrawlConfig, CrawlResult
from app.utils.logging import get_logger

logger = get_logger(__name__)

class CrawlerService:
    """
    爬虫服务类 - 简化版本，基于成功的crawl4ai-fastapi项目
    """
    
    def __init__(self):
        self.user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
        self.crawler_timeout = 30
        self.request_timeout = 60
    
    async def _validate_url(self, url: str) -> bool:
        """验证URL格式"""
        try:
            parsed = urlparse(url)
            return bool(parsed.netloc and parsed.scheme in ["http", "https"])
        except Exception:
            return False
    
    async def crawl_single(self, url: str, config: CrawlConfig) -> CrawlResult:
        """
        爬取单个URL - 基于成功的实现
        """
        try:
            # 验证URL
            if not await self._validate_url(url):
                return CrawlResult(
                    url=url,
                    success=False,
                    error_message="Invalid URL format"
                )
            
            logger.info(f"开始爬取: {url}")
            
            # 使用与成功项目相同的爬取逻辑
            async with AsyncWebCrawler(
                verbose=True,
                user_agent=self.user_agent,
                timeout=self.crawler_timeout,
            ) as crawler:
                result = await wait_for(
                    crawler.arun(
                        url=url,
                        screenshot=False,
                        excluded_tags=["form"],
                        exclude_external_links=False,
                        exclude_social_media_links=True,
                        exclude_external_images=False,
                        remove_overlay_elements=True,
                        html2text={
                            "escape_dot": False,
                        },
                    ),
                    timeout=self.request_timeout,
                )
            
            # 垃圾回收
            gc.collect()
            
            # 检查结果
            if result.markdown is None:
                return CrawlResult(
                    url=url,
                    success=False,
                    error_message="Content crawling failed - no markdown content"
                )
            
            # 构建成功结果
            crawl_result = CrawlResult(
                url=url,
                success=True,
                status_code=getattr(result, 'status_code', 200),
                title=getattr(result, 'title', None),
                markdown=result.markdown,
                cleaned_html=getattr(result, 'html', None),
                metadata={
                    "method": "crawl4ai_simple",
                    "user_agent": self.user_agent,
                    "content_length": len(result.markdown) if result.markdown else 0
                }
            )
            
            logger.info(f"爬取成功: {url}, 内容长度: {len(result.markdown) if result.markdown else 0}")
            return crawl_result
            
        except TimeoutError:
            logger.error(f"爬取超时: {url}")
            return CrawlResult(
                url=url,
                success=False,
                error_message="Request timed out"
            )
        except Exception as e:
            logger.error(f"爬取失败: {url}, 错误: {str(e)}")
            return CrawlResult(
                url=url,
                success=False,
                error_message=f"Crawling failed: {str(e)}"
            )
    
    async def crawl_batch(
        self, 
        urls: List[str], 
        config: CrawlConfig,
        concurrent_limit: int = 3,
        progress_callback: Optional[callable] = None
    ) -> List[CrawlResult]:
        """
        批量爬取URLs - 使用信号量控制并发
        """
        try:
            logger.info(f"开始批量爬取: {len(urls)} 个URLs")
            
            # 使用信号量控制并发
            semaphore = asyncio.Semaphore(concurrent_limit)
            results = []
            completed = 0
            
            async def crawl_with_semaphore(url: str) -> CrawlResult:
                nonlocal completed
                async with semaphore:
                    try:
                        result = await self.crawl_single(url, config)
                    except Exception as e:
                        result = CrawlResult(
                            url=url,
                            success=False,
                            error_message=str(e)
                        )
                    
                    completed += 1
                    if progress_callback:
                        progress_callback(completed, len(urls))
                    
                    logger.info(f"进度: {completed}/{len(urls)}, URL: {url}")
                    return result
            
            # 并发执行所有爬取任务
            tasks = [crawl_with_semaphore(url) for url in urls]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # 处理异常结果
            final_results = []
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    final_results.append(CrawlResult(
                        url=urls[i],
                        success=False,
                        error_message=str(result)
                    ))
                else:
                    final_results.append(result)
            
            success_count = sum(1 for r in final_results if r.success)
            logger.info(f"批量爬取完成: 成功 {success_count}/{len(urls)}")
            
            return final_results
            
        except Exception as e:
            logger.error(f"批量爬取失败: {e}")
            # 返回所有失败的结果
            return [
                CrawlResult(url=url, success=False, error_message=str(e))
                for url in urls
            ]
    
    async def extract_structured_data(
        self, 
        url: str, 
        extraction_prompt: str, 
        config: CrawlConfig
    ) -> CrawlResult:
        """
        结构化数据提取 - 简化版本
        """
        try:
            # 先爬取内容
            crawl_result = await self.crawl_single(url, config)
            
            if not crawl_result.success:
                return crawl_result
            
            # 这里可以添加LLM处理逻辑来提取结构化数据
            # 暂时返回爬取结果
            crawl_result.extracted_data = {
                "prompt": extraction_prompt,
                "note": "Structured extraction not implemented yet"
            }
            
            return crawl_result
            
        except Exception as e:
            logger.error(f"结构化数据提取失败: {url}, 错误: {e}")
            return CrawlResult(
                url=url,
                success=False,
                error_message=f"Extraction failed: {str(e)}"
            )
    
    async def test_connection(self) -> Dict[str, Any]:
        """
        测试爬虫连接
        """
        try:
            test_url = "https://httpbin.org/html"
            result = await self.crawl_single(test_url, CrawlConfig())
            
            return {
                "status": "success" if result.success else "error",
                "test_url": test_url,
                "has_content": bool(result.markdown),
                "content_length": len(result.markdown) if result.markdown else 0,
                "error": result.error_message if not result.success else None
            }
            
        except Exception as e:
            logger.error(f"连接测试失败: {e}")
            return {
                "status": "error",
                "error": str(e)
            } 