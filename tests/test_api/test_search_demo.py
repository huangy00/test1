# -*- coding: utf-8 -*-
"""
搜索接口自动化测试 - 教学演示
"""
import requests
from utils.config_reader import config

site_url = config.get("ui", "base_url")


def test_search_success():
    """用例1：搜索存在的商品"""
    # GET请求用params传参
    response = requests.get(
        site_url + "index.php?route=product/search",
        params={"search": "MacBook"},
    )
    # 断言状态码
    assert response.status_code == 200
    # 断言页面包含MacBook
    assert "macbook" in response.text.lower()


def test_search_no_results():
    """用例2：搜索不存在的商品"""
    response = requests.get(
        site_url + "index.php?route=product/search",
        params={"search": "xyz不存在123"},
    )
    assert response.status_code == 200
    # 断言页面显示无结果提示
    assert "no product" in response.text.lower()


def test_search_sql_injection():
    """用例3：SQL注入测试"""
    response = requests.get(
        site_url + "index.php?route=product/search",
        params={"search": "' OR 1=1 --"},
    )
    # 断言：不报500服务器错误
    assert response.status_code != 500
