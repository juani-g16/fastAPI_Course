from time import timezone
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base


# the class Post defines the model our table is going to have
class Post(Base):
    __tablename__ = "posts"  # we must give a name to the table
    id = Column(Integer, primary_key=True, nullable=False)
    content = Column(String, nullable=False)
    title = Column(String, nullable=False)
    published = Column(Boolean, default=True, server_default="TRUE")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
