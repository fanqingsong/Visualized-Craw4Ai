"""
爬虫服务 - 封装 crawl4ai 的核心功能
"""

import asyncio
from typing import List, Optional, Callable, Any, Dict
import sys
from pathlib import Path

# 导入 crawl4ai
try:
    from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BrowserConfig
    from crawl4ai.extraction_strategy import LLMExtractionStrategy
    from crawl4ai.deep_crawling import BFSDeepCrawlStrategy, DFSDeepCrawlStrategy
except ImportError as e:
    print(f"导入 crawl4ai 失败: {e}")
    print("请确保 crawl4ai 在 Python 路径中")
    raise

from app.models.schemas import CrawlConfig, CrawlResult, CrawlStrategy
from app.utils.logging import get_logger

logger = get_logger(__name__)

class CrawlerService:
    """
    爬虫服务类
    
    封装 crawl4ai 的核心功能，提供统一的接口。
    """
    
    def __init__(self):
        self.crawler: Optional[AsyncWebCrawler] = None
        self._crawler_lock = asyncio.Lock()
        self._current_proxy_config = None
    
    async def _get_crawler(self, proxy_config: Optional[Dict[str, str]] = None) -> AsyncWebCrawler:
        """获取爬虫实例 (支持动态代理配置)"""
        # 如果代理配置发生变化，需要重新创建爬虫实例
        if self.crawler is None or proxy_config != self._current_proxy_config:
            async with self._crawler_lock:
                if self.crawler is None or proxy_config != self._current_proxy_config:
                    # 关闭旧的爬虫实例
                    if self.crawler is not None:
                        await self.crawler.close()
                        logger.info("旧爬虫实例已关闭")
                    
                    # 创建浏览器配置
                    browser_config_params = {
                        "browser_type": "chromium",
                        "headless": True,
                        "verbose": False
                    }
                    
                    # 添加代理配置
                    if proxy_config and proxy_config.get("server"):
                        if proxy_config.get("username") and proxy_config.get("password"):
                            # 使用高级代理配置
                            browser_config_params["proxy_config"] = {
                                "server": proxy_config["server"],
                                "username": proxy_config["username"],
                                "password": proxy_config["password"]
                            }
                            logger.info(f"使用认证代理: {proxy_config['server']}")
                        else:
                            # 使用简单代理配置
                            browser_config_params["proxy"] = proxy_config["server"]
                            logger.info(f"使用代理: {proxy_config['server']}")
                    
                    browser_config = BrowserConfig(**browser_config_params)
                    self.crawler = AsyncWebCrawler(config=browser_config)
                    await self.crawler.start()
                    self._current_proxy_config = proxy_config
                    logger.info("爬虫实例已初始化")
        return self.crawler
    
    def _extract_proxy_config(self, config: CrawlConfig) -> Optional[Dict[str, str]]:
        """从爬取配置中提取代理配置"""
        if not config.proxy_server:
            return None
        
        proxy_config = {"server": config.proxy_server}
        
        if config.proxy_username:
            proxy_config["username"] = config.proxy_username
        
        if config.proxy_password:
            proxy_config["password"] = config.proxy_password
            
        return proxy_config
    
    def _convert_config(self, config: CrawlConfig) -> CrawlerRunConfig:
        """将我们的配置转换为 crawl4ai 的配置"""
        crawler_config = CrawlerRunConfig()
        
        # 基本配置
        crawler_config.word_count_threshold = config.word_count_threshold
        
        # 页面交互配置
        crawler_config.wait_until = config.wait_until
        crawler_config.page_timeout = config.page_timeout
        crawler_config.wait_for = config.wait_for
        crawler_config.delay_before_return_html = config.delay_before_return_html
        
        # 内容处理配置
        crawler_config.css_selector = config.css_selector
        crawler_config.excluded_tags = config.excluded_tags
        crawler_config.excluded_selector = config.excluded_selector
        crawler_config.only_text = config.only_text
        
        # 媒体处理配置
        crawler_config.screenshot = config.screenshot
        crawler_config.pdf = config.pdf
        crawler_config.exclude_external_images = config.exclude_external_images
        
        # 过滤配置
        crawler_config.exclude_external_links = config.exclude_external_links
        crawler_config.exclude_social_media_links = config.exclude_social_media_links
        crawler_config.exclude_domains = config.exclude_domains
        
        # 高级配置
        crawler_config.js_code = config.js_code
        crawler_config.simulate_user = config.simulate_user
        crawler_config.override_navigator = config.override_navigator
        crawler_config.magic = config.magic
        
        # 深度爬取配置
        if config.deep_crawl:
            if config.crawl_strategy == CrawlStrategy.BFS:
                crawler_config.deep_crawl_strategy = BFSDeepCrawlStrategy(
                    max_depth=config.crawl_depth
                )
            elif config.crawl_strategy == CrawlStrategy.DFS:
                crawler_config.deep_crawl_strategy = DFSDeepCrawlStrategy(
                    max_depth=config.crawl_depth
                )
        
        return crawler_config
    
    def _convert_result(self, crawl4ai_result, url: str) -> CrawlResult:
        """将 crawl4ai 的结果转换为我们的格式"""
        try:
            success = crawl4ai_result.success if hasattr(crawl4ai_result, 'success') else True
            error_message = None
            
            # 如果不成功，尝试获取错误信息
            if not success:
                error_message = getattr(crawl4ai_result, 'error_message', None) or \
                               getattr(crawl4ai_result, 'error', None) or \
                               getattr(crawl4ai_result, 'message', None) or \
                               "爬取失败，未知错误"
            
            return CrawlResult(
                url=url,
                success=success,
                status_code=getattr(crawl4ai_result, 'status_code', None),
                title=getattr(crawl4ai_result, 'title', None),
                markdown=getattr(crawl4ai_result, 'markdown', None),
                cleaned_html=getattr(crawl4ai_result, 'cleaned_html', None),
                media=getattr(crawl4ai_result, 'media', None),
                links=getattr(crawl4ai_result, 'links', None),
                metadata=getattr(crawl4ai_result, 'metadata', None),
                screenshot=getattr(crawl4ai_result, 'screenshot', None),
                pdf=getattr(crawl4ai_result, 'pdf', None),
                error_message=error_message,
            )
        except Exception as e:
            logger.error(f"转换爬取结果失败: {e}")
            return CrawlResult(
                url=url,
                success=False,
                error_message=str(e)
            )
    
    async def crawl_single(self, url: str, config: CrawlConfig) -> CrawlResult:
        """
        爬取单个URL
        
        Args:
            url: 要爬取的URL
            config: 爬取配置
            
        Returns:
            CrawlResult: 爬取结果
        """
        try:
            # 提取代理配置
            proxy_config = self._extract_proxy_config(config)
            
            # 获取爬虫实例（支持代理）
            crawler = await self._get_crawler(proxy_config)
            crawler_config = self._convert_config(config)
            
            logger.info(f"开始爬取: {url}")
            if proxy_config:
                logger.info(f"使用代理: {proxy_config.get('server', 'Unknown')}")
            
            # 执行爬取
            result = await crawler.arun(url=url, config=crawler_config)
            
            # 转换结果
            crawl_result = self._convert_result(result, url)
            
            logger.info(f"爬取完成: {url}, 成功: {crawl_result.success}")
            return crawl_result
            
        except Exception as e:
            logger.error(f"爬取失败: {url}, 错误: {e}")
            return CrawlResult(
                url=url,
                success=False,
                error_message=str(e)
            )
    
    async def crawl_batch(
        self, 
        urls: List[str], 
        config: CrawlConfig,
        concurrent_limit: int = 5,
        progress_callback: Optional[Callable[[int, int], None]] = None
    ) -> List[CrawlResult]:
        """
        批量爬取URLs
        
        Args:
            urls: URL列表
            config: 爬取配置
            concurrent_limit: 并发限制
            progress_callback: 进度回调函数
            
        Returns:
            List[CrawlResult]: 爬取结果列表
        """
        try:
            # 提取代理配置
            proxy_config = self._extract_proxy_config(config)
            
            # 获取爬虫实例（支持代理）
            crawler = await self._get_crawler(proxy_config)
            crawler_config = self._convert_config(config)
            
            logger.info(f"开始批量爬取: {len(urls)} 个URLs")
            if proxy_config:
                logger.info(f"使用代理: {proxy_config.get('server', 'Unknown')}")
            
            # 使用信号量控制并发
            semaphore = asyncio.Semaphore(concurrent_limit)
            results = []
            completed = 0
            
            async def crawl_with_semaphore(url: str) -> CrawlResult:
                nonlocal completed
                async with semaphore:
                    try:
                        result = await crawler.arun(url=url, config=crawler_config)
                        crawl_result = self._convert_result(result, url)
                    except Exception as e:
                        crawl_result = CrawlResult(
                            url=url,
                            success=False,
                            error_message=str(e)
                        )
                    
                    completed += 1
                    if progress_callback:
                        progress_callback(completed, len(urls))
                    
                    logger.info(f"进度: {completed}/{len(urls)}, URL: {url}")
                    return crawl_result
            
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
        结构化数据提取
        
        Args:
            url: 要提取的URL
            extraction_prompt: 提取指令 (自然语言)
            config: 爬取配置
            
        Returns:
            CrawlResult: 包含结构化数据的爬取结果
        """
        try:
            # 提取代理配置
            proxy_config = self._extract_proxy_config(config)
            
            # 获取爬虫实例（支持代理）
            crawler = await self._get_crawler(proxy_config)
            crawler_config = self._convert_config(config)
            
            # 设置提取策略
            crawler_config.extraction_strategy = LLMExtractionStrategy(
                provider="openai",  # 需要配置 LLM 提供商
                instruction=extraction_prompt
            )
            
            logger.info(f"开始结构化数据提取: {url}")
            
            # 执行爬取和提取
            result = await crawler.arun(url=url, config=crawler_config)
            
            # 转换结果
            crawl_result = self._convert_result(result, url)
            
            # 添加提取的结构化数据
            if hasattr(result, 'extracted_content'):
                crawl_result.extracted_data = result.extracted_content
            
            logger.info(f"结构化数据提取完成: {url}")
            return crawl_result
            
        except Exception as e:
            logger.error(f"结构化数据提取失败: {url}, 错误: {e}")
            return CrawlResult(
                url=url,
                success=False,
                error_message=str(e)
            )
    
    async def test_connection(self) -> Dict[str, Any]:
        """
        测试爬虫连接
        
        Returns:
            Dict: 测试结果
        """
        try:
            crawler = await self._get_crawler()
            
            # 使用一个简单的测试页面
            test_url = "https://httpbin.org/html"
            config = CrawlerRunConfig()
            
            result = await crawler.arun(url=test_url, config=config)
            
            return {
                "status": "success",
                "test_url": test_url,
                "has_content": bool(getattr(result, 'markdown', None)),
                "content_length": len(getattr(result, 'markdown', ''))
            }
            
        except Exception as e:
            logger.error(f"连接测试失败: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def close(self):
        """关闭爬虫实例"""
        if self.crawler:
            await self.crawler.close()
            self.crawler = None
            logger.info("爬虫实例已关闭") 