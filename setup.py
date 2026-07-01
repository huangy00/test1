# -*- coding: utf-8 -*-
"""
一键初始化脚本
自动完成：创建数据库 → 安装Python依赖 → 安装Playwright浏览器 → 安装支付扩展
"""
import os
import sys
import subprocess
import pymysql
from pymysql.cursors import DictCursor


def print_step(msg):
    print(f"\n{'='*50}")
    print(f"  {msg}")
    print(f"{'='*50}")


def check_mysql():
    """检查 MySQL 是否可连接"""
    print_step("步骤1：检查 MySQL 连接")
    try:
        conn = pymysql.connect(
            host="localhost", port=3306, user="root", password="root123456",
            charset="utf8mb4"
        )
        conn.close()
        print("  [OK] MySQL 连接成功")
        return True
    except Exception as e:
        print(f"  [FAIL] MySQL 连接失败: {e}")
        print("  请确保 XAMPP 的 MySQL 已启动，密码为 root123456")
        return False


def create_database():
    """创建数据库"""
    print_step("步骤2：创建数据库 xiangmu")
    conn = pymysql.connect(
        host="localhost", port=3306, user="root", password="root123456",
        charset="utf8mb4"
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS xiangmu CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci")
    cursor.execute("USE xiangmu")
    print("  [OK] 数据库 xiangmu 创建成功")
    conn.close()


def install_python_deps():
    """安装 Python 依赖"""
    print_step("步骤3：安装 Python 依赖")
    venv_path = os.path.join(os.path.dirname(__file__), "venv")

    # 创建虚拟环境
    if not os.path.exists(venv_path):
        print("  创建虚拟环境...")
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)

    # 根据系统选择 python/pip 路径
    if sys.platform == "win32":
        pip = os.path.join(venv_path, "Scripts", "pip.exe")
        python = os.path.join(venv_path, "Scripts", "python.exe")
    else:
        pip = os.path.join(venv_path, "bin", "pip")
        python = os.path.join(venv_path, "bin", "python")

    # 安装依赖
    print("  安装 requirements.txt...")
    subprocess.run([pip, "install", "-r", "requirements.txt"], check=True)
    print("  [OK] Python 依赖安装完成")
    return python


def install_playwright(python):
    """安装 Playwright 浏览器"""
    print_step("步骤4：安装 Playwright Chromium 浏览器")
    subprocess.run([python, "-m", "playwright", "install", "chromium"], check=True)
    print("  [OK] Playwright Chromium 安装完成")


def install_payment_extensions():
    """安装 OpenCart 支付扩展"""
    print_step("步骤5：安装支付扩展")
    try:
        conn = pymysql.connect(
            host="localhost", port=3306, user="root", password="root123456",
            database="xiangmu", charset="utf8mb4", cursorclass=DictCursor
        )
        cursor = conn.cursor()

        # 检查是否已安装
        cursor.execute("SELECT * FROM oc_extension_install WHERE code IN ('cod', 'free_checkout')")
        installed = cursor.fetchall()

        if len(installed) >= 2:
            print("  [OK] 支付扩展已安装，跳过")
        else:
            # 获取 extension_id
            cursor.execute("SELECT extension_id FROM oc_extension WHERE code='cod'")
            cod = cursor.fetchone()
            cursor.execute("SELECT extension_id FROM oc_extension WHERE code='free_checkout'")
            fc = cursor.fetchone()

            if cod:
                cursor.execute(
                    "INSERT IGNORE INTO oc_extension_install (extension_id, extension_download_id, name, description, code, version, author, link, status) VALUES (%s, 0, 'Cash on Delivery', 'Cash on Delivery', 'cod', '1.0', 'OpenCart', '', 1)",
                    (cod['extension_id'],)
                )
            if fc:
                cursor.execute(
                    "INSERT IGNORE INTO oc_extension_install (extension_id, extension_download_id, name, description, code, version, author, link, status) VALUES (%s, 0, 'Free Checkout', 'Free Checkout', 'free_checkout', '1.0', 'OpenCart', '', 1)",
                    (fc['extension_id'],)
                )
            conn.commit()
            print("  [OK] 支付扩展安装完成")

        conn.close()
    except Exception as e:
        print(f"  [WARN] 支付扩展安装跳过: {e}")
        print("  如果 OpenCart 未安装，此步骤可忽略")


def main():
    print("\n" + "="*50)
    print("  OpenCart 自动化测试框架 - 一键初始化")
    print("="*50)

    if not check_mysql():
        sys.exit(1)

    create_database()
    python = install_python_deps()
    install_playwright(python)
    install_payment_extensions()

    print_step("初始化完成!")
    print("""
  使用方法：
    1. 启动 XAMPP（Apache + MySQL）
    2. 部署 OpenCart 到 htdocs/opencart
    3. 运行测试：
       venv\\Scripts\\activate     # Windows
       source venv/bin/activate    # Linux/Mac
       pytest tests/ -v
    4. 查看 Allure 报告：
       allure serve allure-results
""")


if __name__ == "__main__":
    main()
