"""
数据模型定义
"""

from pydantic import BaseModel, HttpUrl, Field, validator
from typing import Optional, List, Dict, Any, Union
from enum import Enum
from datetime import datetime

# 爬取相关的枚举
class CrawlStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running" 
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class CacheMode(str, Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"
    BYPASS = "bypass"
    READ_ONLY = "read_only"
    WRITE_ONLY = "write_only"

class CrawlStrategy(str, Enum):
    BFS = "bfs"  # 广度优先
    DFS = "dfs"  # 深度优先
    BEST_FIRST = "best_first"  # 最佳优先

# 爬取配置模型
class CrawlConfig(BaseModel):
    """爬取配置"""
    # 基本配置
    word_count_threshold: int = Field(default=200, ge=0, description="最小词数阈值")
    cache_mode: CacheMode = Field(default=CacheMode.BYPASS, description="缓存模式")
    
    # 代理配置
    proxy_server: Optional[str] = Field(default=None, description="代理服务器地址 (如: http://127.0.0.1:7890)")
    proxy_username: Optional[str] = Field(default=None, description="代理用户名")
    proxy_password: Optional[str] = Field(default=None, description="代理密码")
    
    # 页面交互配置
    wait_until: str = Field(default="domcontentloaded", description="等待条件")
    page_timeout: int = Field(default=60000, ge=1000, le=300000, description="页面超时(ms)")
    wait_for: Optional[str] = Field(default=None, description="等待元素CSS选择器")
    delay_before_return_html: float = Field(default=0.1, ge=0, description="返回HTML前延迟(秒)")
    
    # 内容处理配置
    css_selector: Optional[str] = Field(default=None, description="CSS选择器")
    excluded_tags: List[str] = Field(default_factory=list, description="排除的HTML标签")
    excluded_selector: Optional[str] = Field(default=None, description="排除的CSS选择器")
    only_text: bool = Field(default=False, description="仅提取文本")
    
    # 媒体处理配置
    screenshot: bool = Field(default=False, description="截图")
    pdf: bool = Field(default=False, description="生成PDF")
    exclude_external_images: bool = Field(default=False, description="排除外部图片")
    
    # 深度爬取配置
    deep_crawl: bool = Field(default=False, description="启用深度爬取")
    crawl_depth: int = Field(default=1, ge=1, le=10, description="爬取深度")
    crawl_strategy: CrawlStrategy = Field(default=CrawlStrategy.BFS, description="爬取策略")
    
    # 过滤配置
    exclude_external_links: bool = Field(default=False, description="排除外部链接")
    exclude_social_media_links: bool = Field(default=True, description="排除社交媒体链接")
    exclude_domains: List[str] = Field(default_factory=list, description="排除的域名")
    
    # 高级配置
    js_code: Optional[List[str]] = Field(default=None, description="JavaScript代码")
    simulate_user: bool = Field(default=False, description="模拟用户行为")
    override_navigator: bool = Field(default=False, description="覆盖导航器属性")
    magic: bool = Field(default=False, description="智能处理")
    
    # 实验性功能
    experimental: Optional[Dict[str, Any]] = Field(default=None, description="实验性参数")

class SingleCrawlRequest(BaseModel):
    """单个URL爬取请求"""
    url: HttpUrl = Field(..., description="要爬取的URL")
    config: Optional[CrawlConfig] = Field(default_factory=CrawlConfig, description="爬取配置")
    
    @validator('url')
    def validate_url(cls, v):
        url_str = str(v)
        if not (url_str.startswith('http://') or url_str.startswith('https://')):
            raise ValueError('URL必须以http://或https://开头')
        return v

class BatchCrawlRequest(BaseModel):
    """批量URL爬取请求"""
    urls: List[HttpUrl] = Field(..., min_items=1, max_items=100, description="要爬取的URL列表")
    config: Optional[CrawlConfig] = Field(default_factory=CrawlConfig, description="爬取配置")
    concurrent_limit: int = Field(default=5, ge=1, le=20, description="并发限制")

class StructuredExtractionRequest(BaseModel):
    """结构化数据提取请求"""
    url: HttpUrl = Field(..., description="要提取的URL")
    extraction_prompt: str = Field(..., min_length=10, description="提取指令(自然语言)")
    config: Optional[CrawlConfig] = Field(default_factory=CrawlConfig, description="爬取配置")
    
    class Config:
        schema_extra = {
            "example": {
                "url": "https://example.com/products",
                "extraction_prompt": "提取所有产品的名称、价格和描述",
                "config": {}
            }
        }

# 响应模型
class CrawlResult(BaseModel):
    """爬取结果"""
    url: str = Field(..., description="原始URL")
    success: bool = Field(..., description="是否成功")
    status_code: Optional[int] = Field(default=None, description="HTTP状态码")
    title: Optional[str] = Field(default=None, description="页面标题")
    markdown: Optional[str] = Field(default=None, description="Markdown内容")
    cleaned_html: Optional[str] = Field(default=None, description="清理后的HTML")
    media: Optional[Dict[str, Any]] = Field(default=None, description="媒体内容")
    links: Optional[Dict[str, Any]] = Field(default=None, description="链接信息")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="元数据")
    screenshot: Optional[str] = Field(default=None, description="截图(base64)")
    pdf: Optional[str] = Field(default=None, description="PDF(base64)")
    execution_time: Optional[float] = Field(default=None, description="执行时间(秒)")
    error_message: Optional[str] = Field(default=None, description="错误信息")
    extracted_data: Optional[Any] = Field(default=None, description="结构化提取的数据")

class TaskInfo(BaseModel):
    """任务信息"""
    task_id: str = Field(..., description="任务ID")
    status: CrawlStatus = Field(..., description="任务状态")
    progress: float = Field(default=0.0, ge=0.0, le=100.0, description="进度百分比")
    total_urls: int = Field(default=0, ge=0, description="总URL数量")
    completed_urls: int = Field(default=0, ge=0, description="已完成URL数量")
    failed_urls: int = Field(default=0, ge=0, description="失败URL数量")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: Optional[datetime] = Field(default=None, description="更新时间")
    completed_at: Optional[datetime] = Field(default=None, description="完成时间")
    error_message: Optional[str] = Field(default=None, description="错误信息")
    results: Optional[List[CrawlResult]] = Field(default=None, description="爬取结果")

class ProjectInfo(BaseModel):
    """项目信息"""
    project_id: str = Field(..., description="项目ID")
    name: str = Field(..., min_length=1, max_length=100, description="项目名称")
    description: Optional[str] = Field(default=None, max_length=500, description="项目描述")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: Optional[datetime] = Field(default=None, description="更新时间")
    task_count: int = Field(default=0, ge=0, description="任务数量")
    total_urls: int = Field(default=0, ge=0, description="总URL数量")

# API响应模型
class APIResponse(BaseModel):
    """通用API响应"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="响应消息")
    data: Optional[Any] = Field(default=None, description="响应数据")
    timestamp: datetime = Field(default_factory=datetime.now, description="时间戳")

class TaskResponse(APIResponse):
    """任务响应"""
    data: Optional[TaskInfo] = None

class CrawlResponse(APIResponse):
    """爬取响应"""
    data: Optional[Union[CrawlResult, List[CrawlResult]]] = None

class ProjectResponse(APIResponse):
    """项目响应"""
    data: Optional[Union[ProjectInfo, List[ProjectInfo]]] = None 