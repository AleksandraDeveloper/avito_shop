from sqlalchemy.orm import Session
from ..models import Item
from ..database import SessionLocal

def init_db() -> None:
    db = SessionLocal()
    init_items(db)
    db.close()

def init_items(db: Session) -> None:
    if not db.query(Item).first():
        items = [
            Item(name="t-shirt", price=80),
            Item(name="cup", price=20),
            Item(name="book", price=50),
            Item(name="pen", price=10),
            Item(name="powerbank", price=200),
            Item(name="hoody", price=300),
            Item(name="umbrella", price=200),
            Item(name="socks", price=10),
            Item(name="wallet", price=50),
            Item(name="pink-hoody", price=500)
        ]
        db.add_all(items)
        db.commit() 