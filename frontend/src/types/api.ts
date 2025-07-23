// API 相关的类型定义

export enum CrawlStatus {
  PENDING = 'pending',
  RUNNING = 'running',
  COMPLETED = 'completed',
  FAILED = 'failed',
  CANCELLED = 'cancelled'
}

export enum CacheMode {
  ENABLED = 'enabled',
  DISABLED = 'disabled',
  BYPASS = 'bypass',
  READ_ONLY = 'read_only',
  WRITE_ONLY = 'write_only'
}

export enum CrawlStrategy {
  BFS = 'bfs',
  DFS = 'dfs',
  BEST_FIRST = 'best_first'
}

// 爬取配置
export interface CrawlConfig {
  // 基本配置
  word_count_threshold?: number
  cache_mode?: CacheMode
  
  // 页面交互配置
  wait_until?: string
  page_timeout?: number
  wait_for?: string
  delay_before_return_html?: number
  
  // 内容处理配置
  css_selector?: string
  excluded_tags?: string[]
  excluded_selector?: string
  only_text?: boolean
  
  // 媒体处理配置
  screenshot?: boolean
  pdf?: boolean
  exclude_external_images?: boolean
  
  // 深度爬取配置
  deep_crawl?: boolean
  crawl_depth?: number
  crawl_strategy?: CrawlStrategy
  
  // 过滤配置
  exclude_external_links?: boolean
  exclude_social_media_links?: boolean
  exclude_domains?: string[]
  
  // 高级配置
  js_code?: string[]
  simulate_user?: boolean
  override_navigator?: boolean
  magic?: boolean
  
  // 实验性功能
  experimental?: Record<string, any>
}

// 请求类型
export interface SingleCrawlRequest {
  url: string
  config?: CrawlConfig
}

export interface BatchCrawlRequest {
  urls: string[]
  config?: CrawlConfig
  concurrent_limit?: number
}

export interface StructuredExtractionRequest {
  url: string
  extraction_prompt: string
  config?: CrawlConfig
}

// 响应类型
export interface CrawlResult {
  url: string
  success: boolean
  status_code?: number
  title?: string
  markdown?: string
  cleaned_html?: string
  media?: Record<string, any>
  links?: Record<string, any>
  metadata?: Record<string, any>
  screenshot?: string
  pdf?: string
  execution_time?: number
  error_message?: string
  extracted_data?: any
}

export interface TaskInfo {
  task_id: string
  status: CrawlStatus
  progress: number
  total_urls: number
  completed_urls: number
  failed_urls: number
  created_at: string
  updated_at?: string
  completed_at?: string
  error_message?: string
  results?: CrawlResult[]
}

export interface ProjectInfo {
  project_id: string
  name: string
  description?: string
  created_at: string
  updated_at?: string
  task_count: number
  total_urls: number
}

// API 响应包装
export interface APIResponse<T = any> {
  success: boolean
  message: string
  data?: T
  timestamp: string
}

export type TaskResponse = APIResponse<TaskInfo | TaskInfo[]>
export type CrawlResponse = APIResponse<CrawlResult | CrawlResult[]>
export type ProjectResponse = APIResponse<ProjectInfo | ProjectInfo[]> 