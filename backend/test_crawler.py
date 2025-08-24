#!/usr/bin/env python3
"""
简单的爬虫测试脚本
"""

import asyncio
import sys
import os

# 添加app路径到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.services.crawler_service import CrawlerService
from app.models.schemas import CrawlConfig

async def test_crawler():
    """测试爬虫功能"""
    print("开始测试爬虫功能...")
    
    # 创建爬虫服务
    crawler_service = CrawlerService()
    
    # 测试连接
    print("\n1. 测试爬虫连接...")
    try:
        connection_result = await crawler_service.test_connection()
        print(f"连接测试结果: {connection_result}")
    except Exception as e:
        print(f"连接测试失败: {e}")
        return
    
    # 测试简单爬取
    print("\n2. 测试简单爬取...")
    test_url = "https://httpbin.org/html"
    try:
        result = await crawler_service.crawl_single(test_url, CrawlConfig())
        print(f"爬取结果: success={result.success}")
        if result.success:
            print(f"内容长度: {len(result.markdown) if result.markdown else 0}")
            print(f"标题: {result.title}")
        else:
            print(f"错误信息: {result.error_message}")
    except Exception as e:
        print(f"爬取测试失败: {e}")
    
    # 测试真实网站爬取
    print("\n3. 测试真实网站爬取...")
    real_url = "https://www.example.com"
    try:
        result = await crawler_service.crawl_single(real_url, CrawlConfig())
        print(f"爬取结果: success={result.success}")
        if result.success:
            print(f"内容长度: {len(result.markdown) if result.markdown else 0}")
            print(f"标题: {result.title}")
        else:
            print(f"错误信息: {result.error_message}")
    except Exception as e:
        print(f"真实网站爬取测试失败: {e}")
    
    print("\n测试完成!")

if __name__ == "__main__":
    asyncio.run(test_crawler())
