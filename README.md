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
├── setup.py                 # 一键初始化脚本
├── conftest.py              # Pytest Fixture
├── pytest.ini               # Pytest 配置
├── requirements.txt         # Python 依赖
└── README.md                # 项目说明
```

## 环境要求

- Python 3.10+
- XAMPP（Apache + MySQL）
- OpenCart 4.x

## 快速开始

### 第一步：安装 XAMPP 并启动服务

1. 下载安装 [XAMPP](https://www.apachefriends.org/)
2. 启动 Apache 和 MySQL
3. 下载 [OpenCart 4.x](https://github.com/opencart/opencart/releases)
4. 将 `upload` 目录复制到 `C:\xampp\htdocs\opencart`
5. 浏览器访问 `http://localhost/opencart`，完成安装向导
   - 数据库名：`xiangmu`
   - 数据库用户：`root`
   - 数据库密码：`root123456`

### 第二步：一键初始化

```bash
git clone https://github.com/huangy00/test1.git
cd test1
python setup.py
```

setup.py 会自动完成：
- 创建 `xiangmu` 数据库
- 创建虚拟环境并安装 Python 依赖
- 安装 Playwright Chromium 浏览器
- 安装 OpenCart 支付扩展

### 第三步：运行测试

```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# 运行所有测试
pytest

# 仅运行 UI 测试
pytest tests/test_ui/

# 仅运行数据库测试
pytest tests/test_db/
```

### 第四步：查看 Allure 报告

```bash
allure serve allure-results
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
