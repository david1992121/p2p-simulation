from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_network():
    return "network app created!"
