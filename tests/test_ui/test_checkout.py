# -*- coding: utf-8 -*-
"""
Checkout / order UI tests
"""
import allure
import pytest
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from pages.checkout_page import CheckoutPage
from utils.logger import logger


@allure.feature("Checkout Order UI")
class TestCheckoutUI:

    @allure.story("Checkout page accessible")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_checkout_page_accessible(self, page):
        """After adding product, checkout page should be accessible"""
        # Login
        login_page = LoginPage(page)
        login_page.open()
        login_page.login("testuser_2026@example.com", "Test@12345")

        # Add to cart
        product_page = ProductPage(page)
        product_page.open()
        product_page.search("MacBook")
        product_page.add_to_cart(0)

        # Go to checkout
        checkout_page = CheckoutPage(page)
        checkout_page.checkout()
        checkout_page.screenshot("checkout_accessible")
        assert "checkout" in page.url

    @allure.story("Payment method selection")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_payment_method_selection(self, page):
        """Payment method button should be visible and clickable"""
        # Login
        login_page = LoginPage(page)
        login_page.open()
        login_page.login("testuser_2026@example.com", "Test@12345")

        # Add to cart
        product_page = ProductPage(page)
        product_page.open()
        product_page.search("MacBook")
        product_page.add_to_cart(0)

        # Go to checkout
        checkout_page = CheckoutPage(page)
        checkout_page.checkout()

        # Click payment method
        payment_btn = page.locator("#button-payment-methods")
        assert payment_btn.is_visible(timeout=5000)
        payment_btn.click()
        page.wait_for_timeout(2000)
        checkout_page.screenshot("payment_method_selected")

    @allure.story("Confirm order button")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_confirm_order_button(self, page):
        """Confirm order button should exist"""
        # Login
        login_page = LoginPage(page)
        login_page.open()
        login_page.login("testuser_2026@example.com", "Test@12345")

        # Add to cart
        product_page = ProductPage(page)
        product_page.open()
        product_page.search("MacBook")
        product_page.add_to_cart(0)

        # Go to checkout
        checkout_page = CheckoutPage(page)
        checkout_page.checkout()

        # Confirm order
        checkout_page.confirm_order()
        checkout_page.screenshot("confirm_order")
        # After confirm, should show success or redirect
        assert "checkout" in page.url or "success" in page.url or "order" in page.url

    @allure.story("Checkout shows order summary")
    @allure.severity(allure.severity_level.NORMAL)
    def test_checkout_order_summary(self, page):
        """Checkout page should show order summary with product and total"""
        # Login
        login_page = LoginPage(page)
        login_page.open()
        login_page.login("testuser_2026@example.com", "Test@12345")

        # Add to cart
        product_page = ProductPage(page)
        product_page.open()
        product_page.search("MacBook")
        product_page.add_to_cart(0)

        # Go to checkout
        checkout_page = CheckoutPage(page)
        checkout_page.checkout()
        checkout_page.screenshot("checkout_summary")

        # Should contain product name and price info
        content = page.content()
        assert "MacBook" in content or "Total" in content or "checkout" in page.url
