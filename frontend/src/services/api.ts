// API 服务模块
import axios from 'axios'
import type {
  SingleCrawlRequest,
  BatchCrawlRequest,
  StructuredExtractionRequest,
  TaskResponse,
  CrawlResponse,
  ProjectResponse,
  APIResponse
} from '@/types/api'

// 创建 axios 实例
const api = axios.create({
  baseURL: '/api/v1',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    // 可以在这里添加认证 token 等
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    const message = error.response?.data?.detail || error.message || '请求失败'
    return Promise.reject(new Error(message))
  }
)

// 爬虫 API
export const crawlerAPI = {
  // 单个URL爬取
  crawlSingle: (data: SingleCrawlRequest): Promise<CrawlResponse> =>
    api.post('/crawler/single', data),

  // 批量URL爬取
  crawlBatch: (data: BatchCrawlRequest): Promise<TaskResponse> =>
    api.post('/crawler/batch', data),

  // 结构化数据提取
  extractStructured: (data: StructuredExtractionRequest): Promise<CrawlResponse> =>
    api.post('/crawler/extract', data),

  // 测试连接
  testConnection: (): Promise<APIResponse> =>
    api.get('/crawler/test-connection')
}

// 任务 API
export const taskAPI = {
  // 获取任务信息
  getTask: (taskId: string): Promise<TaskResponse> =>
    api.get(`/tasks/${taskId}`),

  // 获取所有任务
  getAllTasks: (): Promise<TaskResponse> =>
    api.get('/tasks/'),

  // 获取任务进度
  getTaskProgress: (taskId: string): Promise<any> =>
    api.get(`/tasks/${taskId}/progress`),

  // 取消任务
  cancelTask: (taskId: string): Promise<APIResponse> =>
    api.post(`/tasks/${taskId}/cancel`),

  // 删除任务
  deleteTask: (taskId: string): Promise<APIResponse> =>
    api.delete(`/tasks/${taskId}`),

  // 清理任务
  cleanupTasks: (maxAgeHours?: number): Promise<APIResponse> =>
    api.post('/tasks/cleanup', { max_age_hours: maxAgeHours })
}

// 项目 API
export const projectAPI = {
  // 创建项目
  createProject: (name: string, description?: string): Promise<ProjectResponse> =>
    api.post('/projects/', { name, description }),

  // 获取所有项目
  getAllProjects: (): Promise<ProjectResponse> =>
    api.get('/projects/'),

  // 获取项目信息
  getProject: (projectId: string): Promise<ProjectResponse> =>
    api.get(`/projects/${projectId}`),

  // 删除项目
  deleteProject: (projectId: string): Promise<APIResponse> =>
    api.delete(`/projects/${projectId}`)
}

export default api 