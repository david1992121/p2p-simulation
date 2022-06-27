from fastapi import APIRouter, HTTPException, Response
from network.crud import P2PNetwork
from ..schemas import JoinInfo, LeaveInfo

router = APIRouter()
network = P2PNetwork()


@router.post("/join")
async def join(capacity_info: JoinInfo):
    '''
    Add a new node into the network.
    The capacity of the node is required.

    In this step, the network just assigns the node to the best-fitting parent (the node with the most free capacity).

    '''
    network.join(capacity_info.capacity)
    return Response(status_code=200)


@router.post("/leave")
async def leave(leave_info: LeaveInfo):
    '''
    Remove the node from the network.
    The node to be removed can be specified using it's identifier.

    In this case, we want to reorder the current node tree (not all the network) to build the solution
    where the tree has the fewest number of depth levels.

    '''
    if network.leave(leave_info.id):
        return Response(status_code=200)
    raise HTTPException(status_code=400, detail="Node not found")


@router.get("/status")
async def get_network():
    '''
    Get the current topology of the network.

    The result has the list of the information for each tree.
    Each tree information has the list of the nodes with capacities and the edges.

    '''
    info = network.info()
    return info
