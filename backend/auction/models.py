from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, func
from sqlalchemy.orm import relationship

from database.connection import Base


class RoomUser(Base):
    __tablename__ = "rooms_users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(Integer, ForeignKey("users.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"))

    member = relationship("User", back_populates="room", foreign_keys=[member_id])
    room = relationship("Room", back_populates="member", foreign_keys=[room_id])


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, autoincrement=True)
    max_members = Column(Integer)

    member = relationship("RoomUser", back_populates="room")
    lot = relationship("Lot", back_populates="room")


class Lot(Base):
    __tablename__ = "lots"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
    start_price = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=func.current_timestamp())
    owner_id = Column(Integer, ForeignKey("users.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"))

    owner = relationship("User", back_populates="lot", foreign_keys=[owner_id])
    room = relationship("Room", back_populates="lot", foreign_keys=[room_id])


class Bid(Base):
    __tablename__ = "bids"

    id = Column(Integer, primary_key=True, autoincrement=True)
    bid = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    lot_id = Column(Integer, ForeignKey("lots.id"))

    lot = relationship("Lot", foreign_keys=[lot_id])
    user = relationship("User", back_populates="bid", foreign_keys=[user_id])
