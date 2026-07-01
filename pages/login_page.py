# -*- coding: utf-8 -*-
"""
登录页面对象模块
封装 OpenCart 登录页面的元素定位和操作方法
定位器参考 OpenCart 4.x 登录页面
"""
from pages.base_page import BasePage
from utils.config_reader import config
from utils.logger import logger


class LoginPage(BasePage):
    """OpenCart 登录页面对象"""

    # 页面元素定位器
    INPUT_EMAIL = "#input-email"              # 邮箱输入框
    INPUT_PASSWORD = "#input-password"        # 密码输入框
    BTN_LOGIN = "button.btn-primary[type='submit']"  # 登录按钮（Login）
    MSG_ERROR = ".alert-danger"               # 登录失败提示
    MSG_SUCCESS = ".alert-success"            # 登录成功提示
    LINK_REGISTER = "a:has-text('Register')"  # 注册链接
    LINK_ACCOUNT = "a:has-text('My Account')" # 我的账户链接

    def open(self):
        """打开登录页面"""
        base_url = config.get("ui", "base_url")
        self.navigate(f"{base_url}/index.php?route=account/login")
        logger.info("Login page opened")
        return self

    def login(self, email: str, password: str):
        """
        执行登录操作
        :param email: 邮箱
        :param password: 密码
        """
        logger.info(f"Logging in with: {email}")
        self.fill(self.INPUT_EMAIL, email)
        self.fill(self.INPUT_PASSWORD, password)
        self.click(self.BTN_LOGIN)
        return self

    def is_login_success(self) -> bool:
        """判断登录是否成功"""
        return self.is_visible(self.LINK_ACCOUNT, timeout=5000)

    def is_error_displayed(self) -> bool:
        """判断是否显示错误信息"""
        return self.is_visible(self.MSG_ERROR, timeout=3000)

    def get_error_message(self) -> str:
        """获取错误信息文本"""
        return self.get_text(self.MSG_ERROR)

    def click_register(self):
        """点击注册链接"""
        self.click(self.LINK_REGISTER)
        return self
