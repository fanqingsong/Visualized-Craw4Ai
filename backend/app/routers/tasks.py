"""
任务管理相关的 API 路由
"""

from fastapi import APIRouter, HTTPException
from typing import List, Optional

from app.models.schemas import TaskResponse, TaskInfo, APIResponse
from app.services.task_service import TaskService
from app.utils.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)

# 初始化服务
task_service = TaskService()

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str):
    """
    获取任务信息
    
    Args:
        task_id: 任务ID
        
    Returns:
        TaskResponse: 任务信息响应
    """
    try:
        task = await task_service.get_task(task_id)
        
        if not task:
            raise HTTPException(status_code=404, detail="任务不存在")
        
        return TaskResponse(
            success=True,
            message="获取任务信息成功",
            data=task
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取任务信息失败: {task_id}, 错误: {e}")
        raise HTTPException(status_code=500, detail=f"获取任务信息失败: {str(e)}")

@router.get("/", response_model=APIResponse)
async def get_all_tasks():
    """获取所有任务"""
    try:
        tasks = await task_service.get_all_tasks()
        return APIResponse(
            success=True,
            message="获取任务列表成功",
            data=tasks
        )
    except Exception as e:
        logger.error(f"获取任务列表失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取任务列表失败: {e}")

@router.post("/{task_id}/cancel", response_model=APIResponse)
async def cancel_task(task_id: str):
    """
    取消任务
    
    Args:
        task_id: 任务ID
        
    Returns:
        APIResponse: 取消结果响应
    """
    try:
        success = await task_service.cancel_task(task_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="任务不存在或无法取消")
        
        return APIResponse(
            success=True,
            message="任务已取消"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"取消任务失败: {task_id}, 错误: {e}")
        raise HTTPException(status_code=500, detail=f"取消任务失败: {str(e)}")

@router.delete("/{task_id}", response_model=APIResponse)
async def delete_task(task_id: str):
    """
    删除任务
    
    Args:
        task_id: 任务ID
        
    Returns:
        APIResponse: 删除结果响应
    """
    try:
        success = await task_service.delete_task(task_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="任务不存在")
        
        return APIResponse(
            success=True,
            message="任务已删除"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"删除任务失败: {task_id}, 错误: {e}")
        raise HTTPException(status_code=500, detail=f"删除任务失败: {str(e)}")

@router.post("/cleanup", response_model=APIResponse)
async def cleanup_tasks(max_age_hours: Optional[int] = 24):
    """
    清理已完成的旧任务
    
    Args:
        max_age_hours: 最大保留时间(小时)，默认24小时
        
    Returns:
        APIResponse: 清理结果响应
    """
    try:
        cleaned_count = await task_service.cleanup_completed_tasks(max_age_hours)
        
        return APIResponse(
            success=True,
            message=f"已清理 {cleaned_count} 个旧任务"
        )
        
    except Exception as e:
        logger.error(f"清理任务失败: {e}")
        raise HTTPException(status_code=500, detail=f"清理任务失败: {str(e)}")

@router.get("/{task_id}/progress")
async def get_task_progress(task_id: str):
    """
    获取任务进度 (轻量级接口，仅返回进度信息)
    
    Args:
        task_id: 任务ID
        
    Returns:
        Dict: 进度信息
    """
    try:
        task = await task_service.get_task(task_id)
        
        if not task:
            raise HTTPException(status_code=404, detail="任务不存在")
        
        return {
            "task_id": task_id,
            "status": task.status,
            "progress": task.progress,
            "completed_urls": task.completed_urls,
            "total_urls": task.total_urls,
            "failed_urls": task.failed_urls
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取任务进度失败: {task_id}, 错误: {e}")
        raise HTTPException(status_code=500, detail=f"获取任务进度失败: {str(e)}") 