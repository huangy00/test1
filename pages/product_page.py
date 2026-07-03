# -*- coding: utf-8 -*-
"""
商品页面对象
作用：把商品搜索、加购、查看购物车等操作封装成函数
"""
from pages.base_page import BasePage
from utils.config_reader import config
from utils.logger import logger


class ProductPage(BasePage):
    """商品页面对象，继承BasePage获得基础操作能力"""

    # ============================================
    # 元素定位器
    # ============================================
    INPUT_SEARCH = "input[name='search']"            # 搜索框（name=search的input）
    BTN_SEARCH = "button[type='button']"              # 搜索按钮
    LIST_PRODUCTS = ".product-thumb"                  # 商品卡片（每个商品是一个product-thumb）
    PRODUCT_NAME = ".product-thumb h4 a"              # 商品名称（在h4标签里的a链接）
    PRODUCT_PRICE = ".product-thumb .price"           # 商品价格
    BTN_ADD_CART = "button[title='Add to Cart']"     # 加入购物车按钮
    MSG_CART_SUCCESS = ".alert-success"               # 加购成功提示
    BTN_VIEW_CART = "a[title='Shopping Cart']"        # 查看购物车按钮

    def open(self):
        """打开首页"""
        base_url = config.get("ui", "base_url")
        self.navigate(f"{base_url}")
        return self

    def search(self, keyword: str):
        """
        搜索商品
        用法：product_page.search("MacBook")
        原理：在搜索框输入关键词，然后按回车
        """
        logger.info(f"Searching product: {keyword}")

        # 第1步：在搜索框里填写关键词
        self.fill(self.INPUT_SEARCH, keyword)

        # 第2步：按回车提交搜索（比点击按钮更稳定）
        self.page.locator(self.INPUT_SEARCH).press("Enter")

        # 第3步：等待页面加载完
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_timeout(1000)  # 额外等1秒，确保内容加载完
        return self

    def get_product_count(self) -> int:
        """
        获取搜索结果的商品数量
        返回值：比如返回3，表示搜到3个商品
        原理：数页面上有多少个.product-thumb元素
        """
        return len(self.page.locator(self.LIST_PRODUCTS).all())

    def get_product_name(self, index: int = 0) -> str:
        """
        获取第几个商品的名称
        参数index：从0开始，0=第一个，1=第二个
        返回值：商品名称字符串，比如"MacBook"
        """
        return self.page.locator(self.PRODUCT_NAME).nth(index).inner_text()

    def add_to_cart(self, index: int = 0):
        """
        把第几个商品加入购物车
        参数index：从0开始
        原理：找到加购按钮，点击它
        """
        logger.info(f"Adding product at index {index} to cart")
        # nth(index) = 选择第几个按钮
        self.page.locator(self.BTN_ADD_CART).nth(index).click()
        # 等待加购成功提示出现
        self.wait_for_selector(self.MSG_CART_SUCCESS, timeout=5000)
        return self

    def go_to_cart(self):
        """点击查看购物车按钮"""
        self.click(self.BTN_VIEW_CART)
        self.page.wait_for_load_state("domcontentloaded")
        return self

    def is_cart_success(self) -> bool:
        """判断加购是否成功（成功提示框是否显示）"""
        return self.is_visible(self.MSG_CART_SUCCESS, timeout=5000)
