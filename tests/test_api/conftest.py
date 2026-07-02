# -*- coding: utf-8 -*-
"""
API test fixtures
"""
import pytest
import requests
from utils.config_reader import config
from utils.logger import logger


@pytest.fixture(scope="function")
def api_session():
    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json, text/html, */*",
    })
    logger.info("API session created")
    yield session
    session.close()
    logger.info("API session closed")


@pytest.fixture(scope="function")
def site_url():
    return config.get("ui", "base_url").rstrip("/")


@pytest.fixture(scope="function")
def logged_in_session(api_session, site_url):
    api_session.get(f"{site_url}/index.php?route=account/login")
    login_data = {
        "email": "testuser_2026@example.com",
        "password": "Test@12345",
    }
    response = api_session.post(
        f"{site_url}/index.php?route=account/login.login",
        data=login_data,
        allow_redirects=True,
    )
    logger.info(f"Login response: {response.status_code}")
    yield api_session
