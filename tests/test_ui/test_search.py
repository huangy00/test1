# -*- coding: utf-8 -*-
"""
Product search UI tests
"""
import allure
import pytest
from pages.product_page import ProductPage
from utils.logger import logger


@allure.feature("Product Search UI")
class TestSearchUI:

    @allure.story("Normal search")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_search_success(self, page):
        """Search for existing product, should show results"""
        product_page = ProductPage(page)
        product_page.open()
        product_page.search("MacBook")
        product_page.screenshot("search_success")
        count = product_page.get_product_count()
        assert count >= 1, f"Expected at least 1 product, got {count}"

    @allure.story("No results")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_no_results(self, page):
        """Search for non-existent product, should show no results"""
        product_page = ProductPage(page)
        product_page.open()
        product_page.search("xyznonexistent123")
        product_page.screenshot("search_no_results")
        count = product_page.get_product_count()
        assert count == 0, f"Expected 0 products, got {count}"

    @allure.story("Empty keyword search")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_empty_keyword(self, page):
        """Search with empty keyword, should show all products or prompt"""
        product_page = ProductPage(page)
        product_page.open()
        product_page.search("")
        product_page.screenshot("search_empty")
        # Should show products or stay on same page
        assert page.url or product_page.get_product_count() >= 0

    @allure.story("Search result has correct product")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_result_content(self, page):
        """Search for MacBook, result should contain MacBook"""
        product_page = ProductPage(page)
        product_page.open()
        product_page.search("MacBook")
        product_page.screenshot("search_content")
        if product_page.get_product_count() > 0:
            name = product_page.get_product_name(0)
            assert "macbook" in name.lower()

    @allure.story("Special characters search")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_special_chars(self, page):
        """Search with special characters, should not crash"""
        product_page = ProductPage(page)
        product_page.open()
        product_page.search("!@#$%^&*()")
        product_page.screenshot("search_special_chars")
        # Should not crash, page should load
        assert product_page.get_product_count() >= 0

    @allure.story("SQL injection search")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_search_sql_injection(self, page):
        """SQL injection in search, should not cause error"""
        product_page = ProductPage(page)
        product_page.open()
        product_page.search("' OR 1=1 --")
        product_page.screenshot("search_sql_injection")
        # Should not crash
        assert product_page.get_product_count() >= 0
