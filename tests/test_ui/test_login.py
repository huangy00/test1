# -*- coding: utf-8 -*-
"""
登录页面UI自动化测试
作用：用代码模拟用户在浏览器里操作登录页面
"""
import allure
import pytest
from pages.login_page import LoginPage
from utils.logger import logger


# @allure.feature 标记这个类属于"登录UI"模块，生成报告时会分组显示
@allure.feature("User Login UI")
class TestLoginUI:
    """登录页面测试类"""

    # ============================================
    # 用例1：正常登录
    # ============================================
    # @allure.story 标记具体场景名称
    # @allure.severity 标记严重程度（BLOCKER=阻塞级，最重要）
    @allure.story("Normal login")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_login_success(self, page):
        """
        用例：正确账号密码登录
        page 参数：由 conftest.py 的 fixture 自动传入，是一个浏览器页面对象
        """
        # 第1步：创建登录页面对象（把页面操作封装成函数）
        login_page = LoginPage(page)

        # 第2步：打开登录页面
        login_page.open()

        # 第3步：填写邮箱和密码，点击登录
        login_page.login("testuser_2026@example.com", "Test12345")

        # 第4步：截图保存（方便事后查看）
        login_page.screenshot("login_success")

        # 第5步：断言 - 检查URL是否包含account（登录成功会跳转到账户页）
        assert "account" in page.url

    # ============================================
    # 用例2：密码错误
    # ============================================
    @allure.story("Wrong password")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_wrong_password(self, page):
        """用例：输入错误密码，应该显示错误提示"""
        login_page = LoginPage(page)
        login_page.open()

        # 用错误密码登录
        login_page.login("testuser_2026@example.com", "wrongpassword")
        login_page.screenshot("login_wrong_password")

        # 断言：错误提示框是否显示
        assert login_page.is_error_displayed()

    # ============================================
    # 用例3：账号不存在
    # ============================================
    @allure.story("Nonexistent user")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_nonexistent_user(self, page):
        """用例：用不存在的邮箱登录，应该显示错误提示"""
        login_page = LoginPage(page)
        login_page.open()

        # 用不存在的邮箱登录
        login_page.login("nonexistent@example.com", "Test12345")
        login_page.screenshot("login_nonexistent")

        # 断言：错误提示框是否显示
        assert login_page.is_error_displayed()

    # ============================================
    # 用例4：邮箱为空
    # ============================================
    @allure.story("Empty email")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_empty_email(self, page):
        """用例：邮箱不填直接登录，应该显示错误或留在登录页"""
        login_page = LoginPage(page)
        login_page.open()

        # 邮箱传空字符串
        login_page.login("", "Test12345")
        login_page.screenshot("login_empty_email")

        # 断言：要么显示错误提示，要么还在登录页
        assert login_page.is_error_displayed() or "login" in page.url

    # ============================================
    # 用例5：密码为空
    # ============================================
    @allure.story("Empty password")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_empty_password(self, page):
        """用例：密码不填直接登录，应该显示错误或留在登录页"""
        login_page = LoginPage(page)
        login_page.open()

        # 密码传空字符串
        login_page.login("testuser_2026@example.com", "")
        login_page.screenshot("login_empty_password")

        assert login_page.is_error_displayed() or "login" in page.url

    # ============================================
    # 用例6：全部为空
    # ============================================
    @allure.story("Empty form submit")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_empty_form(self, page):
        """用例：邮箱和密码都不填，应该显示错误或留在登录页"""
        login_page = LoginPage(page)
        login_page.open()

        # 两个都传空
        login_page.login("", "")
        login_page.screenshot("login_empty_form")

        assert login_page.is_error_displayed() or "login" in page.url
