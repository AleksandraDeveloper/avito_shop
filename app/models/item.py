from sqlalchemy import Column, Integer, String, CheckConstraint
from sqlalchemy.orm import relationship
from ..database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    price = Column(Integer, nullable=False)
    
    purchases = relationship("Purchase", back_populates="item")
    __table_args__ = (
        CheckConstraint('price > 0', name='check_price_positive'),
    )