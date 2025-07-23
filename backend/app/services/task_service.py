"""
任务管理服务
"""

from typing import Dict, List, Optional
from datetime import datetime
import asyncio

from app.models.schemas import TaskInfo, CrawlStatus, CrawlResult
from app.utils.logging import get_logger

logger = get_logger(__name__)

class TaskService:
    """
    任务管理服务
    
    管理爬取任务的生命周期，包括创建、更新状态、进度追踪等。
    目前使用内存存储，生产环境建议使用数据库。
    """
    
    def __init__(self):
        # 内存存储任务信息 (生产环境应使用数据库)
        self.tasks: Dict[str, TaskInfo] = {}
        self._lock = asyncio.Lock()
    
    async def create_task(self, task_info: TaskInfo) -> TaskInfo:
        """
        创建新任务
        
        Args:
            task_info: 任务信息
            
        Returns:
            TaskInfo: 创建的任务信息
        """
        async with self._lock:
            self.tasks[task_info.task_id] = task_info
            logger.info(f"任务已创建: {task_info.task_id}")
            return task_info
    
    async def get_task(self, task_id: str) -> Optional[TaskInfo]:
        """
        获取任务信息
        
        Args:
            task_id: 任务ID
            
        Returns:
            Optional[TaskInfo]: 任务信息，如果不存在则返回None
        """
        return self.tasks.get(task_id)
    
    async def get_all_tasks(self) -> List[TaskInfo]:
        """
        获取所有任务信息
        
        Returns:
            List[TaskInfo]: 任务信息列表
        """
        return list(self.tasks.values())
    
    async def update_task_status(self, task_id: str, status: CrawlStatus) -> bool:
        """
        更新任务状态
        
        Args:
            task_id: 任务ID
            status: 新状态
            
        Returns:
            bool: 是否更新成功
        """
        async with self._lock:
            if task_id in self.tasks:
                self.tasks[task_id].status = status
                self.tasks[task_id].updated_at = datetime.now()
                
                if status == CrawlStatus.COMPLETED or status == CrawlStatus.FAILED:
                    self.tasks[task_id].completed_at = datetime.now()
                
                logger.info(f"任务状态已更新: {task_id} -> {status}")
                return True
            return False
    
    async def update_task_progress(self, task_id: str, completed: int, total: int) -> bool:
        """
        更新任务进度
        
        Args:
            task_id: 任务ID
            completed: 已完成数量
            total: 总数量
            
        Returns:
            bool: 是否更新成功
        """
        async with self._lock:
            if task_id in self.tasks:
                self.tasks[task_id].completed_urls = completed
                self.tasks[task_id].progress = (completed / total * 100) if total > 0 else 0
                self.tasks[task_id].updated_at = datetime.now()
                
                logger.debug(f"任务进度已更新: {task_id} -> {completed}/{total}")
                return True
            return False
    
    async def complete_task(
        self, 
        task_id: str, 
        results: List[CrawlResult],
        completed_urls: int,
        failed_urls: int
    ) -> bool:
        """
        完成任务
        
        Args:
            task_id: 任务ID
            results: 爬取结果列表
            completed_urls: 成功完成的URL数量
            failed_urls: 失败的URL数量
            
        Returns:
            bool: 是否更新成功
        """
        async with self._lock:
            if task_id in self.tasks:
                task = self.tasks[task_id]
                task.status = CrawlStatus.COMPLETED
                task.progress = 100.0
                task.completed_urls = completed_urls
                task.failed_urls = failed_urls
                task.results = results
                task.updated_at = datetime.now()
                task.completed_at = datetime.now()
                
                logger.info(f"任务已完成: {task_id}, 成功: {completed_urls}, 失败: {failed_urls}")
                return True
            return False
    
    async def fail_task(self, task_id: str, error_message: str) -> bool:
        """
        标记任务失败
        
        Args:
            task_id: 任务ID
            error_message: 错误信息
            
        Returns:
            bool: 是否更新成功
        """
        async with self._lock:
            if task_id in self.tasks:
                task = self.tasks[task_id]
                task.status = CrawlStatus.FAILED
                task.error_message = error_message
                task.updated_at = datetime.now()
                task.completed_at = datetime.now()
                
                logger.error(f"任务失败: {task_id}, 错误: {error_message}")
                return True
            return False
    
    async def cancel_task(self, task_id: str) -> bool:
        """
        取消任务
        
        Args:
            task_id: 任务ID
            
        Returns:
            bool: 是否取消成功
        """
        async with self._lock:
            if task_id in self.tasks:
                task = self.tasks[task_id]
                if task.status in [CrawlStatus.PENDING, CrawlStatus.RUNNING]:
                    task.status = CrawlStatus.CANCELLED
                    task.updated_at = datetime.now()
                    task.completed_at = datetime.now()
                    
                    logger.info(f"任务已取消: {task_id}")
                    return True
            return False
    
    async def delete_task(self, task_id: str) -> bool:
        """
        删除任务
        
        Args:
            task_id: 任务ID
            
        Returns:
            bool: 是否删除成功
        """
        async with self._lock:
            if task_id in self.tasks:
                del self.tasks[task_id]
                logger.info(f"任务已删除: {task_id}")
                return True
            return False
    
    async def cleanup_completed_tasks(self, max_age_hours: int = 24) -> int:
        """
        清理已完成的旧任务
        
        Args:
            max_age_hours: 最大保留时间(小时)
            
        Returns:
            int: 清理的任务数量
        """
        async with self._lock:
            current_time = datetime.now()
            tasks_to_delete = []
            
            for task_id, task in self.tasks.items():
                if (task.status in [CrawlStatus.COMPLETED, CrawlStatus.FAILED, CrawlStatus.CANCELLED] 
                    and task.completed_at):
                    age_hours = (current_time - task.completed_at).total_seconds() / 3600
                    if age_hours > max_age_hours:
                        tasks_to_delete.append(task_id)
            
            for task_id in tasks_to_delete:
                del self.tasks[task_id]
            
            if tasks_to_delete:
                logger.info(f"已清理 {len(tasks_to_delete)} 个旧任务")
            
            return len(tasks_to_delete) 