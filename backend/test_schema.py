# test_schema.py
from datetime import datetime

from app.database import SessionLocal, Base, engine
from app import models
from app.models.user import User
from app.models.ticket import Ticket
from app.models.ticket_log import TicketLog
from app.schemas.user import UserOut
from app.schemas.tickets import TicketOut, TicketList


def cleanup(db):
    """清理测试数据（注意外键顺序：先子后父）"""
    db.query(TicketLog).delete()
    db.query(Ticket).delete()
    db.query(User).filter(User.username.in_(["test_user", "test_handler"])).delete(
        synchronize_session=False
    )
    db.commit()


def main():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # ---------- 1. 先清理 ----------
        cleanup(db)

        # ---------- 2. 建测试数据 ----------
        creator = User(username="test_user", password_hash="fake_hash", role="reporter")
        handler = User(username="test_handler", password_hash="fake_hash", role="handler")
        db.add_all([creator, handler])
        db.commit()
        db.refresh(creator)
        db.refresh(handler)

        ticket = Ticket(
            title="VPN连不上",
            description="今天早上来公司，VPN一直连不上，提示认证失败。",
            status="pending",
            priority="high",
            category="网络",
            ai_summary="员工VPN认证失败，影响客户会议",
            ai_confidence=0.94,
            creator_id=creator.id,
            assignee_id=None,
        )
        db.add(ticket)
        db.commit()
        db.refresh(ticket)

        print(f"✅ 测试数据插入完成：ticket.id={ticket.id}")

        # ---------- 3. UserOut ----------
        print("\n=== UserOut ===")
        print(UserOut.model_validate(creator).model_dump_json(indent=2))

        # ---------- 4. TicketOut ----------
        print("\n=== TicketOut ===")
        ticket_out = TicketOut(
            **{k: v for k, v in ticket.__dict__.items() if not k.startswith("_")},
            creator_username=creator.username,
            assignee_username=None,
        )
        print(ticket_out.model_dump_json(indent=2))

        # ---------- 5. TicketList ----------
        print("\n=== TicketList ===")
        print(TicketList(total=1, items=[ticket_out]).model_dump_json(indent=2))

    except Exception as e:
        db.rollback()
        print(f"\n❌ 出错：{type(e).__name__}: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()