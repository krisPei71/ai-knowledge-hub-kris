# backend/seed.py
"""
种子脚本：插入测试账号。
用法：cd backend && python seed.py
"""
from app.database import SessionLocal, Base, engine
from app.models.user import User
from app.security import get_hash_password as hash_password


# 测试账号：用户名 / 密码 / 角色
SEED_USERS = [
    ("admin",    "admin123",    "admin"),     # 管理员
    ("agent",    "agent123",    "handler"),   # 处理人（IT/客服）
    ("employee", "employee123", "reporter"),  # 提交人（普通员工）
]


def main():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        for username, password, role in SEED_USERS:
            # 已存在就跳过
            exists = db.query(User).filter(User.username == username).first()
            if exists:
                print(f"⏭️  用户 {username} 已存在，跳过")
                continue

            user = User(
                username=username,
                password_hash=hash_password(password),
                role=role,
            )
            db.add(user)
            print(f"✅ 创建用户：{username} / {password}（{role}）")

        db.commit()
        print("\n🎉 种子数据插入完成")
        print("\n测试账号：")
        for u, p, r in SEED_USERS:
            print(f"  {u:10s} / {p:12s}  ({r})")
    except Exception as e:
        db.rollback()
        print(f"❌ 出错：{e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()