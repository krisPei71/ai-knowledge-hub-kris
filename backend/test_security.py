# test_security.py
"""
验证 security.py 的哈希和 JWT 功能。
"""
from app.security import (
    get_hash_password,
    verify_hash_password,
    create_access_token,
    decode_token,
)


def main():
    # ---------- 1. 密码哈希 ----------
    print("=== 1. 密码哈希测试 ===")
    password = "my_secret_123"
    hashed = get_hash_password(password)
    print(f"原密码：{password}")
    print(f"哈希后：{hashed}")

    # 校验正确密码
    assert verify_hash_password(password, hashed) is True, "正确密码校验失败"
    print("✅ 正确密码校验通过")

    # 校验错误密码
    assert verify_hash_password("wrong_password", hashed) is False, "错误密码应该校验失败"
    print("✅ 错误密码校验被正确拒绝")

    # 相同密码两次哈希结果不同（加盐）
    hashed2 = get_hash_password(password)
    assert hashed != hashed2, "加盐应该让两次哈希不同"
    print("✅ 加盐生效：两次哈希结果不同")

    # ---------- 2. JWT ----------
    print("\n=== 2. JWT 测试 ===")
    token = create_access_token(user_id=5, role="handler")
    print(f"生成的 token：{token[:60]}...")

    # 解析
    payload = decode_token(token)
    assert payload is not None, "token 解析失败"
    print(f"解析出的 payload：{payload}")
    assert payload["sub"] == "5", "user_id 不对"
    assert payload["role"] == "handler", "role 不对"
    print("✅ payload 还原正确")

    # ---------- 3. 非法 token ----------
    print("\n=== 3. 非法 token 测试 ===")
    assert decode_token("this.is.not.a.token") is None, "非法 token 应返回 None"
    print("✅ 非法 token 被拒绝")

    # 篡改 token
    tampered = token[:-5] + "xxxxx"
    assert decode_token(tampered) is None, "篡改 token 应返回 None"
    print("✅ 篡改 token 被拒绝")

    print("\n🎉 全部通过！")


if __name__ == "__main__":
    main()