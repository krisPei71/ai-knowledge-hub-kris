import requests

BASE = "http://localhost:8080"

# 1. 登录
r = requests.post(f"{BASE}/api/auth/login", json={"username": "admin", "password": "admin123"})
token = r.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# 2. 创建知识
docs = [
    ("VPN连接失败排查指南", "检查网络连接。清除VPN缓存。若提示认证失败，请联系IT检查账号是否被锁。"),
    ("打印机常见问题", "打印机没墨了请找行政部换硒鼓。如果是卡纸，请打开后盖取出纸张。"),
    ("忘记密码怎么办", "如果您忘记了公司账号密码，请在OA系统点击找回密码，或拨打IT分机 8888 进行重置。"),
]

print("--- 创建知识 ---")
for title, content in docs:
    r = requests.post(f"{BASE}/api/knowledge", json={"title": title, "content": content}, headers=headers)
    if r.status_code == 200:
        print(f"✅ 创建成功: {title}")
    else:
        print(f"❌ 创建失败: {r.text}")

# 3. 测试语义搜索
print("\n--- 测试语义搜索 ---")
queries = [
    "连不上公司的内网怎么弄",  # 应该匹配 VPN
    "硒鼓在哪里换",            # 应该匹配 打印机
    "账号被锁了"               # 应该匹配 VPN 或 密码
]

for q in queries:
    print(f"\n🔍 搜索: {q}")
    r = requests.post(f"{BASE}/api/knowledge/search", json={"query": q, "top_k": 2}, headers=headers)
    results = r.json()
    print(results,9999)
    if not results:
        print("  (无匹配结果)")
    for res in results:
        print(f"  -> [{res['score']:.3f}] {res['title']}")