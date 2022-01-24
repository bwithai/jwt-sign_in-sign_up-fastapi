from fastapi import APIRouter

store_router = APIRouter(prefix="/store", tags=['Store'])


@store_router.get("")
def index():
    return {"all": "stores"}
