
from models import Trade
from sqlalchemy.orm import Session
from db_setup import SessionLocal

def save_trade_to_db(trade_data: dict) -> bool:
    session: Session = SessionLocal()
    try:
        existing = session.query(Trade).filter_by(order_id=trade_data["order_id"]).first()
        if existing:
            return False

        new_trade = Trade(
            order_id=trade_data["order_id"],
            symbol=trade_data["symbol"],
            side=trade_data["side"],
            qty=trade_data["qty"],
            price=trade_data["price"],
            timestamp=trade_data["timestamp"]
        )
        session.add(new_trade)
        session.commit()
        return True
    except Exception as e:
        print(f"[ERROR] DB insert failed: {e}")
        session.rollback()
        return False
    finally:
        session.close()
