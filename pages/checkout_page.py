# -*- coding: utf-8 -*-
"""
结算页面对象模块
封装 OpenCart 购物车结算流程操作
包括填写账单地址、选择配送方式、确认订单等步骤
"""
from pages.base_page import BasePage
from utils.config_reader import config
from utils.logger import logger


class CheckoutPage(BasePage):
    """OpenCart 结算页面对象"""

    # 账单地址表单定位器
    INPUT_FIRSTNAME = "#input-payment-firstname"
    INPUT_LASTNAME = "#input-payment-lastname"
    INPUT_EMAIL = "#input-payment-email"
    INPUT_TELEPHONE = "#input-payment-telephone"
    INPUT_ADDRESS = "#input-payment-address-1"
    INPUT_CITY = "#input-payment-city"
    INPUT_POSTCODE = "#input-payment-postcode"
    SELECT_COUNTRY = "#input-payment-country"
    SELECT_REGION = "#input-payment-zone"

    # 结算步骤按钮
    BTN_GUEST_CHECKOUT = "#button-guest"           # 游客结算按钮
    BTN_CONTINUE_DELIVERY = "#button-shipping-method"  # 继续配送方式
    BTN_CONTINUE_PAYMENT = "#button-payment-method"    # 继续支付方式
    BTN_CONFIRM_ORDER = "#button-confirm"              # 确认订单按钮

    # 结算成功
    MSG_ORDER_SUCCESS = "h1:has-text('Your order has been placed')"  # 订单成功标题
    ORDER_ID = ".mr-auto"                              # 订单号

    def go_to_cart(self):
        """跳转到购物车页面"""
        base_url = config.get("ui", "base_url")
        self.navigate(f"{base_url}/index.php?route=checkout/cart")
        logger.info("Cart page opened")
        return self

    def go_to_checkout(self):
        """跳转到结算页面"""
        base_url = config.get("ui", "base_url")
        self.navigate(f"{base_url}/index.php?route=checkout/checkout")
        logger.info("Checkout page opened")
        return self

    def checkout(self):
        """从购物车跳转到结算页面"""
        base_url = config.get("ui", "base_url")
        self.navigate(f"{base_url}/index.php?route=checkout/checkout")
        logger.info("Checkout initiated")
        return self

    def fill_billing_details(self, details: dict):
        """
        填写账单地址
        :param details: 地址信息字典，包含 firstname, lastname, email 等字段
        """
        logger.info("Filling billing details")
        self.fill(self.INPUT_FIRSTNAME, details.get("firstname", ""))
        self.fill(self.INPUT_LASTNAME, details.get("lastname", ""))
        self.fill(self.INPUT_EMAIL, details.get("email", ""))
        self.fill(self.INPUT_TELEPHONE, details.get("telephone", ""))
        self.fill(self.INPUT_ADDRESS, details.get("address", ""))
        self.fill(self.INPUT_CITY, details.get("city", ""))
        self.fill(self.INPUT_POSTCODE, details.get("postcode", ""))

        # 选择国家（如果有下拉框）
        country_select = self.page.locator(self.SELECT_COUNTRY)
        if country_select.is_visible(timeout=2000):
            country_select.select_option(label=details.get("country", "China"))

        # 选择地区（如果有下拉框）
        region_select = self.page.locator(self.SELECT_REGION)
        if region_select.is_visible(timeout=2000):
            region_select.select_option(label=details.get("region", "Beijing"))

        return self

    def confirm_order(self):
        """确认订单：依次点击各步骤按钮"""
        logger.info("Confirming order")

        # 步骤1：点击游客结算（如果不是登录用户）
        guest_btn = self.page.locator(self.BTN_GUEST_CHECKOUT)
        if guest_btn.is_visible(timeout=3000):
            guest_btn.click()

        # 步骤2：继续配送方式
        delivery_btn = self.page.locator(self.BTN_CONTINUE_DELIVERY)
        if delivery_btn.is_visible(timeout=3000):
            delivery_btn.click()
            self.page.wait_for_timeout(1000)

        # 步骤3：继续支付方式
        payment_btn = self.page.locator(self.BTN_CONTINUE_PAYMENT)
        if payment_btn.is_visible(timeout=3000):
            payment_btn.click()
            self.page.wait_for_timeout(1000)

        # 步骤4：确认订单
        confirm_btn = self.page.locator(self.BTN_CONFIRM_ORDER)
        if confirm_btn.is_visible(timeout=3000):
            confirm_btn.click()
            self.page.wait_for_load_state("domcontentloaded")

        return self

    def is_order_success(self) -> bool:
        """判断订单是否提交成功"""
        return self.is_visible(self.MSG_ORDER_SUCCESS, timeout=10000)

    def get_order_id(self) -> str:
        """
        获取订单号
        :return: 订单号字符串
        """
        try:
            text = self.get_text(self.ORDER_ID)
            # 从文本中提取订单号（格式如 "Order #12345"）
            if "#" in text:
                return text.split("#")[-1].strip()
            return text
        except Exception:
            logger.warning("Failed to extract order ID")
            return ""
