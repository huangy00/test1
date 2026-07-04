# Python学习计划 - 测试工程师方向

## 学习目标

掌握Python基础，能独立编写自动化测试脚本。

## 时间安排

5周，每天1-2小时。

---

## 第1周：基础语法

### Day 1-2：变量和数据类型
```python
# 你需要掌握的内容
name = "张三"           # 字符串
age = 25               # 整数
price = 99.9           # 浮点数
is_vip = True          # 布尔值
```

**练习：** 写一个程序，定义5个变量并打印出来。

### Day 3-4：条件判断
```python
# if-elif-else
score = 85
if score >= 90:
    print("优秀")
elif score >= 60:
    print("及格")
else:
    print("不及格")
```

**练习：** 写一个程序，根据用户输入的成绩给出评语。

### Day 5-7：循环
```python
# for循环
for i in range(5):
    print(i)

# while循环
count = 0
while count < 5:
    print(count)
    count += 1
```

**练习：** 写一个程序，打印九九乘法表。

---

## 第2周：数据结构

### Day 1-2：列表（List）
```python
# 列表 = 可以存多个值
fruits = ["苹果", "香蕉", "橘子"]
fruits.append("西瓜")    # 添加
fruits.remove("香蕉")    # 删除
print(fruits[0])         # 取第一个
```

**练习：** 写一个程序，存储5个学生的成绩，计算平均分。

### Day 3-4：字典（Dict）
```python
# 字典 = 键值对
user = {
    "name": "张三",
    "age": 25,
    "email": "zhangsan@test.com"
}
print(user["name"])      # 取值
user["phone"] = "13800"  # 添加
```

**练习：** 写一个程序，存储3个商品的信息（名称、价格、库存）。

### Day 5-7：列表和字典嵌套
```python
# 嵌套 = 列表里套字典
users = [
    {"name": "张三", "age": 25},
    {"name": "李四", "age": 30}
]
for user in users:
    print(user["name"])
```

**练习：** 写一个程序，存储5个用户的信息，按年龄排序。

---

## 第3周：函数和类

### Day 1-3：函数
```python
# 定义函数
def greet(name):
    print(f"你好，{name}")

# 调用函数
greet("张三")

# 返回值
def add(a, b):
    return a + b

result = add(3, 5)
print(result)  # 8
```

**练习：** 写一个函数，计算商品总价（数量x单价）。

### Day 4-7：类和对象
```python
# 定义类
class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def bark(self):
        print(f"{self.name}在叫")

# 创建对象
dog = Dog("旺财", 3)
dog.bark()
```

**练习：** 写一个Student类，包含姓名、成绩属性，以及计算平均分的方法。

---

## 第4周：文件和异常

### Day 1-3：文件操作
```python
# 写文件
with open("data.txt", "w") as f:
    f.write("Hello World")

# 读文件
with open("data.txt", "r") as f:
    content = f.read()
    print(content)

# 读JSON
import json
with open("data.json", "r") as f:
    data = json.load(f)
```

**练习：** 写一个程序，把用户信息保存到JSON文件。

### Day 4-7：异常处理
```python
# try-except
try:
    result = 10 / 0
except ZeroDivisionError:
    print("不能除以0")
finally:
    print("无论如何都会执行")
```

**练习：** 写一个函数，安全地读取文件，文件不存在时返回空内容。

---

## 第5周：实战练习

### Day 1-2：HTTP请求
```python
import requests

# GET请求
response = requests.get("http://localhost/opencart")
print(response.status_code)

# POST请求
data = {"username": "admin", "password": "123456"}
response = requests.post("http://localhost/opencart/login", data=data)
```

**练习：** 用requests调用OpenCart的登录接口。

### Day 3-4：数据库操作
```python
import pymysql

# 连接数据库
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="root123456",
    database="xiangmu"
)

# 查询
cursor = conn.cursor()
cursor.execute("SELECT * FROM oc_customer")
results = cursor.fetchall()
for row in results:
    print(row)

conn.close()
```

**练习：** 查询OpenCart数据库里的用户数量。

### Day 5-7：综合练习
**项目：** 写一个接口自动化测试脚本，测试OpenCart的登录接口。

```python
import requests

def test_login():
    url = "http://localhost/opencart/index.php?route=account/login.login"
    data = {"email": "test@test.com", "password": "123456"}
    response = requests.post(url, data=data)
    assert response.status_code == 200
    print("测试通过")

test_login()
```

---

## 每周检查点

| 周 | 检查标准 |
|---|---------|
| 第1周 | 能独立写条件判断和循环程序 |
| 第2周 | 能熟练使用列表和字典 |
| 第3周 | 能定义函数和类 |
| 第4周 | 能读写文件和处理异常 |
| 第5周 | 能写接口测试脚本 |

---

## 学习资源

| 资源 | 用途 |
|------|------|
| 菜鸟教程 | 查语法 |
| B站搜"Python基础" | 看视频 |
| LeetCode简单题 | 练算法 |
| 这个项目里的代码 | 实战参考 |
