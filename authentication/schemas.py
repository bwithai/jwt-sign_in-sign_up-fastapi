from pydantic import BaseModel


class RegisterUserSchema(BaseModel):
    email: str
    username: str
    password: str


class LoginUserSchema(BaseModel):
    username: str
    password: str
