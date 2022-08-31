import datetime

from pydantic import BaseModel


class BaseRoomSchema(BaseModel):
    max_members: int = 5


class GetRoomSchema(BaseRoomSchema):
    pass


class CreateRoomSchema(BaseRoomSchema):
    pass


class BaseLotSchema(BaseModel):
    name: str
    description: str
    start_price: int


class GetLotSchema(BaseLotSchema):
    id: int
    owner_id: int
    room_id: int
    created_at: datetime.datetime
    edited_at: datetime.datetime


class CreateLotSchema(BaseLotSchema):
    pass


class BaseBidSchema(BaseModel):
    bid: int


class GetBidSchema(BaseBidSchema):
    id: int
    user_id: int
    lot_id: int


class CreateBidSchema(BaseBidSchema):
    pass
