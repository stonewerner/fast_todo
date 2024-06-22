from sqlalchemy import Boolean, Column, Integer, String
from database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    description = Column(String)
    read = Column(Boolean, default=False)

# would add schemas here?