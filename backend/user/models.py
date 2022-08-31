from database.connection import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=True, unique=True)
    name = Column(String(30), nullable=False)
    last_name = Column(String(35), nullable=False)
    patronymic = Column(String(35), nullable=True)
    balance = Column(Integer, default=0)
    email = Column(String, unique=True)
    password = Column(String(50))

    room = relationship("RoomUser", back_populates="member")
    lot = relationship("Lot", back_populates="owner")
    bid = relationship("Bid", back_populates="user")
