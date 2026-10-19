import requests
import json

BASE = "http://localhost:8080"

# 1. 登录
r = requests.post(f"{BASE}/api/auth/login", json={
    "username": "employee", "password": "employee123",
})
token = r.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# 2. 测试 AI 分类
test_cases = [
    ("VPN连不上", "今天早上来公司，VPN一直连不上，提示认证失败。急！"),
    ("打印机没墨", "行政部打印机没墨了，有空来换一下"),
    ("忘记密码", "我的账号密码忘记了，登录不了"),
    ("随便说点什么", "就是随便写写，没什么问题"),
]

for title, desc in test_cases:
    print(f"\n{'='*60}")
    print(f"输入：{title} | {desc}")
    r = requests.post(
        f"{BASE}/api/ai/classify",
        json={"title": title, "description": desc},
        headers=headers,
    )
    print(f"HTTP {r.status_code}")
    result = r.json()
    print(f"  分类：{result['category']}")
    print(f"  优先级：{result['priority']}")
    print(f"  置信度：{result['confidence']}")
    print(f"  摘要：{result['summary']}")


# 3. 测试未登录
print(f"\n{'='*60}")
print("未登录调用（应 401）")
r = requests.post(
    f"{BASE}/api/ai/classify",
    json={"title": "test", "description": "test"},
)
print(f"HTTP {r.status_code}")


# 4. 测试空标题（应 422）
print(f"\n{'='*60}")
print("空标题（应 422）")
r = requests.post(
    f"{BASE}/api/ai/classify",
    json={"title": "", "description": "test"},
    headers=headers,
)
print(f"HTTP {r.status_code}")