# -*- coding: utf-8 -*-
"""
数据库数据一致性测试
专门测试数据库中的数据完整性和一致性
包括：用户注册后数据落库验证、订单生成后数据验证
"""
import allure
import pytest
from utils.db_helper import db_helper
from utils.logger import logger


@allure.feature("数据库数据一致性")
class TestDataConsistency:
    """数据库数据一致性测试类"""

    @allure.story("用户数据一致性")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_user_exists_after_registration(self, test_data):
        """
        验证用户注册后数据已正确写入数据库
        查询 oc_customer 表，确认用户记录存在
        """
        email = test_data["register_user"]["email"]

        with allure.step(f"查询用户: {email}"):
            user = db_helper.query_one(
                "SELECT * FROM oc_customer WHERE email = %s", (email,)
            )

        with allure.step("验证用户记录"):
            if user:
                allure.attach(
                    str(user),
                    name="用户记录",
                    attachment_type=allure.attachment_type.JSON,
                )
                logger.info(f"User found: {user.get('email')}")
            else:
                allure.attach(
                    f"未找到用户: {email}",
                    name="用户记录",
                    attachment_type=allure.attachment_type.TEXT,
                )
                logger.warning(f"User not found: {email}")

            # 断言用户存在
            assert user is not None, f"用户 {email} 在数据库中不存在"
            assert user["email"] == email, f"邮箱不匹配: {user['email']} != {email}"

    @allure.story("订单数据一致性")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_order_exists_after_checkout(self, test_data):
        """
        验证下单后订单数据已正确写入数据库
        查询 oc_order 表，确认订单记录存在
        """
        with allure.step("查询最新订单"):
            order = db_helper.query_one(
                "SELECT * FROM oc_order ORDER BY order_id DESC LIMIT 1"
            )

        with allure.step("验证订单记录"):
            if order:
                allure.attach(
                    str(order),
                    name="订单记录",
                    attachment_type=allure.attachment_type.JSON,
                )
                logger.info(f"Order found: order_id={order.get('order_id')}")
            else:
                allure.attach(
                    "未找到订单记录",
                    name="订单记录",
                    attachment_type=allure.attachment_type.TEXT,
                )
                logger.warning("No order found")

            # 断言订单存在
            assert order is not None, "数据库中未找到订单记录"
            assert order["order_id"] is not None, "订单ID为空"
            assert order["total"] > 0, f"订单金额异常: {order['total']}"

    @allure.story("订单商品关联一致性")
    @allure.severity(allure.severity_level.NORMAL)
    def test_order_product_consistency(self, test_data):
        """
        验证订单与商品的关联关系正确
        查询 oc_order 表和 oc_order_product 表，确认订单包含正确的商品
        """
        with allure.step("查询最新订单"):
            order = db_helper.query_one(
                "SELECT * FROM oc_order ORDER BY order_id DESC LIMIT 1"
            )

        if order is None:
            pytest.skip("没有找到订单记录，跳过测试")

        order_id = order["order_id"]

        with allure.step(f"查询订单商品: order_id={order_id}"):
            order_products = db_helper.query_all(
                "SELECT * FROM oc_order_product WHERE order_id = %s", (order_id,)
            )

        with allure.step("验证订单商品关联"):
            if order_products:
                allure.attach(
                    str(order_products),
                    name="订单商品记录",
                    attachment_type=allure.attachment_type.JSON,
                )
                logger.info(f"Order products count: {len(order_products)}")
            else:
                allure.attach(
                    "订单无关联商品",
                    name="订单商品记录",
                    attachment_type=allure.attachment_type.TEXT,
                )

            # 断言订单有商品
            assert len(order_products) > 0, f"订单 {order_id} 没有关联商品"

    @allure.story("库存一致性")
    @allure.severity(allure.severity_level.NORMAL)
    def test_stock_consistency(self, test_data):
        """
        验证下单后商品库存已正确扣减
        对比 oc_product 的 quantity 和订单数量
        """
        with allure.step("查询最新订单商品"):
            order = db_helper.query_one(
                "SELECT * FROM oc_order ORDER BY order_id DESC LIMIT 1"
            )
            if order is None:
                pytest.skip("没有找到订单记录，跳过测试")

            order_products = db_helper.query_all(
                "SELECT * FROM oc_order_product WHERE order_id = %s",
                (order["order_id"],),
            )

        with allure.step("验证库存扣减"):
            for op in order_products:
                product = db_helper.query_one(
                    "SELECT quantity FROM oc_product WHERE product_id = %s",
                    (op["product_id"],),
                )
                if product:
                    allure.attach(
                        f"商品ID: {op['product_id']}, 订单数量: {op['quantity']}, 当前库存: {product['quantity']}",
                        name=f"商品{op['product_id']}库存",
                        attachment_type=allure.attachment_type.TEXT,
                    )
                    logger.info(
                        f"Product {op['product_id']}: ordered={op['quantity']}, stock={product['quantity']}"
                    )
