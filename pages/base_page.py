# -*- coding: utf-8 -*-
"""
页面基类
作用：封装所有页面都能用的基础操作（点击、填表、截图等）
所有页面对象都继承这个类，这样就不用重复写代码
"""
import allure
from playwright.sync_api import Page, Locator, expect
from utils.logger import logger
from utils.config_reader import config


class BasePage:
    """页面基类，所有页面对象的爸爸"""

    def __init__(self, page: Page):
        """
        初始化
        page参数：Playwright的页面对象，由conftest.py自动传入
        有了page，才能操作浏览器
        """
        self.page = page
        # 从配置文件读取超时时间，转换成毫秒
        self.timeout = config.getint("DEFAULT", "timeout") * 1000

    def navigate(self, url: str):
        """
        打开网页
        用法：self.navigate("http://localhost/opencart/login")
        人话：在浏览器地址栏输入网址，按回车
        """
        logger.info(f"Navigating to {url}")
        try:
            # goto = 打开网页，wait_until="domcontentloaded" = 等页面内容加载完
            self.page.goto(url, wait_until="domcontentloaded", timeout=15000)
        except Exception:
            # 如果上面的方式失败，换一种方式重试
            logger.warning(f"Navigation failed, retrying")
            self.page.goto(url, wait_until="commit", timeout=15000)

    def click(self, selector: str, timeout: int = None):
        """
        点击元素
        用法：self.click("#login-btn")
        参数selector：CSS选择器，用来定位网页上的元素
        人话：找到这个按钮，用鼠标点一下
        """
        timeout = timeout or self.timeout
        logger.info(f"Clicking: {selector}")
        try:
            # locator = 定位器，找到页面上的元素
            # click = 点击
            self.page.locator(selector).click(timeout=timeout)
        except Exception as e:
            # 如果点击失败，自动截图（方便排查问题）
            self._screenshot_on_failure("click_failure")
            raise e

    def fill(self, selector: str, value: str, timeout: int = None):
        """
        填写输入框
        用法：self.fill("#input-email", "test@test.com")
        参数selector：CSS选择器，定位输入框
        参数value：要填写的内容
        人话：找到这个输入框，往里面打字
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
        用法：self.wait_for_selector("#loading", state="hidden")
        参数state：
            "visible" = 等元素显示出来
            "hidden" = 等元素消失
        人话：等页面加载完，某个元素出现了再继续
        """
        timeout = timeout or self.timeout
        logger.info(f"Waiting for: {selector} (state={state})")
        locator = self.page.locator(selector)
        locator.wait_for(state=state, timeout=timeout)
        return locator

    def get_text(self, selector: str, timeout: int = None) -> str:
        """
        获取元素的文字内容
        用法：error_text = self.get_text(".error-msg")
        返回值：比如 "Warning: Password is wrong"
        人话：读取页面上某段文字是什么
        """
        timeout = timeout or self.timeout
        locator = self.wait_for_selector(selector, timeout=timeout)
        return locator.inner_text()

    def is_visible(self, selector: str, timeout: int = 5000) -> bool:
        """
        判断元素是否显示在页面上
        用法：if self.is_visible(".error-msg"): print("有错误")
        返回值：True = 显示了，False = 没显示
        人话：看某个元素在不在页面上
        """
        try:
            self.page.locator(selector).wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    def screenshot(self, name: str):
        """
        截图并保存到Allure报告
        用法：self.screenshot("login_success")
        人话：截一张当前页面的图，贴到测试报告里
        """
        screenshot = self.page.screenshot(full_page=True)
        allure.attach(screenshot, name=name, attachment_type=allure.attachment_type.PNG)
        logger.info(f"Screenshot saved: {name}")

    def _screenshot_on_failure(self, name: str):
        """
        失败时自动截图（内部方法，不用手动调用）
        人话：测试失败了自动截图，方便看哪里出了问题
        """
        try:
            screenshot = self.page.screenshot(full_page=True)
            allure.attach(
                screenshot,
                name=f"FAILURE_{name}",
                attachment_type=allure.attachment_type.PNG,
            )
            logger.warning(f"Failure screenshot: {name}")
        except Exception as e:
            logger.error(f"Screenshot failed: {e}")
