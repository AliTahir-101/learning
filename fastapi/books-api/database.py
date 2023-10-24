from sqlalchemy.orm import registry, relationship, Session
from sqlalchemy import Column, String, Integer, create_engine, ForeignKey, select

engine = create_engine(
    "mysql+mysqlconnector://root:test123@localhost:3306/books",
    echo=True
)

mapper_registry = registry()

Base = mapper_registry.generate_base()


class Author(Base):
    __tablename__ = 'authors'
    author_id = Column(Integer, primary_key=True)
    first_name = Column(String(length=50))
    last_name = Column(String(length=50))

    def __repr__(self):
        return f"<Author(author_id='{self.author_id}', first_name='{self.first_name}', last_name= '{self.last_name}')>"


class Book(Base):
    __tablename__ = 'books'

    book_id = Column(Integer, primary_key=True)
    title = Column(String(length=255))
    number_of_pages = Column(Integer)

    def __repr__(self):
        return f"<Book(book_id='{self.book_id}', title='{self.title}', number_of_pages='{self.number_of_pages}')>"


class BookAuthor(Base):
    __tablename__ = 'bookauthors'
    bookauthor_id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('authors.author_id'))
    book_id = Column(Integer, ForeignKey('books.book_id'))

    author = relationship("Author")
    book = relationship("Book")

    def __repr__(self):
        return f"<BookAuthor(bookauthor_id='{self.bookauthor_id}', author_id='{self.author_id}', book_id='{self.book_id}', first_name='{self.author.first_name}', last_name='{self.author.last_name}', title='{self.book.title}')>"


Base.metadata.create_all(engine)


def add_book(book: Book, author: Author):
    with Session(engine) as session:
        existing_book = session.execute(select(Book).filter(
            Book.title == book.title, Book.number_of_pages == book.number_of_pages)).scalar()
        if existing_book:
            print("Book has already been added.")
            return
        else:
            print("Book does not exist. Adding Book!")
            session.add(book)
        existing_author = session.execute(select(Author).filter(
            Author.first_name == author.first_name, Author.last_name == author.last_name)).scalar()
        if existing_author:
            print("Author has already been added.")
            session.flush()
            pairing = BookAuthor(
                author_id=existing_author.author_id, book_id=book.book_id)
        else:
            print("Author does not exist. Adding Author!")
            session.add(author)
            session.flush()
            pairing = BookAuthor(
                author_id=author.author_id, book_id=book.book_id)
        session.add(pairing)
        session.commit()
        print("New pairing added!", str(pairing))


def get_book(id: int):
    with Session(engine) as session:
        existing_book = session.execute(select(Book).filter(
            Book.book_id == id)).scalar()
        if existing_book:
            pairing = session.execute(select(BookAuthor).filter(
                BookAuthor.book_id == id
            )).scalar()
            author = session.execute(select(Author).filter(
                Author.author_id == pairing.author_id
            )).scalar()
            return {
                "Book Id": existing_book.book_id,
                "Book Title": existing_book.title,
                "Total Book Pages": existing_book.number_of_pages,
                "Author Name": f"{author.first_name} {author.last_name}"
            }
        else:
            return None
