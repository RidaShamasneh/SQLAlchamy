from sqlalchemy import Column, String, Integer, VARCHAR, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database, drop_database

Base = declarative_base()
engine = create_engine("mysql+mysqlconnector://root:root@localhost:3306/testing_db")
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine, checkfirst=True)
s = session()


class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(255), nullable=False)
    books = relationship("Book")


class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True, autoincrement=True)
    isbn = Column(VARCHAR(255), nullable=False, unique=True)
    title = Column(String(60), nullable=False)
    price = Column(Integer, nullable=False)
    author_id = Column(Integer, ForeignKey(Author.id))
    author = relationship("Author")


def create_fresh_database():
    if database_exists(engine.url):
        drop_database(engine.url)
    if not database_exists(engine.url):
        create_database(engine.url)

    Base.metadata.create_all(engine, checkfirst=True)
    s = session()

    auther_obj_1 = Author(name='Izaat')
    auther_obj_2 = Author(name='Rida')
    auther_obj_3 = Author(name='Abu Tamim')
    book_obj_1 = Book(isbn='0000', title='Islam Between West and East', price=50, author=auther_obj_1)
    book_obj_2 = Book(isbn='0001', title='Soviets', price=60, author=auther_obj_1)
    book_obj_3 = Book(isbn='0002', title='Hitler', price=70, author=auther_obj_2)
    book_obj_4 = Book(isbn='0003', title='ZXY', price=70, author=auther_obj_3)
    s.add(book_obj_1)
    s.add(book_obj_2)
    s.add(book_obj_3)
    s.add(book_obj_4)
    s.commit()


if __name__ == '__main__':

    # create_fresh_database()

    print "All Authors:"
    all_authors = s.query(Author).all()
    for author in all_authors:
        print 'id : %d, name : %s' % (author.id, author.name)
    print "--------------------"

    print "All Books:"
    all_books = s.query(Book).all()
    for book in all_books:
        print 'isbn : %s, title : %s' % (book.isbn, book.title)
    print "--------------------"

    print "Searching for specific book:"
    specific_book = s.query(Book).filter(Book.title == 'zxy')
    for book in specific_book:
        print 'isbn : %s, title : %s' % (book.isbn, book.title)
    print "--------------------"

    print "Method#1: All Books from specific Author:"
    all_books_from_author = s.query(Book).join(Book.author).filter(Author.name == 'Izaat')
    for book in all_books_from_author:
        print 'isbn : %s, title : %s' % (book.isbn, book.title)
    print "--------------------"

    print "Method#2: All Books from specific Author:"
    result = s.query(Author).filter(Author.name == 'Izaat').one()
    for book in result.books:
        print 'isbn : %s, title : %s' % (book.isbn, book.title)
    print "--------------------"

    s.close()
