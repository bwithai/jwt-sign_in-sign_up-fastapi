import time

import jwt
from fastapi import APIRouter
from passlib.context import CryptContext

from database import get_db_session
from models import User
from schemas.users import LoginUserSchema, RegisterUserSchema

auth_router = APIRouter(prefix="", tags=['Authentication'])
SECRET = "MOBILEACCESSORIESSECRETKEY!"
pswd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@auth_router.post('/register')
def register(data: RegisterUserSchema):
    pswd_hashed = pswd_context.hash(data.password)

    with get_db_session() as db_session:
        existing_user = db_session.query(User).filter_by(user_name=data.username).first()

        if existing_user:
            return {
                "massage": "email or user_name already exist",
                "status": "Not registered"
            }

        user = User(user_name=data.username, email=data.email, hash_password=pswd_hashed)

        db_session.add(user)
        db_session.commit()
        return {
            "massage": "Well come",
            "status": "Registration done successfully"
        }


@auth_router.post('/login')
def login(data: LoginUserSchema):
    with get_db_session() as db_session:
        existing_user = db_session.query(User).filter_by(user_name=data.username).first()
        if not existing_user:
            return {
                "message": "Login failed",
                "status_code": 401
            }

        if pswd_context.verify(data.password, existing_user.hash_password):
            expire_time = int(time.time() + 3600)
            token = jwt.encode({"exp": expire_time}, SECRET, algorithm="HS256")
            return {
                "message": "You Login Successfully",
                "status_code": 200,
                "session_token": token
            }
        else:
            return {
                "message": "Login failed",
                "status_code": 401
            }
