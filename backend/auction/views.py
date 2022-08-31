from auction.schemas import CreateBidSchema, CreateLotSchema, CreateRoomSchema
from database.connection import get_db
from fastapi import APIRouter, Depends
from sqlalchemy import delete
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse
from user.authentication_logic import get_current_user
from auction.models import Bid, Lot, Room, RoomUser
from user.schemas import ErrorMessage, GetUserWithIdSchema, SuccessMessage
from user.utils import save_model, set_model_attrs

router = APIRouter(prefix="/auction", tags=["auction"])


@router.post(
    "/room/create",
    responses={201: {"model": SuccessMessage}, 400: {"model": ErrorMessage}},
)
def create_room(
    room_schema: CreateRoomSchema,
    db: Session = Depends(get_db),
    this_user: GetUserWithIdSchema = Depends(get_current_user),
):
    room = Room()
    set_model_attrs(model=room, schema=room_schema, meta=None)
    save_model(room, db)

    room_user = RoomUser()
    set_model_attrs(
        model=room_user,
        schema=None,
        meta={"member_id": this_user.id, "room_id": room.id},
    )
    save_model(room_user, db)
    return JSONResponse(
        {"message": "room created", "success": True},
        status_code=status.HTTP_201_CREATED,
    )


@router.post(
    "/room/enter/{id}",
    responses={
        status.HTTP_200_OK: {"model": SuccessMessage},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorMessage},
    },
)
def enter_room(
    id: int,
    db: Session = Depends(get_db),
    this_user: GetUserWithIdSchema = Depends(get_current_user),
):
    if (
        not db.query(RoomUser)
        .filter(RoomUser.room_id == id, RoomUser.member_id == this_user.id)
        .first()
    ):
        max_members = db.query(Room).filter(Room.id == id).first().max_members
        room_with_members = db.query(RoomUser).filter(RoomUser.room_id == id)
        members_in_room = room_with_members.count()
        if max_members <= members_in_room:
            return JSONResponse(
                {"message": "there is no room in the room", "success": False},
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        room = RoomUser()
        set_model_attrs(
            model=room, schema=None, meta={"member_id": this_user.id, "room_id": id}
        )
        save_model(room, db)
        return JSONResponse(
            {"message": "success", "success": True}, status_code=status.HTTP_200_OK
        )
    return JSONResponse(
        {"message": "you are already in this room", "success": False},
        status_code=status.HTTP_400_BAD_REQUEST,
    )


@router.post(
    "/room/leave/{id}",
    responses={
        status.HTTP_200_OK: {"model": SuccessMessage},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorMessage},
    },
)
def leave_room(
    id: int,
    db: Session = Depends(get_db),
    this_user: GetUserWithIdSchema = Depends(get_current_user),
):
    if (
        db.query(RoomUser)
        .filter(RoomUser.room_id == id, RoomUser.member_id == this_user.id)
        .first()
    ):
        dl = delete(RoomUser).where(
            RoomUser.room_id == id, RoomUser.member_id == this_user.id
        )
        db.execute(dl)
        db.commit()

        return JSONResponse(
            {"message": "you left the room", "success": True},
            status_code=status.HTTP_200_OK,
        )
    return JSONResponse(
        {"message": "you are not in this room", "success": False},
        status_code=status.HTTP_400_BAD_REQUEST,
    )


@router.post(
    "/room/{id}/lot/create",
    responses={
        status.HTTP_200_OK: {"model": SuccessMessage},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorMessage},
    },
)
def create_lot(
    id: int,
    lot_schema: CreateLotSchema,
    db: Session = Depends(get_db),
    this_user: GetUserWithIdSchema = Depends(get_current_user),
):
    if (
        db.query(Room).filter(Room.id == id).first()
        and db.query(RoomUser)
        .filter(RoomUser.room_id == id, RoomUser.member_id == this_user.id)
        .first()
    ):
        lot = Lot()
        set_model_attrs(
            model=lot, schema=lot_schema, meta={"room_id": id, "owner_id": this_user.id}
        )
        save_model(lot, db)
        return JSONResponse(
            {"message": "lot created", "success": True}, status_code=status.HTTP_200_OK
        )
    return JSONResponse(
        {"message": "room does not exists", "success": False},
        status_code=status.HTTP_400_BAD_REQUEST,
    )


@router.post(
    "/room/{room_id}/lot/{lot_id}/bid",
    responses={
        status.HTTP_200_OK: {"model": SuccessMessage},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorMessage},
    },
)
def place_bid(
    room_id: int,
    lot_id: int,
    bid_schema: CreateBidSchema,
    db: Session = Depends(get_db),
    this_user: GetUserWithIdSchema = Depends(get_current_user),
):
    if (
        db.query(RoomUser)
        .filter(RoomUser.room_id == room_id, RoomUser.member_id == this_user.id)
        .first()
    ):
        lot = db.query(Lot).filter(Lot.id == lot_id).first()
        if lot:
            last_bet = (
                db.query(Bid)
                .filter(Bid.lot_id == lot_id)
                .order_by(Bid.id.desc())
                .first()
            )
            if last_bet:
                if bid_schema.bid > last_bet.bid:
                    dl = delete(Bid).where(Bid.id == last_bet.id)
                    bid = Bid()
                    set_model_attrs(
                        model=bid,
                        schema=bid_schema,
                        meta={"lot_id": lot_id, "user_id": this_user.id},
                    )
                    db.execute(dl)
                    save_model(bid, db)
                    return JSONResponse(
                        {"message": "the bet is made", "success": True},
                        status_code=status.HTTP_200_OK,
                    )
                return JSONResponse(
                    {
                        "message": "the bid must be greater than the last bid",
                        "success": False,
                    },
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
            else:
                if bid_schema.bid > lot.start_price:
                    bid = Bid()
                    set_model_attrs(
                        model=bid,
                        schema=bid_schema,
                        meta={"lot_id": lot_id, "user_id": this_user.id},
                    )
                    save_model(bid, db)
                    return JSONResponse(
                        {"message": "the bet is made", "success": True},
                        status_code=status.HTTP_200_OK,
                    )
                return JSONResponse(
                    {
                        "message": "the bid must be greater than the starting price",
                        "success": True,
                    },
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
        return JSONResponse(
            {"message": "lot does not exists", "success": False},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    return JSONResponse(
        {"message": "room does not exists", "success": False},
        status_code=status.HTTP_400_BAD_REQUEST,
    )
