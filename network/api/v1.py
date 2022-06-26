from fastapi import APIRouter, HTTPException, Response
from network.crud import P2PNetwork
from ..schemas import JoinInfo, LeaveInfo

router = APIRouter()
network = P2PNetwork()


@router.get("/status")
async def get_network():
    info = network.info()
    return info


@router.post("/join")
async def join(capacity_info: JoinInfo):
    network.join(capacity_info.capacity)
    return Response(status_code=200)


@router.post("/leave")
async def leave(leave_info: LeaveInfo):
    if network.leave(leave_info.id):
        return Response(status_code=200)
    raise HTTPException(status_code=400, detail="Node not found")
