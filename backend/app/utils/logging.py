"""
日志工具模块
"""

import logging
import sys
from pathlib import Path
from typing import Optional

def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """
    设置应用日志
    
    Args:
        log_level: 日志级别
        
    Returns:
        logging.Logger: 配置好的日志器
    """
    # 创建日志目录
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # 配置日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 创建根日志器
    logger = logging.getLogger("crawl4ai_visual")
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 文件处理器
    file_handler = logging.FileHandler(log_dir / "app.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger

def get_logger(name: str) -> logging.Logger:
    """
    获取指定名称的日志器
    
    Args:
        name: 日志器名称
        
    Returns:
        logging.Logger: 日志器实例
    """
    return logging.getLogger(f"crawl4ai_visual.{name}") 