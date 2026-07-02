# -*- coding: utf-8 -*-
"""
User registration API tests
"""
import uuid
import allure
import pytest
from utils.logger import logger


@allure.feature("User Registration API")
class TestRegisterAPI:

    @allure.story("Normal registration")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_register_success(self, api_session, site_url):
        unique_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
        data = {
            "firstname": "Test",
            "lastname": "User",
            "email": unique_email,
            "telephone": "13800138000",
            "password": "Test@12345",
        }
        response = api_session.post(
            f"{site_url}/index.php?route=account/register.register",
            data=data,
        )
        logger.info(f"Register response: {response.status_code}")
        assert response.status_code in [200, 302]

    @allure.story("Duplicate email")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_register_duplicate_email(self, api_session, site_url):
        data = {
            "firstname": "Test",
            "lastname": "User",
            "email": "testuser_2026@example.com",
            "telephone": "13800138000",
            "password": "Test@12345",
        }
        response = api_session.post(
            f"{site_url}/index.php?route=account/register.register",
            data=data,
        )
        assert response.status_code == 200
        # OpenCart 4.x returns JSON redirect back to register page on failure
        assert "register" in response.text.lower() or "error" in response.text.lower()

    @allure.story("Empty email")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_register_empty_email(self, api_session, site_url):
        data = {
            "firstname": "Test",
            "lastname": "User",
            "email": "",
            "telephone": "13800138000",
            "password": "Test@12345",
        }
        response = api_session.post(
            f"{site_url}/index.php?route=account/register.register",
            data=data,
        )
        assert response.status_code == 200

    @allure.story("Empty password")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_register_empty_password(self, api_session, site_url):
        data = {
            "firstname": "Test",
            "lastname": "User",
            "email": "newuser@example.com",
            "telephone": "13800138000",
            "password": "",
        }
        response = api_session.post(
            f"{site_url}/index.php?route=account/register.register",
            data=data,
        )
        assert response.status_code == 200

    @allure.story("Invalid email format")
    @allure.severity(allure.severity_level.NORMAL)
    def test_register_invalid_email(self, api_session, site_url):
        data = {
            "firstname": "Test",
            "lastname": "User",
            "email": "invalidemail",
            "telephone": "13800138000",
            "password": "Test@12345",
        }
        response = api_session.post(
            f"{site_url}/index.php?route=account/register.register",
            data=data,
        )
        assert response.status_code == 200

    @allure.story("SQL injection")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_register_sql_injection(self, api_session, site_url):
        data = {
            "firstname": "Test",
            "lastname": "User",
            "email": "' OR 1=1 --@test.com",
            "telephone": "13800138000",
            "password": "Test@12345",
        }
        response = api_session.post(
            f"{site_url}/index.php?route=account/register.register",
            data=data,
        )
        assert response.status_code != 500

    @allure.story("XSS injection")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_register_xss(self, api_session, site_url):
        data = {
            "firstname": "<script>alert(1)</script>",
            "lastname": "User",
            "email": "xss_test@example.com",
            "telephone": "13800138000",
            "password": "Test@12345",
        }
        response = api_session.post(
            f"{site_url}/index.php?route=account/register.register",
            data=data,
        )
        assert response.status_code != 500
