"""
项目管理相关的 API 路由
"""

from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
import uuid

from app.models.schemas import ProjectResponse, ProjectInfo, APIResponse
from app.utils.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)

# 简化的内存存储 (生产环境应使用数据库)
projects_store = {}

@router.post("/", response_model=ProjectResponse)
async def create_project(name: str, description: str = None):
    """
    创建新项目
    
    Args:
        name: 项目名称
        description: 项目描述
        
    Returns:
        ProjectResponse: 创建的项目信息
    """
    try:
        project_id = str(uuid.uuid4())
        project = ProjectInfo(
            project_id=project_id,
            name=name,
            description=description,
            created_at=datetime.now()
        )
        
        projects_store[project_id] = project
        
        logger.info(f"项目已创建: {project_id} - {name}")
        
        return ProjectResponse(
            success=True,
            message="项目创建成功",
            data=project
        )
        
    except Exception as e:
        logger.error(f"创建项目失败: {e}")
        raise HTTPException(status_code=500, detail=f"创建项目失败: {str(e)}")

@router.get("/", response_model=ProjectResponse)
async def get_all_projects():
    """
    获取所有项目
    
    Returns:
        ProjectResponse: 项目列表
    """
    try:
        projects = list(projects_store.values())
        
        return ProjectResponse(
            success=True,
            message=f"获取项目列表成功，共 {len(projects)} 个项目",
            data=projects
        )
        
    except Exception as e:
        logger.error(f"获取项目列表失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取项目列表失败: {str(e)}")

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: str):
    """
    获取项目信息
    
    Args:
        project_id: 项目ID
        
    Returns:
        ProjectResponse: 项目信息
    """
    try:
        project = projects_store.get(project_id)
        
        if not project:
            raise HTTPException(status_code=404, detail="项目不存在")
        
        return ProjectResponse(
            success=True,
            message="获取项目信息成功",
            data=project
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取项目信息失败: {project_id}, 错误: {e}")
        raise HTTPException(status_code=500, detail=f"获取项目信息失败: {str(e)}")

@router.delete("/{project_id}", response_model=APIResponse)
async def delete_project(project_id: str):
    """
    删除项目
    
    Args:
        project_id: 项目ID
        
    Returns:
        APIResponse: 删除结果
    """
    try:
        if project_id not in projects_store:
            raise HTTPException(status_code=404, detail="项目不存在")
        
        del projects_store[project_id]
        
        logger.info(f"项目已删除: {project_id}")
        
        return APIResponse(
            success=True,
            message="项目删除成功"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"删除项目失败: {project_id}, 错误: {e}")
        raise HTTPException(status_code=500, detail=f"删除项目失败: {str(e)}") 