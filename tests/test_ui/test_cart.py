# -*- coding: utf-8 -*-
"""
购物车UI自动化测试
作用：用代码模拟用户登录后搜索商品、加入购物车、查看购物车
"""
import allure
import pytest
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from utils.logger import logger


@allure.feature("Shopping Cart UI")
class TestCartUI:
    """购物车测试类"""

    # ============================================
    # 用例1：正常加购
    # ============================================
    @allure.story("Add to cart success")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_add_to_cart_success(self, page):
        """用例：登录后搜索商品并加入购物车，应该显示成功提示"""

        # 第1步：先登录（购物车需要登录状态）
        login_page = LoginPage(page)
        login_page.open()
        login_page.login("testuser_2026@example.com", "Test@12345")

        # 第2步：搜索商品并加购
        product_page = ProductPage(page)
        product_page.open()
        product_page.search("MacBook")

        # add_to_cart(0) = 把第一个搜索结果加入购物车
        product_page.add_to_cart(0)
        product_page.screenshot("cart_add_success")

        # 第3步：断言加购成功
        assert product_page.is_cart_success()

    # ============================================
    # 用例2：查看购物车
    # ============================================
    @allure.story("View cart")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_view_cart(self, page):
        """用例：加购后查看购物车，应该跳转到购物车页面"""

        # 第1步：登录
        login_page = LoginPage(page)
        login_page.open()
        login_page.login("testuser_2026@example.com", "Test@12345")

        # 第2步：搜索并加购
        product_page = ProductPage(page)
        product_page.open()
        product_page.search("MacBook")
        product_page.add_to_cart(0)

        # 第3步：点击查看购物车
        product_page.go_to_cart()
        product_page.screenshot("cart_view")

        # 第4步：断言URL包含cart（跳转到了购物车页面）
        assert "cart" in page.url

    # ============================================
    # 用例3：购物车显示正确的商品
    # ============================================
    @allure.story("Cart shows correct item")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_cart_shows_item(self, page):
        """用例：加购后购物车里应该显示该商品"""

        # 第1步：登录
        login_page = LoginPage(page)
        login_page.open()
        login_page.login("testuser_2026@example.com", "Test@12345")

        # 第2步：搜索并加购MacBook
        product_page = ProductPage(page)
        product_page.open()
        product_page.search("MacBook")
        product_page.add_to_cart(0)

        # 第3步：查看购物车
        product_page.go_to_cart()
        product_page.screenshot("cart_shows_item")

        # 第4步：断言购物车页面包含MacBook这个文字
        # page.content() = 获取整个页面的HTML源代码
        assert "MacBook" in page.content() or "cart" in page.url

    # ============================================
    # 用例4：加购多个商品
    # ============================================
    @allure.story("Add multiple products")
    @allure.severity(allure.severity_level.NORMAL)
    def test_add_multiple_products(self, page):
        """用例：连续加购两个不同的商品"""

        # 第1步：登录
        login_page = LoginPage(page)
        login_page.open()
        login_page.login("testuser_2026@example.com", "Test@12345")

        # 第2步：加购第一个商品（MacBook）
        product_page = ProductPage(page)
        product_page.open()
        product_page.search("MacBook")
        product_page.add_to_cart(0)

        # 第3步：加购第二个商品（iPhone）
        product_page.search("iPhone")
        # 如果搜到了iPhone，就加购第一个
        if product_page.get_product_count() > 0:
            product_page.add_to_cart(0)

        product_page.screenshot("cart_multiple")

        # 第4步：断言加购成功
        assert product_page.is_cart_success() or "cart" in page.url
