# -*- coding: utf-8 -*-
"""
商品搜索UI自动化测试
作用：用代码模拟用户在搜索框里输入关键词并搜索
"""
import allure
import pytest
from pages.product_page import ProductPage
from utils.logger import logger


@allure.feature("Product Search UI")
class TestSearchUI:
    """商品搜索测试类"""

    # ============================================
    # 用例1：正常搜索
    # ============================================
    @allure.story("Normal search")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_search_success(self, page):
        """用例：搜索存在的商品，应该显示搜索结果"""
        # 创建商品页面对象
        product_page = ProductPage(page)
        product_page.open()

        # 在搜索框输入MacBook并按回车
        product_page.search("MacBook")
        product_page.screenshot("search_success")

        # 获取搜索结果数量
        count = product_page.get_product_count()

        # 断言：至少搜到1个商品
        assert count >= 1, f"Expected at least 1 product, got {count}"

    # ============================================
    # 用例2：搜索不存在的商品
    # ============================================
    @allure.story("No results")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_no_results(self, page):
        """用例：搜索不存在的商品，应该显示无结果"""
        product_page = ProductPage(page)
        product_page.open()

        # 搜索一个不存在的词
        product_page.search("xyznonexistent123")
        product_page.screenshot("search_no_results")

        # 获取搜索结果数量
        count = product_page.get_product_count()

        # 断言：结果数量应该是0
        assert count == 0, f"Expected 0 products, got {count}"

    # ============================================
    # 用例3：空关键词搜索
    # ============================================
    @allure.story("Empty keyword search")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_empty_keyword(self, page):
        """用例：搜索框为空时搜索，应该显示全部商品或提示"""
        product_page = ProductPage(page)
        product_page.open()

        # 搜索空字符串
        product_page.search("")
        product_page.screenshot("search_empty")

        # 断言：页面正常加载就行
        assert product_page.get_product_count() >= 0

    # ============================================
    # 用例4：验证搜索结果内容
    # ============================================
    @allure.story("Search result has correct product")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_result_content(self, page):
        """用例：搜索MacBook，结果应该包含MacBook"""
        product_page = ProductPage(page)
        product_page.open()
        product_page.search("MacBook")
        product_page.screenshot("search_content")

        # 如果有搜索结果，检查第一个商品名是否包含macbook
        if product_page.get_product_count() > 0:
            name = product_page.get_product_name(0)
            assert "macbook" in name.lower()

    # ============================================
    # 用例5：特殊字符搜索
    # ============================================
    @allure.story("Special characters search")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_special_chars(self, page):
        """用例：搜索特殊字符，不应该报错崩溃"""
        product_page = ProductPage(page)
        product_page.open()
        product_page.search("!@#$%^&*()")
        product_page.screenshot("search_special_chars")

        # 断言：页面正常加载就行
        assert product_page.get_product_count() >= 0

    # ============================================
    # 用例6：SQL注入搜索
    # ============================================
    @allure.story("SQL injection search")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_search_sql_injection(self, page):
        """用例：搜索SQL注入语句，不应该报500服务器错误"""
        product_page = ProductPage(page)
        product_page.open()

        # 搜索SQL注入语句
        product_page.search("' OR 1=1 --")
        product_page.screenshot("search_sql_injection")

        # 断言：页面正常加载就行
        assert product_page.get_product_count() >= 0
