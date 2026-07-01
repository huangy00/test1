# auto_test_framework - OpenCart 电商自动化测试框架

## 项目简介

本项目是一个针对本地部署的 OpenCart 电商系统的全链路自动化测试框架，覆盖 UI 自动化和数据库数据一致性验证两大维度。

### 技术栈

- **Python 3.11** - 主语言
- **Pytest** - 测试框架
- **Playwright** - UI 自动化
- **Requests** - HTTP 客户端
- **Allure** - 测试报告
- **PyMySQL** - 数据库操作

### 被测系统

- **OpenCart 4.1.0.3** - 本地部署 (http://localhost/opencart)
- **MySQL** - 数据库名 `xiangmu`，表前缀 `oc_`

## 目录结构

```
auto_test_framework/
├── config/
│   └── config.ini           # 配置文件
├── data/
│   ├── users.json           # 用户测试数据
│   └── products.json        # 商品测试数据
├── utils/
│   ├── __init__.py
│   ├── config_reader.py     # 配置读取
│   ├── logger.py            # 日志封装
│   ├── api_client.py        # API 客户端
│   └── db_helper.py         # 数据库助手
├── pages/
│   ├── __init__.py
│   ├── base_page.py         # 页面基类
│   ├── login_page.py        # 登录页面
│   ├── register_page.py     # 注册页面
│   ├── product_page.py      # 商品页面
│   └── checkout_page.py     # 结算页面
├── tests/
│   ├── __init__.py
│   ├── test_ui/
│   │   ├── __init__.py
│   │   └── test_checkout_flow.py  # 完整流程测试
│   └── test_db/
│       ├── __init__.py
│       └── test_data_consistency.py  # 数据一致性测试
├── conftest.py              # Pytest Fixture
├── pytest.ini               # Pytest 配置
├── requirements.txt         # Python 依赖
└── README.md                # 项目说明
```

## 环境要求

- Python 3.10+
- MySQL 8.0+ (XAMPP)
- OpenCart 4.x (已部署到 http://localhost/opencart)

## 快速开始

### 1. 安装依赖

```bash
cd auto_test_framework
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
playwright install chromium
```

### 2. 配置数据库

确保 MySQL 中存在 `xiangmu` 数据库：

```sql
CREATE DATABASE IF NOT EXISTS xiangmu CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
```

修改 `config/config.ini` 中的数据库连接信息：

```ini
[db]
host = localhost
port = 3306
user = root
password = root123456
database = xiangmu
```

### 3. 运行测试

```bash
# 运行所有测试
pytest

# 仅运行 UI 测试
pytest tests/test_ui/

# 仅运行数据库测试
pytest tests/test_db/

# 运行指定测试
pytest tests/test_ui/test_checkout_flow.py
```

### 4. 查看 Allure 报告

```bash
# 生成报告
allure generate allure-results -o allure-report --clean

# 打开报告
allure open allure-report
```

## 核心模块说明

### utils/config_reader.py
读取 `config.ini` 配置文件，提供 `get(section, key)` 和 `getint(section, key)` 方法。

### utils/logger.py
封装 logging 模块，同时输出到控制台和日志文件，格式：`时间 - 名称 - 级别 - 消息`。

### utils/api_client.py
封装 requests.Session，统一处理 base_url、headers、超时，支持 GET/POST/PUT/DELETE，超时自动重试 3 次。

### utils/db_helper.py
使用 pymysql 封装数据库操作，支持 `query_one`、`query_all`、`execute` 方法，连接参数从 config.ini 读取。

### pages/base_page.py
Playwright 基础页面封装，提供 click、fill、wait_for_selector、screenshot 等操作，失败时自动截图附加到 Allure。

### pages/register_page.py / login_page.py / product_page.py / checkout_page.py
各业务页面对象，封装元素定位和操作方法，遵循 POM 设计模式。

## 测试流程

```
注册用户 → 登录 → 搜索商品 → 加入购物车 → 下单结算 → 数据库验证
```

### UI 测试 (test_checkout_flow.py)

1. 使用 Playwright 操作浏览器完成完整购物流程
2. 下单成功后调用 db_helper 查询 oc_order 表验证订单落库
3. 查询结果附加到 Allure 报告

### 数据库测试 (test_data_consistency.py)

1. 用户注册后查询 oc_customer 表验证用户已插入
2. 下单后查询 oc_order 表验证订单已生成
3. 验证订单商品关联和库存一致性
