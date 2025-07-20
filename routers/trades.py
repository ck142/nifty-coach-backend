
from fastapi import APIRouter
from services.dhan import fetch_trades
from db import SessionLocal, Trade
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter()

@router.post("/sync_trades")
def sync_trades():
    try:
        trades = fetch_trades()
        print("Dhan response JSON:", response.json())
        db = SessionLocal()
        new_trades = 0
        for trade in trades:
            exists = db.query(Trade).filter_by(order_id=trade["order_id"]).first()
            if not exists:
                db.add(Trade(**trade))
                new_trades += 1
        db.commit()
        db.close()
        return {"message": f"Synced {new_trades} new trades."}
    except SQLAlchemyError as e:
        return {"error": f"Database error: {str(e)}"}
    except Exception as e:
        return {"error": f"General error: {str(e)}"}
