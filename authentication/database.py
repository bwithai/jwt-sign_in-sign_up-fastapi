from typing import Optional

from sqlalchemy import UniqueConstraint
from sqlmodel import create_engine, Field, SQLModel


# Models ----------------------
class User(SQLModel, table=True):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint('email'), UniqueConstraint('user_name'),)
    id: Optional[int] = Field(default=None, primary_key=True, )
    user_name: str
    email: str
    hash_password: str


engine = create_engine("mysql+mysqldb://syed:syedfurqan@localhost:3306/mobile_accessories", echo=True)

SQLModel.metadata.create_all(engine)
