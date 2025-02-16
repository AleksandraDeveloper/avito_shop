from sqlalchemy import Column, Integer, String, CheckConstraint
from sqlalchemy.orm import relationship
from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    coins = Column(Integer, default=1000, nullable=False)

    sent_transactions = relationship("Transaction", foreign_keys="Transaction.from_user_id", back_populates="from_user")
    received_transactions = relationship("Transaction", foreign_keys="Transaction.to_user_id", back_populates="to_user")
    purchases = relationship("Purchase", back_populates="user")

    __table_args__ = (
        CheckConstraint('coins >= 0', name='check_coins_non_negative'),
    )