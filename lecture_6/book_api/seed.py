from database import SessionLocal
from models import Book

# Набор книг для заполнения
books_data = [
    {"title": "1984", "author": "George Orwell", "year": 1949},
    {"title": "Animal Farm", "author": "George Orwell", "year": 1945},
    {"title": "Brave New World", "author": "Aldous Huxley", "year": 1932},
    {"title": "Fahrenheit 451", "author": "Ray Bradbury", "year": 1953},
    {"title": "The Hobbit", "author": "J.R.R. Tolkien", "year": 1937},
    {"title": "The Lord of the Rings", "author": "J.R.R. Tolkien", "year": 1954},
    {"title": "To Kill a Mockingbird", "author": "Harper Lee", "year": 1960},
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "year": 1925},
    {"title": "Moby-Dick", "author": "Herman Melville", "year": 1851},
    {"title": "War and Peace", "author": "Leo Tolstoy", "year": 1869},
    {"title": "Crime and Punishment", "author": "Fyodor Dostoevsky", "year": 1866},
    {"title": "The Catcher in the Rye", "author": "J.D. Salinger", "year": 1951},
    {"title": "The Shining", "author": "Stephen King", "year": 1977},
    {"title": "Dune", "author": "Frank Herbert", "year": 1965},
    {"title": "The Martian", "author": "Andy Weir", "year": 2011},
    {"title": "The Alchemist", "author": "Paulo Coelho", "year": 1988},
    {"title": "Harry Potter and the Philosopher’s Stone", "author": "J.K. Rowling", "year": 1997},
    {"title": "Harry Potter and the Chamber of Secrets", "author": "J.K. Rowling", "year": 1998},
    {"title": "The Da Vinci Code", "author": "Dan Brown", "year": 2003},
    {"title": "The Little Prince", "author": "Antoine de Saint-Exupéry", "year": 1943},
]

def seed():
    db = SessionLocal()

    # Очистить таблицу (если хочешь начинать с нуля)
    db.query(Book).delete()
    db.commit()

    # Добавить книги
    for data in books_data:
        book = Book(**data)
        db.add(book)

    db.commit()
    db.close()
    print("База заполнена успешно!")


if __name__ == "__main__":
    seed()
