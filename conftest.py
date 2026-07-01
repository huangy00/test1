# -*- coding: utf-8 -*-
"""
Pytest 全局配置和 Fixture
提供 db fixture（数据库连接）、page fixture（Playwright 页面）、test_data fixture（测试数据）
"""
import json
import os
import allure
import pytest
from playwright.sync_api import sync_playwright
from utils.config_reader import config
from utils.db_helper import db_helper
from utils.logger import logger


# 测试数据目录
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


@pytest.fixture(scope="function")
def db():
    """
    数据库连接 Fixture
    function 级别，每个测试函数独立连接
    yield 后自动关闭连接
    """
    logger.info("Database connection fixture created")
    yield db_helper
    logger.info("Database connection fixture teardown")


@pytest.fixture(scope="function")
def page():
    """
    Playwright 页面 Fixture
    function 级别，每个测试函数独立浏览器上下文
    自动截图失败场景并附加到 Allure
    """
    with sync_playwright() as p:
        # 启动浏览器（headless=False 方便调试，CI 环境改为 True）
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            ignore_https_errors=True,
        )
        page_obj = context.new_page()

        # 导航到 OpenCart 首页
        base_url = config.get("ui", "base_url")
        page_obj.goto(base_url, wait_until="domcontentloaded")
        logger.info(f"Page opened, navigating to {base_url}")

        yield page_obj

        # 测试结束时截图（无论成功失败）
        try:
            screenshot = page_obj.screenshot(full_page=True)
            allure.attach(
                screenshot,
                name="final_screenshot",
                attachment_type=allure.attachment_type.PNG,
            )
        except Exception as e:
            logger.warning(f"Failed to capture final screenshot: {e}")

        context.close()
        browser.close()
        logger.info("Browser closed")


@pytest.fixture(scope="function")
def test_data():
    """
    测试数据 Fixture
    从 data/users.json 读取测试数据
    """
    users_path = os.path.join(DATA_DIR, "users.json")
    with open(users_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    logger.info(f"Test data loaded: {list(data.keys())}")
    return data
