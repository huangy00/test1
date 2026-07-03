# -*- coding: utf-8 -*-
"""
登录接口自动化测试 - 教学演示
"""
import requests
from utils.config_reader import config

# 从配置文件读取网站地址
site_url = config.get("ui", "base_url")


def test_login_success():
    """用例1：正确账号密码登录"""
    # 准备数据
    data = {
        "email": "testuser_2026@example.com",
        "password": "Test@12345",
    }
    # 发请求
    response = requests.post(
        site_url + "index.php?route=account/login.login",
        data=data,
    )
    # 断言
    assert response.status_code == 200


def test_login_wrong_password():
    """用例2：密码错误"""
    data = {
        "email": "testuser_2026@example.com",
        "password": "wrong123",
    }
    response = requests.post(
        site_url + "index.php?route=account/login.login",
        data=data,
    )
    assert response.status_code == 200
    assert "login" in response.text.lower()


def test_login_empty_email():
    """用例3：邮箱为空"""
    data = {
        "email": "",
        "password": "Test12345",
    }
    response = requests.post(
        site_url + "index.php?route=account/login.login",
        data=data,
    )
    assert response.status_code == 200
