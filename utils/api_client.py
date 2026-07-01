# -*- coding: utf-8 -*-
"""
API 客户端工具模块
封装 requests.Session，统一处理 base_url、headers、超时
支持 GET / POST / PUT / DELETE，请求和响应自动记录日志，超时自动重试
"""
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from utils.config_reader import config
from utils.logger import logger


class APIClient:
    """HTTP API 客户端，封装 requests 实现统一请求管理"""

    def __init__(self):
        """初始化 API 客户端，创建 Session 并配置重试策略"""
        self.session = requests.Session()
        self.base_url = config.get("ui", "base_url")
        self.timeout = config.getint("DEFAULT", "timeout")

        # 设置默认请求头
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

        # 配置超时重试策略：最多重试 3 次，指数退避
        retry_strategy = Retry(
            total=3,                    # 最多重试 3 次
            backoff_factor=1,           # 退避因子，每次重试间隔翻倍
            status_forcelist=[500, 502, 503, 504],  # 遇到这些状态码重试
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        logger.info(f"APIClient initialized, base_url={self.base_url}")

    def _build_url(self, path: str) -> str:
        """
        拼接完整 URL
        :param path: API 路径（如 /api/product）
        :return: 完整的请求 URL
        """
        return f"{self.base_url}{path}"

    def get(self, path: str, **kwargs) -> requests.Response:
        """
        发送 GET 请求
        :param path: API 路径
        :param kwargs: 传递给 requests 的额外参数
        :return: Response 对象
        """
        return self._request("GET", path, **kwargs)

    def post(self, path: str, **kwargs) -> requests.Response:
        """
        发送 POST 请求
        :param path: API 路径
        :param kwargs: 传递给 requests 的额外参数
        :return: Response 对象
        """
        return self._request("POST", path, **kwargs)

    def put(self, path: str, **kwargs) -> requests.Response:
        """
        发送 PUT 请求
        :param path: API 路径
        :param kwargs: 传递给 requests 的额外参数
        :return: Response 对象
        """
        return self._request("PUT", path, **kwargs)

    def delete(self, path: str, **kwargs) -> requests.Response:
        """
        发送 DELETE 请求
        :param path: API 路径
        :param kwargs: 传递给 requests 的额外参数
        :return: Response 对象
        """
        return self._request("DELETE", path, **kwargs)

    def _request(self, method: str, path: str, **kwargs) -> requests.Response:
        """
        统一请求方法，处理日志记录、超时、异常
        :param method: HTTP 方法
        :param path: API 路径
        :param kwargs: 额外参数
        :return: Response 对象
        """
        url = self._build_url(path)
        kwargs.setdefault("timeout", self.timeout)

        # 记录请求日志
        logger.info(f"[{method}] {url}")
        if "json" in kwargs:
            logger.debug(f"Request body: {kwargs['json']}")

        try:
            response = self.session.request(method, url, **kwargs)

            # 记录响应日志
            logger.info(f"[{method}] {url} -> {response.status_code}")
            logger.debug(f"Response body: {response.text[:500]}")

            return response

        except requests.exceptions.Timeout:
            logger.error(f"[{method}] {url} -> Timeout after {self.timeout}s")
            raise
        except requests.exceptions.ConnectionError:
            logger.error(f"[{method}] {url} -> Connection Error")
            raise
        except Exception as e:
            logger.error(f"[{method}] {url} -> Error: {e}")
            raise

    def close(self):
        """关闭 Session 连接"""
        self.session.close()
        logger.info("APIClient session closed")


# 全局 API 客户端实例
api_client = APIClient()
