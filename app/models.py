from .database import Base
from sqlalchemy import Column, Integer, String , Boolean  , ForeignKey  # type: ignore
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__="posts"

    id = Column(Integer, primary_key = True , nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published = Column(Boolean, server_default = "True" , nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable = False)
    owner = relationship("User")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(255), nullable=False, unique=True)  # Specify the length of the string
    password = Column(String(255), nullable=False)  # Specify the length of the string
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
