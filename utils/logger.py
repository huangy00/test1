# -*- coding: utf-8 -*-
"""
日志工具模块
封装 logging 模块，同时输出到控制台和日志文件
格式：时间 - 名称 - 级别 - 消息
"""
import os
import logging
from utils.config_reader import config


# 获取项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def setup_logger(name: str = "auto_test") -> logging.Logger:
    """
    创建并配置日志记录器
    :param name: 日志记录器名称
    :return: 配置好的 Logger 实例
    """
    logger = logging.getLogger(name)

    # 避免重复添加 handler
    if logger.handlers:
        return logger

    # 从配置文件读取日志级别和文件路径
    level = config.get("log", "level")
    log_file = config.get("log", "file")

    # 设置日志级别
    logger.setLevel(getattr(logging, level))

    # 日志格式：时间 - 名称 - 级别 - 消息
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 控制台输出处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 文件输出处理器（自动创建日志目录）
    log_path = os.path.join(BASE_DIR, log_file)
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


# 全局日志实例
logger = setup_logger()
