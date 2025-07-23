#!/usr/bin/env python3
"""
Crawl4AI 数据保存工具

用于将爬取结果保存到本地文件系统，便于后续分析。
"""

import json
import os
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from urllib.parse import urlparse
import uuid

class CrawlDataSaver:
    """爬取数据保存器"""
    
    def __init__(self, base_dir: str = "data_analysis"):
        """
        初始化数据保存器
        
        Args:
            base_dir: 基础目录路径
        """
        self.base_dir = Path(base_dir)
        self.ensure_directories()
    
    def ensure_directories(self):
        """确保所有必要的目录存在"""
        dirs = [
            "raw_data/single_crawls",
            "raw_data/batch_crawls", 
            "raw_data/structured",
            "processed_data/cleaned",
            "processed_data/analyzed",
            "processed_data/aggregated",
            "exports/csv",
            "exports/json",
            "exports/reports"
        ]
        
        for dir_path in dirs:
            (self.base_dir / dir_path).mkdir(parents=True, exist_ok=True)
    
    def generate_crawl_id(self, url: str, timestamp: str) -> str:
        """
        生成爬取ID
        
        Args:
            url: 原始URL
            timestamp: 时间戳
            
        Returns:
            str: 唯一的爬取ID
        """
        # 使用URL和时间戳生成唯一ID
        content = f"{url}_{timestamp}"
        return str(uuid.uuid5(uuid.NAMESPACE_URL, content))
    
    def get_domain_from_url(self, url: str) -> str:
        """从URL提取域名"""
        try:
            parsed = urlparse(url)
            return parsed.netloc.replace(':', '_')
        except:
            return "unknown"
    
    def get_url_hash(self, url: str) -> str:
        """生成URL的短哈希"""
        return hashlib.md5(url.encode()).hexdigest()[:8]
    
    def save_single_crawl(self, crawl_result: Dict[Any, Any], config: Optional[Dict] = None) -> str:
        """
        保存单个爬取结果
        
        Args:
            crawl_result: 爬取结果
            config: 爬取配置
            
        Returns:
            str: 保存的文件路径
        """
        timestamp = datetime.now()
        timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
        
        # 生成文件名
        url = crawl_result.get('url', 'unknown')
        domain = self.get_domain_from_url(url)
        url_hash = self.get_url_hash(url)
        
        filename = f"{timestamp_str}_{domain}_{url_hash}.json"
        filepath = self.base_dir / "raw_data/single_crawls" / filename
        
        # 准备保存的数据
        save_data = {
            "crawl_id": self.generate_crawl_id(url, timestamp_str),
            "timestamp": timestamp.isoformat(),
            "config": config or {},
            "result": crawl_result,
            "analysis": self.analyze_crawl_result(crawl_result)
        }
        
        # 保存到文件
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 单个爬取结果已保存: {filepath}")
        return str(filepath)
    
    def save_batch_crawl(self, task_id: str, results: List[Dict], config: Optional[Dict] = None) -> str:
        """
        保存批量爬取结果
        
        Args:
            task_id: 任务ID
            results: 爬取结果列表
            config: 爬取配置
            
        Returns:
            str: 保存的文件路径
        """
        timestamp = datetime.now()
        timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
        
        filename = f"batch_{task_id}_{timestamp_str}.json"
        filepath = self.base_dir / "raw_data/batch_crawls" / filename
        
        # 准备保存的数据
        save_data = {
            "batch_id": task_id,
            "timestamp": timestamp.isoformat(),
            "config": config or {},
            "total_urls": len(results),
            "successful_crawls": sum(1 for r in results if r.get('success', False)),
            "failed_crawls": sum(1 for r in results if not r.get('success', False)),
            "results": results,
            "batch_analysis": self.analyze_batch_results(results)
        }
        
        # 保存到文件
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 批量爬取结果已保存: {filepath}")
        return str(filepath)
    
    def save_structured_extraction(self, url: str, prompt: str, result: Dict, config: Optional[Dict] = None) -> str:
        """
        保存结构化提取结果
        
        Args:
            url: 原始URL
            prompt: 提取提示
            result: 提取结果
            config: 爬取配置
            
        Returns:
            str: 保存的文件路径
        """
        timestamp = datetime.now()
        timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
        
        domain = self.get_domain_from_url(url)
        url_hash = self.get_url_hash(url)
        
        filename = f"structured_{timestamp_str}_{domain}_{url_hash}.json"
        filepath = self.base_dir / "raw_data/structured" / filename
        
        # 准备保存的数据
        save_data = {
            "extraction_id": self.generate_crawl_id(url, timestamp_str),
            "timestamp": timestamp.isoformat(),
            "url": url,
            "extraction_prompt": prompt,
            "config": config or {},
            "result": result,
            "analysis": self.analyze_structured_extraction(result)
        }
        
        # 保存到文件
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 结构化提取结果已保存: {filepath}")
        return str(filepath)
    
    def analyze_crawl_result(self, result: Dict) -> Dict:
        """
        分析单个爬取结果
        
        Args:
            result: 爬取结果
            
        Returns:
            Dict: 分析结果
        """
        analysis = {}
        
        # 基本信息
        analysis['success'] = result.get('success', False)
        analysis['status_code'] = result.get('status_code')
        analysis['execution_time'] = result.get('execution_time', 0)
        
        # 内容分析
        markdown = result.get('markdown', '')
        if markdown:
            analysis['word_count'] = len(markdown.split())
            analysis['char_count'] = len(markdown)
            analysis['paragraph_count'] = markdown.count('\n\n')
            analysis['has_content'] = len(markdown.strip()) > 0
        else:
            analysis['word_count'] = 0
            analysis['char_count'] = 0
            analysis['paragraph_count'] = 0
            analysis['has_content'] = False
        
        # 媒体内容分析
        media = result.get('media', {})
        if media:
            analysis['image_count'] = len(media.get('images', []))
            analysis['video_count'] = len(media.get('videos', []))
            analysis['audio_count'] = len(media.get('audios', []))
        else:
            analysis['image_count'] = 0
            analysis['video_count'] = 0
            analysis['audio_count'] = 0
        
        # 链接分析
        links = result.get('links', {})
        if links:
            analysis['internal_links'] = len(links.get('internal', []))
            analysis['external_links'] = len(links.get('external', []))
        else:
            analysis['internal_links'] = 0
            analysis['external_links'] = 0
        
        # 特殊功能
        analysis['has_screenshot'] = bool(result.get('screenshot'))
        analysis['has_pdf'] = bool(result.get('pdf'))
        analysis['has_structured_data'] = bool(result.get('extracted_data'))
        
        return analysis
    
    def analyze_batch_results(self, results: List[Dict]) -> Dict:
        """
        分析批量爬取结果
        
        Args:
            results: 结果列表
            
        Returns:
            Dict: 分析结果
        """
        if not results:
            return {}
        
        analysis = {
            'total_count': len(results),
            'success_count': 0,
            'failure_count': 0,
            'avg_execution_time': 0,
            'total_words': 0,
            'total_images': 0,
            'domains': set(),
            'status_codes': {},
        }
        
        execution_times = []
        
        for result in results:
            # 成功率统计
            if result.get('success', False):
                analysis['success_count'] += 1
            else:
                analysis['failure_count'] += 1
            
            # 执行时间统计
            exec_time = result.get('execution_time', 0)
            if exec_time > 0:
                execution_times.append(exec_time)
            
            # 内容统计
            markdown = result.get('markdown', '')
            if markdown:
                analysis['total_words'] += len(markdown.split())
            
            # 媒体统计
            media = result.get('media', {})
            if media:
                analysis['total_images'] += len(media.get('images', []))
            
            # 域名统计
            url = result.get('url', '')
            if url:
                domain = self.get_domain_from_url(url)
                analysis['domains'].add(domain)
            
            # 状态码统计
            status_code = result.get('status_code')
            if status_code:
                analysis['status_codes'][status_code] = analysis['status_codes'].get(status_code, 0) + 1
        
        # 计算平均值
        if execution_times:
            analysis['avg_execution_time'] = sum(execution_times) / len(execution_times)
        
        # 转换集合为列表（JSON序列化）
        analysis['domains'] = list(analysis['domains'])
        analysis['success_rate'] = analysis['success_count'] / analysis['total_count'] if analysis['total_count'] > 0 else 0
        
        return analysis
    
    def analyze_structured_extraction(self, result: Dict) -> Dict:
        """
        分析结构化提取结果
        
        Args:
            result: 提取结果
            
        Returns:
            Dict: 分析结果
        """
        analysis = {
            'success': result.get('success', False),
            'has_extracted_data': bool(result.get('extracted_data'))
        }
        
        extracted_data = result.get('extracted_data')
        if extracted_data:
            if isinstance(extracted_data, list):
                analysis['extracted_items_count'] = len(extracted_data)
                analysis['extraction_type'] = 'list'
            elif isinstance(extracted_data, dict):
                analysis['extracted_fields_count'] = len(extracted_data.keys())
                analysis['extraction_type'] = 'object'
            else:
                analysis['extraction_type'] = 'other'
        
        return analysis

def main():
    """主函数 - 用于测试"""
    saver = CrawlDataSaver()
    
    # 测试数据
    test_result = {
        "url": "https://httpbin.org/html",
        "success": True,
        "status_code": 200,
        "title": "Test Page",
        "markdown": "# Test Content\n\nThis is a test page with some content.",
        "execution_time": 1.23,
        "media": {"images": [], "videos": [], "audios": []},
        "links": {"internal": [], "external": []}
    }
    
    test_config = {
        "cache_mode": "enabled",
        "only_text": True,
        "magic": True
    }
    
    # 保存测试数据
    filepath = saver.save_single_crawl(test_result, test_config)
    print(f"测试数据已保存到: {filepath}")

if __name__ == "__main__":
    main() 