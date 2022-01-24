import time

import jwt
from fastapi import FastAPI
from passlib.context import CryptContext
from sqlmodel import select, Session
from starlette.middleware.cors import CORSMiddleware

from authentication.database import engine, User
from authentication.schemas import LoginUserSchema, RegisterUserSchema

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET = "MOBILEACCESSORIESSECRETKEY!"
pswd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@app.post('/register', tags=['Authentication'])
def register(data: RegisterUserSchema):
    pswd_hashed = pswd_context.hash(data.password)

    session = Session(engine)

    # statement = select(User).where(User.user_name == data.username)
    # our_user = session.exec(statement).first()

    our_user = session.query(User).filter_by(user_name=data.username).first()

    end_user = User(user_name=data.username, email=data.email, hash_password=pswd_hashed)

    if not our_user:
        session.add(end_user)
        session.commit()
        session.close()

        return {
            "massage": "Well come",
            "status": "Registration done successfully"
        }

    if (end_user.user_name == our_user.user_name) or (end_user.email == our_user.email):
        return {
            "massage": "email or user_name already exist",
            "status": "Not registered"
        }


@app.post('/login', tags=['Authentication'])
def login(data: LoginUserSchema):
    check_username = select(User).where(User.user_name == data.username)

    print(check_username)

    session = Session(engine)

    end_user = session.exec(check_username).first()

    if not end_user:
        return {
            "message": "Login failed",
            "status_code": 401
        }

    if pswd_context.verify(data.password, end_user.hash_password):
        expire_time = int(time.time() + 3600)
        token = jwt.encode({"exp": expire_time}, SECRET, algorithm="HS256")
        return {
            "message": "You Login Successfuly",
            "status_code": 200,
            "session_token": token
        }
    else:
        return {
            "message": "Login failed",
            "status_code": 401
        }
