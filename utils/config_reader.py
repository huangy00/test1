# -*- coding: utf-8 -*-
"""
配置读取工具模块
负责读取 config/config.ini 配置文件，提供统一的配置访问接口
"""
import os
import configparser


# 获取项目根目录（config文件的上级目录）
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "config", "config.ini")


class ConfigReader:
    """配置文件读取器，封装 configparser 提供便捷访问方法"""

    def __init__(self, config_path: str = CONFIG_PATH):
        """
        初始化配置读取器
        :param config_path: 配置文件路径，默认为项目根目录下的 config/config.ini
        """
        self.config = configparser.ConfigParser()
        self.config.read(config_path, encoding="utf-8")

    def get(self, section: str, key: str) -> str:
        """
        获取字符串配置值
        :param section: 配置节名称（如 [ui], [db]）
        :param key: 配置键名
        :return: 配置值字符串
        """
        return self.config.get(section, key)

    def getint(self, section: str, key: str) -> int:
        """
        获取整数配置值
        :param section: 配置节名称
        :param key: 配置键名
        :return: 配置值整数
        """
        return self.config.getint(section, key)


# 全局单例，方便其他模块直接导入使用
config = ConfigReader()
