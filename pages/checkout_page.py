# -*- coding: utf-8 -*-
"""
结算页面对象模块
封装 OpenCart 购物车结算流程操作
登录用户结算流程：选择支付方式 → 确认订单
"""
from pages.base_page import BasePage
from utils.config_reader import config
from utils.logger import logger


class CheckoutPage(BasePage):
    """OpenCart 结算页面对象"""

    # 结算步骤按钮（OpenCart 4.x 登录用户简化流程）
    BTN_PAYMENT_METHODS = "#button-payment-methods"  # 选择支付方式
    BTN_CONFIRM_ORDER = "#button-confirm"              # 确认订单按钮
    INPUT_COMMENT = "#input-comment"                   # 订单备注

    # 结算成功
    MSG_ORDER_SUCCESS = "h1:has-text('Your order has been placed')"  # 订单成功标题
    MSG_PAYMENT_CHOSEN = ".alert-success"              # 支付方式已选择提示

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
        填写订单备注（登录用户无需填写地址）
        :param details: 包含 comment 字段的字典
        """
        logger.info("Filling order comment")
        # 如果有备注输入框，填写备注
        comment = details.get("comment", "自动化测试订单")
        comment_input = self.page.locator(self.INPUT_COMMENT)
        if comment_input.is_visible(timeout=3000):
            comment_input.fill(comment)
        return self

    def confirm_order(self):
        """确认订单：选择支付方式 → 确认订单"""
        logger.info("Confirming order")

        # 步骤1：点击选择支付方式按钮
        payment_btn = self.page.locator(self.BTN_PAYMENT_METHODS)
        if payment_btn.is_visible(timeout=5000):
            payment_btn.click()
            self.page.wait_for_timeout(2000)
            logger.info("Payment method selected")

        # 步骤2：确认订单
        confirm_btn = self.page.locator(self.BTN_CONFIRM_ORDER)
        if confirm_btn.is_visible(timeout=5000):
            confirm_btn.click()
            self.page.wait_for_load_state("domcontentloaded")
            self.page.wait_for_timeout(3000)
            logger.info("Order confirmed")

        return self

    def is_order_success(self) -> bool:
        """判断订单是否提交成功"""
        return self.is_visible(self.MSG_ORDER_SUCCESS, timeout=15000)

    def get_order_id(self) -> str:
        """
        获取订单号
        :return: 订单号字符串
        """
        try:
            # OpenCart 4.x 订单成功页面显示 "order #12345"
            content = self.page.content()
            if "order" in content.lower():
                # 尝试从页面提取订单号
                import re
                match = re.search(r"order\s*#(\d+)", content, re.IGNORECASE)
                if match:
                    return match.group(1)
            return ""
        except Exception:
            logger.warning("Failed to extract order ID")
            return ""
