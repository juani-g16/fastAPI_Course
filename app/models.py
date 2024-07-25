from enum import unique
from time import timezone
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base


# the class Post defines the model our posts table is going to have
class Post(Base):
    __tablename__ = "posts"  # we must give a name to the table
    id = Column(Integer, primary_key=True, nullable=False)
    content = Column(String, nullable=False)
    title = Column(String, nullable=False)
    published = Column(Boolean, default=True, server_default="TRUE")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    owner_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    owner = relationship("User")

# the class User defines the model our users table is going to have
class User(Base):
    __tablename__ = "users"
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
