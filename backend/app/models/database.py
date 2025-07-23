"""
数据库初始化模块
"""

import os
from pathlib import Path
from app.utils.logging import get_logger

logger = get_logger(__name__)

async def init_db():
    """
    初始化数据库
    
    目前使用简化的文件系统存储，生产环境建议使用 SQLAlchemy + PostgreSQL/MySQL
    """
    try:
        # 创建数据存储目录
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        # 创建子目录
        (data_dir / "tasks").mkdir(exist_ok=True)
        (data_dir / "projects").mkdir(exist_ok=True)
        (data_dir / "results").mkdir(exist_ok=True)
        
        logger.info("数据存储目录已初始化")
        
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
        raise 