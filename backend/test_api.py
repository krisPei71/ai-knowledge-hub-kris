# test_api.py
import requests

BASE = "http://localhost:8080"

# 1. 登录
r = requests.post(f"{BASE}/api/auth/login", json={
    "username": "employee",
    "password": "employee123",
})
token = r.json()["access_token"]
print("token:", token[:30], "...")

headers = {"Authorization": f"Bearer {token}"}

# 2. 创建工单
r = requests.post(f"{BASE}/api/tickets", json={
    "title": "测试工单",
    "description": "用于测试状态流转",
}, headers=headers)
ticket = r.json()
ticket_id = ticket["id"]
print(f"创建工单 id={ticket_id}, status={ticket['status']}")

# 3. agent 登录
r = requests.post(f"{BASE}/api/auth/login", json={
    "username": "agent",
    "password": "agent123",
})
agent_token = r.json()["access_token"]
agent_headers = {"Authorization": f"Bearer {agent_token}"}

# 4. agent 认领
r = requests.patch(
    f"{BASE}/api/tickets/{ticket_id}/status",
    json={"to_status": "processing", "remark": "我来处理"},
    headers=agent_headers,
)
print(f"认领结果：{r.status_code}, status={r.json().get('status')}")

# 5. agent 解决
r = requests.patch(
    f"{BASE}/api/tickets/{ticket_id}/status",
    json={"to_status": "resolved", "remark": "已修复"},
    headers=agent_headers,
)
print(f"解决结果：{r.status_code}, status={r.json().get('status')}")

# 6. employee 打回（remark 必填，测试漏填）
r = requests.patch(
    f"{BASE}/api/tickets/{ticket_id}/status",
    json={"to_status": "processing"},
    headers=headers,
)
print(f"打回不填 remark：{r.status_code}, detail={r.json().get('detail')}")

# 7. employee 打回（带上 remark）
r = requests.patch(
    f"{BASE}/api/tickets/{ticket_id}/status",
    json={"to_status": "processing", "remark": "问题还在"},
    headers=headers,
)
print(f"打回：{r.status_code}, status={r.json().get('status')}")

# 8. 查日志
r = requests.get(f"{BASE}/api/tickets/{ticket_id}/logs", headers=headers)
logs = r.json()
print(f"\n日志 {len(logs)} 条：")
for log in logs:
    print(f"  {log['from_status'] or '(空)'} → {log['to_status']}  by {log['operator_username']}  ({log['remark']})")