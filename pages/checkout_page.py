# -*- coding: utf-8 -*-
"""
结算页面对象
作用：把结算流程的操作封装成函数（选支付方式、确认订单等）
"""
from pages.base_page import BasePage
from utils.config_reader import config
from utils.logger import logger


class CheckoutPage(BasePage):
    """结算页面对象，继承BasePage获得基础操作能力"""

    # ============================================
    # 元素定位器
    # ============================================
    BTN_PAYMENT_METHODS = "#button-payment-methods"  # 选择支付方式按钮
    BTN_CONFIRM_ORDER = "#button-confirm"             # 确认订单按钮
    INPUT_COMMENT = "#input-comment"                  # 订单备注输入框
    MSG_ORDER_SUCCESS = "h1:has-text('Your order has been placed')"  # 下单成功标题

    def checkout(self):
        """
        进入结算页面
        用法：checkout_page.checkout()
        原理：直接访问结算页面的URL
        """
        base_url = config.get("ui", "base_url")
        self.navigate(f"{base_url}/index.php?route=checkout/checkout")
        return self

    def fill_billing_details(self, details: dict):
        """
        填写订单备注
        参数details：字典，包含comment字段
        说明：登录用户已经有地址，不需要重新填写
        """
        comment = details.get("comment", "自动化测试订单")
        comment_input = self.page.locator(self.INPUT_COMMENT)
        if comment_input.is_visible(timeout=3000):
            comment_input.fill(comment)
        return self

    def confirm_order(self):
        """
        确认订单（最关键的函数）
        流程：点击选择支付方式 → 等待加载 → 点击确认订单
        """
        logger.info("Confirming order")

        # 第1步：点击"选择支付方式"按钮
        payment_btn = self.page.locator(self.BTN_PAYMENT_METHODS)
        if payment_btn.is_visible(timeout=5000):
            payment_btn.click()
            self.page.wait_for_timeout(2000)  # 等2秒让支付方式加载

        # 第2步：点击"确认订单"按钮
        confirm_btn = self.page.locator(self.BTN_CONFIRM_ORDER)
        if confirm_btn.is_visible(timeout=5000):
            confirm_btn.click()
            self.page.wait_for_load_state("domcontentloaded")
            self.page.wait_for_timeout(3000)  # 等3秒让订单处理完

        return self

    def is_order_success(self) -> bool:
        """判断订单是否提交成功（检查页面是否显示成功标题）"""
        return self.is_visible(self.MSG_ORDER_SUCCESS, timeout=15000)

    def get_order_id(self) -> str:
        """
        从页面提取订单号
        原理：用正则表达式从HTML里找到类似"order #12345"的文字
        """
        try:
            import re
            content = self.page.content()
            match = re.search(r"order\s*#(\d+)", content, re.IGNORECASE)
            if match:
                return match.group(1)
            return ""
        except Exception:
            return ""
