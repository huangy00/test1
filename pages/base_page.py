# -*- coding: utf-8 -*-
"""
页面基类模块
封装 Playwright 常用操作，提供 click、fill、wait_for_selector、screenshot 等方法
失败时自动截图并附加到 Allure 报告
"""
import allure
from playwright.sync_api import Page, Locator, expect
from utils.logger import logger
from utils.config_reader import config


class BasePage:
    """页面对象基类，所有页面类继承此类"""

    def __init__(self, page: Page):
        """
        初始化基类
        :param page: Playwright Page 对象
        """
        self.page = page
        self.timeout = config.getint("DEFAULT", "timeout") * 1000  # 转换为毫秒

    def navigate(self, url: str):
        """
        导航到指定 URL
        :param url: 目标地址
        """
        logger.info(f"Navigating to {url}")
        self.page.goto(url, wait_until="domcontentloaded")

    def click(self, selector: str, timeout: int = None):
        """
        点击元素
        :param selector: CSS 选择器
        :param timeout: 超时时间（毫秒），默认使用配置值
        """
        timeout = timeout or self.timeout
        logger.info(f"Clicking: {selector}")
        try:
            self.page.locator(selector).click(timeout=timeout)
        except Exception as e:
            self._screenshot_on_failure("click_failure")
            raise e

    def fill(self, selector: str, value: str, timeout: int = None):
        """
        填写输入框
        :param selector: CSS 选择器
        :param value: 填写的值
        :param timeout: 超时时间
        """
        timeout = timeout or self.timeout
        logger.info(f"Filling: {selector} with '{value}'")
        try:
            self.page.locator(selector).fill(value, timeout=timeout)
        except Exception as e:
            self._screenshot_on_failure("fill_failure")
            raise e

    def wait_for_selector(self, selector: str, state: str = "visible", timeout: int = None):
        """
        等待元素出现
        :param selector: CSS 选择器
        :param state: 等待状态（visible / hidden / attached / detached）
        :param timeout: 超时时间
        :return: Locator 对象
        """
        timeout = timeout or self.timeout
        logger.info(f"Waiting for: {selector} (state={state})")
        locator = self.page.locator(selector)
        locator.wait_for(state=state, timeout=timeout)
        return locator

    def get_text(self, selector: str, timeout: int = None) -> str:
        """
        获取元素文本
        :param selector: CSS 选择器
        :param timeout: 超时时间
        :return: 元素文本内容
        """
        timeout = timeout or self.timeout
        locator = self.wait_for_selector(selector, timeout=timeout)
        return locator.inner_text()

    def is_visible(self, selector: str, timeout: int = 5000) -> bool:
        """
        判断元素是否可见
        :param selector: CSS 选择器
        :param timeout: 超时时间
        :return: 是否可见
        """
        try:
            self.page.locator(selector).wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    def screenshot(self, name: str):
        """
        手动截图并附加到 Allure
        :param name: 截图名称
        """
        screenshot = self.page.screenshot(full_page=True)
        allure.attach(screenshot, name=name, attachment_type=allure.attachment_type.PNG)
        logger.info(f"Screenshot saved: {name}")

    def _screenshot_on_failure(self, name: str):
        """
        失败时自动截图（内部方法）
        :param name: 截图名称
        """
        try:
            screenshot = self.page.screenshot(full_page=True)
            allure.attach(
                screenshot,
                name=f"FAILURE_{name}",
                attachment_type=allure.attachment_type.PNG,
            )
            logger.warning(f"Failure screenshot captured: {name}")
        except Exception as e:
            logger.error(f"Failed to capture screenshot: {e}")
