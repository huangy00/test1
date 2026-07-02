# -*- coding: utf-8 -*-
"""
商品页面对象模块
封装 OpenCart 商品搜索和加购操作
定位器参考 OpenCart 4.x 商品页面
"""
from pages.base_page import BasePage
from utils.config_reader import config
from utils.logger import logger


class ProductPage(BasePage):
    """OpenCart 商品页面对象"""

    # 页面元素定位器
    INPUT_SEARCH = "input[name='search']"                # 搜索框
    BTN_SEARCH = "button[type='button']"                  # 搜索按钮
    LIST_PRODUCTS = ".product-thumb"                      # 商品卡片列表
    PRODUCT_NAME = ".product-thumb h4 a"                  # 商品名称
    PRODUCT_PRICE = ".product-thumb .price"               # 商品价格
    BTN_ADD_CART = "button[title='Add to Cart']"           # 加入购物车按钮
    MSG_CART_SUCCESS = ".alert-success"                   # 加购成功提示
    BTN_VIEW_CART = "a[title='Shopping Cart']"            # 查看购物车按钮
    LINK_CONTINUE_SHOPPING = "a:has-text('Continue')"    # 继续购物链接

    def open(self):
        """打开首页（用于搜索）"""
        base_url = config.get("ui", "base_url")
        self.navigate(f"{base_url}")
        logger.info("Home page opened")
        return self

    def search(self, keyword: str):
        """
        搜索商品
        :param keyword: 搜索关键词
        """
        logger.info(f"Searching product: {keyword}")
        self.fill(self.INPUT_SEARCH, keyword)
        # 使用 Enter 键提交搜索（比点击按钮更可靠）
        self.page.locator(self.INPUT_SEARCH).press("Enter")
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_timeout(1000)
        return self

    def get_product_count(self) -> int:
        """获取搜索结果商品数量"""
        return len(self.page.locator(self.LIST_PRODUCTS).all())

    def get_product_name(self, index: int = 0) -> str:
        """
        获取指定位置商品名称
        :param index: 商品索引（从 0 开始）
        :return: 商品名称
        """
        return self.page.locator(self.PRODUCT_NAME).nth(index).inner_text()

    def add_to_cart(self, index: int = 0):
        """
        将指定商品加入购物车
        :param index: 商品索引
        """
        logger.info(f"Adding product at index {index} to cart")
        self.page.locator(self.BTN_ADD_CART).nth(index).click()
        # 等待加购成功提示出现
        self.wait_for_selector(self.MSG_CART_SUCCESS, timeout=5000)
        return self

    def go_to_cart(self):
        """跳转到购物车页面"""
        logger.info("Going to shopping cart")
        self.click(self.BTN_VIEW_CART)
        self.page.wait_for_load_state("domcontentloaded")
        return self

    def is_cart_success(self) -> bool:
        """判断加购是否成功"""
        return self.is_visible(self.MSG_CART_SUCCESS, timeout=5000)
