from sqlalchemy import Column, String, VARCHAR, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import INTEGER

import declarative_base_class


class Author(declarative_base_class.base):
    __tablename__ = 'author'
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    _name = Column(VARCHAR(255), nullable=False)

    # 'lazy' : selectin - items should be loaded 'eagerly' as the parents are loaded, using one or more additional
    # SQL statements, which issues a JOIN to the immediate parent object, specifying primary key identifiers using an IN clause.
    # https://docs.sqlalchemy.org/en/13/orm/relationship_api.html?highlight=relationship#sqlalchemy.orm.relationship
    books = relationship("Book", lazy='selectin')

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name = val


class Book(declarative_base_class.base):
    __tablename__ = 'book'
    id = Column(INTEGER(unsigned=True), primary_key=True, nullable=False, unique=True, autoincrement=True)
    _isbn = Column(VARCHAR(255), nullable=False, unique=True)
    _title = Column(String(60), nullable=False)
    _price = Column(INTEGER, nullable=False)
    author_id = Column(INTEGER, ForeignKey(Author.id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    author = relationship("Author", lazy='selectin')
    _author_marking = ''

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

    @property
    def author_marking(self):
        return self.author.name

    @author_marking.setter
    def author_marking(self, val):
        if val is not None:
            self._author_marking = str(val)
            self.author = None
            self.__set_author_fkey()
        else:
            self._author_marking = None
            self.author_id = None
            self.author = None

    def __set_author_fkey(self):
        if self._author_marking is not '' and self._author_marking is not None:
            # todo: needs refactoring on how to set the id
            from mysql_connection_manager import MysqlConnectionManager
            manager = MysqlConnectionManager.getInstance()
            result = manager.session.query(Author).filter(Author._name == self._author_marking).first()
            manager.session.close()
            if result is not None:
                self.author_id = result.id
                return
            raise Exception("{} in table {} is Not Found as primary key".format(self._author_marking, 'Primary'))
