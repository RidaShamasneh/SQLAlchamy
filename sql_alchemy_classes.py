from sqlalchemy import Column, String, Integer, VARCHAR, ForeignKey
from sqlalchemy.orm import relationship

import declarative_base_class


class Author(declarative_base_class.base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(255), nullable=False)
    books = relationship("Book")


class Book(declarative_base_class.base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True, autoincrement=True)
    isbn = Column(VARCHAR(255), nullable=False, unique=True)
    title = Column(String(60), nullable=False)
    price = Column(Integer, nullable=False)
    author_id = Column(Integer, ForeignKey(Author.id, ondelete='CASCADE', onupdate='CASCADE'))
    author = relationship("Author")
