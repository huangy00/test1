# -*- coding: utf-8 -*-
"""
购物车接口自动化测试 - 教学演示
需要先登录，拿到cookie后才能操作购物车
"""
import requests
from utils.config_reader import config

site_url = config.get("ui", "base_url")


def get_login_cookie():
    """辅助函数：登录并返回cookie"""
    session = requests.Session()
    session.post(
        site_url + "index.php?route=account/login.login",
        data={
            "email": "testuser_2026@example.com",
            "password": "Test12345",
        },
    )
    return session


def test_add_to_cart():
    """用例1：正常加购"""
    # 先登录拿cookie
    session = get_login_cookie()

    # 用cookie发加购请求
    response = session.post(
        site_url + "index.php?route=checkout/cart.add",
        data={
            "product_id": "43",
            "quantity": "1",
        },
    )

    assert response.status_code == 200
    assert "success" in response.text.lower()


def test_view_cart():
    """用例2：查看购物车"""
    session = get_login_cookie()

    response = session.get(
        site_url + "index.php?route=checkout/cart",
    )

    assert response.status_code == 200
    assert "cart" in response.text.lower()
