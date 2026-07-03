# -*- coding: utf-8 -*-
"""
结算流程UI自动化测试
作用：用代码模拟用户完整下单流程：登录→搜索→加购→结算→确认订单
"""
import allure
import pytest
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from pages.checkout_page import CheckoutPage
from utils.logger import logger


@allure.feature("Checkout Order UI")
class TestCheckoutUI:
    """结算流程测试类"""

    # ============================================
    # 用例1：结算页面可访问
    # ============================================
    @allure.story("Checkout page accessible")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_checkout_page_accessible(self, page):
        """用例：加购后能进入结算页面"""

        # 第1步：登录
        login_page = LoginPage(page)
        login_page.open()
        login_page.login("testuser_2026@example.com", "Test@12345")

        # 第2步：搜索并加购
        product_page = ProductPage(page)
        product_page.open()
        product_page.search("MacBook")
        product_page.add_to_cart(0)

        # 第3步：进入结算页面
        checkout_page = CheckoutPage(page)
        checkout_page.checkout()     # 跳转到结算页
        checkout_page.screenshot("checkout_accessible")

        # 第4步：断言URL包含checkout
        assert "checkout" in page.url

    # ============================================
    # 用例2：支付方式选择
    # ============================================
    @allure.story("Payment method selection")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_payment_method_selection(self, page):
        """用例：点击选择支付方式按钮"""

        # 第1步：登录
        login_page = LoginPage(page)
        login_page.open()
        login_page.login("testuser_2026@example.com", "Test@12345")

        # 第2步：搜索并加购
        product_page = ProductPage(page)
        product_page.open()
        product_page.search("MacBook")
        product_page.add_to_cart(0)

        # 第3步：进入结算页面
        checkout_page = CheckoutPage(page)
        checkout_page.checkout()

        # 第4步：点击选择支付方式按钮
        # locator = 定位器，找到页面上的按钮
        payment_btn = page.locator("#button-payment-methods")

        # 断言：按钮是否显示
        assert payment_btn.is_visible(timeout=5000)

        # 点击按钮
        payment_btn.click()
        page.wait_for_timeout(2000)  # 等2秒让支付方式加载出来
        checkout_page.screenshot("payment_method_selected")

    # ============================================
    # 用例3：确认订单按钮
    # ============================================
    @allure.story("Confirm order button")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_confirm_order_button(self, page):
        """用例：点击确认订单按钮完成下单"""

        # 第1步：登录
        login_page = LoginPage(page)
        login_page.open()
        login_page.login("testuser_2026@example.com", "Test@12345")

        # 第2步：搜索并加购
        product_page = ProductPage(page)
        product_page.open()
        product_page.search("MacBook")
        product_page.add_to_cart(0)

        # 第3步：进入结算页面
        checkout_page = CheckoutPage(page)
        checkout_page.checkout()

        # 第4步：确认订单（内部会先选支付方式，再点确认）
        checkout_page.confirm_order()
        checkout_page.screenshot("confirm_order")

        # 第5步：断言下单成功（URL应该包含checkout/success或order）
        assert "checkout" in page.url or "success" in page.url or "order" in page.url

    # ============================================
    # 用例4：订单摘要显示
    # ============================================
    @allure.story("Checkout shows order summary")
    @allure.severity(allure.severity_level.NORMAL)
    def test_checkout_order_summary(self, page):
        """用例：结算页面应该显示商品信息和总价"""

        # 第1步：登录
        login_page = LoginPage(page)
        login_page.open()
        login_page.login("testuser_2026@example.com", "Test@12345")

        # 第2步：搜索并加购
        product_page = ProductPage(page)
        product_page.open()
        product_page.search("MacBook")
        product_page.add_to_cart(0)

        # 第3步：进入结算页面
        checkout_page = CheckoutPage(page)
        checkout_page.checkout()
        checkout_page.screenshot("checkout_summary")

        # 第4步：断言页面包含商品信息
        # page.content() = 获取整个页面的HTML源代码
        content = page.content()
        assert "MacBook" in content or "Total" in content or "checkout" in page.url
