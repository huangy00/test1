# -*- coding: utf-8 -*-
"""
Login UI tests
"""
import allure
import pytest
from pages.login_page import LoginPage
from utils.logger import logger


@allure.feature("User Login UI")
class TestLoginUI:

    @allure.story("Normal login")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_login_success(self, page):
        """Login with correct credentials, should redirect to account page"""
        login_page = LoginPage(page)
        login_page.open()
        login_page.login("testuser_2026@example.com", "Test@12345")
        login_page.screenshot("login_success")
        # After login, URL should contain account
        assert "account" in page.url

    @allure.story("Wrong password")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_wrong_password(self, page):
        """Login with wrong password, should show error"""
        login_page = LoginPage(page)
        login_page.open()
        login_page.login("testuser_2026@example.com", "wrongpassword")
        login_page.screenshot("login_wrong_password")
        assert login_page.is_error_displayed()

    @allure.story("Nonexistent user")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_nonexistent_user(self, page):
        """Login with non-existent email, should show error"""
        login_page = LoginPage(page)
        login_page.open()
        login_page.login("nonexistent@example.com", "Test@12345")
        login_page.screenshot("login_nonexistent")
        assert login_page.is_error_displayed()

    @allure.story("Empty email")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_empty_email(self, page):
        """Login with empty email, should show error"""
        login_page = LoginPage(page)
        login_page.open()
        login_page.login("", "Test@12345")
        login_page.screenshot("login_empty_email")
        assert login_page.is_error_displayed() or "login" in page.url

    @allure.story("Empty password")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_empty_password(self, page):
        """Login with empty password, should show error"""
        login_page = LoginPage(page)
        login_page.open()
        login_page.login("testuser_2026@example.com", "")
        login_page.screenshot("login_empty_password")
        assert login_page.is_error_displayed() or "login" in page.url

    @allure.story("Empty form submit")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_empty_form(self, page):
        """Submit empty form, should show error"""
        login_page = LoginPage(page)
        login_page.open()
        login_page.login("", "")
        login_page.screenshot("login_empty_form")
        assert login_page.is_error_displayed() or "login" in page.url
