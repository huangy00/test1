# -*- coding: utf-8 -*-
"""
登录页面对象
作用：把登录页面的所有操作封装成函数，测试脚本直接调用
"""
from pages.base_page import BasePage
from utils.config_reader import config
from utils.logger import logger


class LoginPage(BasePage):
    """登录页面对象，继承BasePage获得基础操作能力"""

    # ============================================
    # 元素定位器：用CSS选择器找到网页上的元素
    # 怎么找？打开浏览器F12 → 右键元素 → 检查 → 复制selector
    # ============================================
    INPUT_EMAIL = "#input-email"              # 邮箱输入框（id=input-email）
    INPUT_PASSWORD = "#input-password"        # 密码输入框（id=input-password）
    BTN_LOGIN = "button.btn-primary[type='submit']"  # 登录按钮（class包含btn-primary）
    MSG_ERROR = ".alert-danger"               # 错误提示框（class=alert-danger）
    MSG_SUCCESS = ".alert-success"            # 成功提示框（class=alert-success）
    LINK_REGISTER = "a:has-text('Register')"  # 注册链接（文字包含Register）
    LINK_ACCOUNT = "a:has-text('My Account')" # 我的账户链接（文字包含My Account）

    def open(self):
        """
        打开登录页面
        调用方式：login_page.open()
        """
        base_url = config.get("ui", "base_url")
        # navigate是BasePage的方法，作用是打开网页
        self.navigate(f"{base_url}/index.php?route=account/login")
        logger.info("Login page opened")
        return self

    def login(self, email: str, password: str):
        """
        执行登录操作
        调用方式：login_page.login("xxx@xxx.com", "password123")
        """
        logger.info(f"Logging in with: {email}")

        # fill是BasePage的方法，作用是在输入框里填写内容
        # 参数：第一个是CSS选择器（定位哪个输入框），第二个是要填的值
        self.fill(self.INPUT_EMAIL, email)
        self.fill(self.INPUT_PASSWORD, password)

        # click是BasePage的方法，作用是点击按钮
        self.click(self.BTN_LOGIN)
        return self

    def is_login_success(self) -> bool:
        """
        判断登录是否成功
        原理：登录成功后页面会出现" My Account"链接，检查这个链接在不在
        """
        return self.is_visible(self.LINK_ACCOUNT, timeout=5000)

    def is_error_displayed(self) -> bool:
        """
        判断是否显示错误提示
        原理：登录失败时页面会出现红色警告框，检查这个框在不在
        """
        return self.is_visible(self.MSG_ERROR, timeout=3000)

    def get_error_message(self) -> str:
        """
        获取错误提示的文字内容
        比如返回："Warning: No match for E-Mail Address and/or Password."
        """
        return self.get_text(self.MSG_ERROR)

    def click_register(self):
        """点击页面上的Register链接"""
        self.click(self.LINK_REGISTER)
        return self
