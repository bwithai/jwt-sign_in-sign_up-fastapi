from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.auth import auth_router
from api.store import store_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(store_router)
