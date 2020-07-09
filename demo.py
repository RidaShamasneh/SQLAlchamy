from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database

import declarative_base_class
from sql_alchemy_classes import Book, Author
from sqlalchemy import and_
from sqlalchemy import or_

engine = create_engine("mysql+mysqlconnector://root:root@localhost:3306/testing_db")  # , echo=True
session = sessionmaker()
session.configure(bind=engine)
declarative_base_class.base.metadata.create_all(engine, checkfirst=True)
s = session()


def create_fresh_database():
    if database_exists(engine.url):
        drop_database(engine.url)
    if not database_exists(engine.url):
        create_database(engine.url)

    session = sessionmaker()
    session.configure(bind=engine)
    declarative_base_class.base.metadata.create_all(engine, checkfirst=True)
    s = session()

    auther_obj_1 = Author(_name='Izaat')
    auther_obj_2 = Author(_name='Rida')
    auther_obj_3 = Author(_name='Abu Tamim')
    book_obj_1 = Book(_isbn='0000', _title='Islam Between West and East', _price=50, author=auther_obj_1)
    book_obj_2 = Book(_isbn='0001', _title='Soviets', _price=60, author=auther_obj_1)
    book_obj_3 = Book(_isbn='0002', _title='Hitler', _price=70, author=auther_obj_2)
    book_obj_4 = Book(_isbn='0003', _title='ZXY', _price=70, author=auther_obj_3)
    book_obj_5 = Book(_isbn='0004', _title='Authorless_1', _price=80)
    book_obj_6 = Book(_isbn='0005', _title='Authorless_2', _price=80)
    book_obj_7 = Book(_isbn='0006', _title='Authorless_3', _price=80)
    book_obj_8 = Book(_isbn='0007', _title='Authorless_4', _price=80)
    s.add(book_obj_1)
    s.add(book_obj_2)
    s.add(book_obj_3)
    s.add(book_obj_4)
    s.add(book_obj_5)
    s.add(book_obj_6)
    s.add(book_obj_7)
    s.add(book_obj_8)

    auther_obj_4 = Author(_name='Rida')
    auther_obj_5 = Author(_name='Ali')
    auther_obj_6 = Author(_name='')
    s.add(auther_obj_4)
    s.add(auther_obj_5)
    s.add(auther_obj_6)

    s.commit()


def fill_data_in_database():
    print "All Authors:"
    all_authors = s.query(Author).all()
    for author in all_authors:
        print 'id : %d, name : %s' % (author.id, author.name)
    print "--------------------"

    print "Authors that have books:"
    authors = s.query(Author).join(Book, Author.id == Book.author_id)
    for author in authors:
        print 'author_name: %s' % (author.name)
    print "--------------------"

    print "Distinct Author names: approach #1 (using distinct in SQL Alchamy)"
    distinct_author_names = s.query(Author._name).distinct().all()
    for author_name in distinct_author_names:
        print 'author_name: %s' % (author_name)
    print "--------------------"

    print "Distinct Authors: approach #2 (Getting all results and finding distinct names programmatically)"
    all_authors = s.query(Author).all()
    distinct_author_names = {author._name for author in all_authors}
    for author_name in distinct_author_names:
        print 'author_name: %s' % (author_name)
    print "--------------------"

    print "Distinct Author names from books table"
    all_books = s.query(Book).all()
    distinct_author_names = {book.author_marking for book in all_books}
    for author_name in distinct_author_names:
        print 'author_name: %s' % (author_name)
    print "--------------------"

    print "All Books:"
    all_books = s.query(Book).all()
    for book in all_books:
        print 'isbn : %s, title : %s, price: %d' % (book.isbn, book.title, book.price)
    print "--------------------"

    print "Some Books:"
    list_of_all = [Book.author_id.in_([1]), Book._isbn.in_(['0000'])]
    args = tuple(list_of_all)
    all_books = s.query(Book).filter(*args)
    for book in all_books:
        print 'isbn : %s, title : %s, price: %d' % (book._isbn, book._title, book._price)
    print "--------------------"

    print "Books without author:"
    list_of_all = [Book.author_id.is_(None)]
    args = tuple(list_of_all)
    all_books = s.query(Book).filter(*args)
    for book in all_books:
        print 'isbn : %s, title : %s, price: %d' % (book._isbn, book._title, book._price)
    print "--------------------"

    print "Books without author and another author:"
    list_of_all = [Book.author_id.in_([1]), Book._isbn.in_(['0000'])]
    args = tuple(list_of_all)
    all_books = s.query(Book).filter(or_(Book.author_id.is_(None), *args))
    for book in all_books:
        print 'isbn : %s, title : %s, price: %d' % (book._isbn, book._title, book._price)
    print "--------------------"

    print "Books without author and another author:"
    global_and_operator = True

    local_and_operator = True
    local_and_operator = Book.author_id.in_([1])
    local_and_operator = or_(local_and_operator, Book.author_id.is_(None))
    global_and_operator = and_(global_and_operator, local_and_operator)

    local_and_operator = True
    local_and_operator = and_(local_and_operator, Book._isbn.in_(['0000']))
    global_and_operator = and_(global_and_operator, local_and_operator)

    all_books = s.query(Book).filter(global_and_operator)
    for book in all_books:
        print 'isbn : %s, title : %s, price: %d' % (book._isbn, book._title, book._price)
    print "--------------------"

    print "Searching for specific book:"
    specific_book = s.query(Book).filter(Book._title == 'zxy')
    for book in specific_book:
        print 'isbn : %s, title : %s, price: %d' % (book._isbn, book._title, book._price)
    print "--------------------"

    print "Method#1: All Books from specific Author:"
    all_books_from_author = s.query(Book).join(Book.author).filter(Author._name == 'Izaat')
    for book in all_books_from_author:
        print 'isbn : %s, title : %s' % (book._isbn, book._title)
    print "--------------------"

    print "Method#2: All Books from specific Author:"
    result = s.query(Author).filter(Author._name == 'Izaat').one()
    for book in result.books:
        print 'isbn : %s, title : %s' % (book._isbn, book._title)
    print "--------------------"

    print "Updating some book price:"
    specific_book = s.query(Book).filter(Book._title == 'zxy')
    for book in specific_book:
        book.price = 123

    print "Deleting some book:"
    # Returns 1 as deletion_result upon success deletion (i.e. item was found and deleted)
    # Returns 0 as deletion_result upon failed deletion (e.g. the item was not found)
    # deletion_result = s.query(Book).filter(Book.title == 'Hitler').delete()

    print "Deleting some Author:"
    # deletion_result = s.query(Author).filter(Author.name == 'Izaat').delete()

    s.commit()
    s.close()


if __name__ == '__main__':
    create_fresh_database()
    fill_data_in_database()
    pass
