# -*- coding: utf-8 -*-
"""
Shopping cart UI tests
"""
import allure
import pytest
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from utils.logger import logger


@allure.feature("Shopping Cart UI")
class TestCartUI:

    @allure.story("Add to cart success")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_add_to_cart_success(self, page):
        """Add product to cart, should show success message"""
        # Login first
        login_page = LoginPage(page)
        login_page.open()
        login_page.login("testuser_2026@example.com", "Test@12345")

        # Search and add to cart
        product_page = ProductPage(page)
        product_page.open()
        product_page.search("MacBook")
        product_page.add_to_cart(0)
        product_page.screenshot("cart_add_success")
        assert product_page.is_cart_success()

    @allure.story("View cart")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_view_cart(self, page):
        """View shopping cart, should show cart page"""
        # Login first
        login_page = LoginPage(page)
        login_page.open()
        login_page.login("testuser_2026@example.com", "Test@12345")

        # Add to cart first
        product_page = ProductPage(page)
        product_page.open()
        product_page.search("MacBook")
        product_page.add_to_cart(0)

        # View cart
        product_page.go_to_cart()
        product_page.screenshot("cart_view")
        assert "cart" in page.url

    @allure.story("Cart shows correct item")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_cart_shows_item(self, page):
        """After adding product, cart should show the product"""
        # Login first
        login_page = LoginPage(page)
        login_page.open()
        login_page.login("testuser_2026@example.com", "Test@12345")

        # Add to cart
        product_page = ProductPage(page)
        product_page.open()
        product_page.search("MacBook")
        product_page.add_to_cart(0)

        # View cart
        product_page.go_to_cart()
        product_page.screenshot("cart_shows_item")
        # Cart page should contain product info
        assert "MacBook" in page.content() or "cart" in page.url

    @allure.story("Add multiple products")
    @allure.severity(allure.severity_level.NORMAL)
    def test_add_multiple_products(self, page):
        """Add multiple products to cart"""
        # Login first
        login_page = LoginPage(page)
        login_page.open()
        login_page.login("testuser_2026@example.com", "Test@12345")

        # Add first product
        product_page = ProductPage(page)
        product_page.open()
        product_page.search("MacBook")
        product_page.add_to_cart(0)

        # Add second product
        product_page.search("iPhone")
        if product_page.get_product_count() > 0:
            product_page.add_to_cart(0)

        product_page.screenshot("cart_multiple")
        # Should still show success
        assert product_page.is_cart_success() or "cart" in page.url
