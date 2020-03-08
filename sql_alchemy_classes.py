from sqlalchemy import Column, String, VARCHAR, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import INTEGER

import declarative_base_class


class Author(declarative_base_class.base):
    __tablename__ = 'author'
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    _name = Column(VARCHAR(255), nullable=False)
    books = relationship("Book")


class Book(declarative_base_class.base):
    __tablename__ = 'book'
    id = Column(INTEGER(unsigned=True), primary_key=True, nullable=False, unique=True, autoincrement=True)
    _isbn = Column(VARCHAR(255), nullable=False, unique=True)
    _title = Column(String(60), nullable=False)
    _price = Column(INTEGER, nullable=False)
    author_id = Column(INTEGER, ForeignKey(Author.id, ondelete='CASCADE', onupdate='CASCADE'))
    author = relationship("Author")

    @property
    def isbn(self):
        return self._isbn

    @isbn.setter
    def isbn(self, val):
        self._isbn = val

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, val):
        self._title = val

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, val):
        self._price = val
