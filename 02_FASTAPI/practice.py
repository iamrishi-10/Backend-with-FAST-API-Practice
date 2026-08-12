from fastapi import FastAPI 


app = FastAPI()

BOOKS = [
    {
        'title': 'A Brief History of Time', 
        'author': 'Stephen Hawking', 
        'category': 'science'
    },
    {
        'title': 'Sync: How Order Emerges from Chaos in the Universe, Nature, and Daily Life', 
        'author': 'Steven Strogatz', 
        'category': 'science'
    },
    {
        'title': 'Sapiens: A Brief History of Humankind', 
        'author': 'Yuval Noah Harari', 
        'category': 'history'
    },
    {
        'title': 'How Not to Be Wrong: The Power of Mathematical Thinking', 
        'author': 'Jordan Ellenberg', 
        'category': 'math'
    },
    {
        'title': "Fermat's Enigma: The Epic Quest to Solve the World's Greatest Mathematical Problem", 
        'author': 'Simon Singh', 
        'category': 'math'
    },
    {
        'title': 'The Joy of x: A Guided Tour of Math, from One to Infinity', 
        'author': 'Steven Strogatz', 
        'category': 'math'
    }
]




@app.get('/books')
def read_all_books():
    return BOOKS



@app.get("/books/")
def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').lower() == category.lower():
            books_to_return.append(book)
    return books_to_return



#Using Path Parameters
@app.get("/books/byauthor/")
def read_books_by_author_path(author: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').lower() == author.lower():
            books_to_return.append(book)

    return books_to_return



#Using Query Parameters
@app.get("/books/{book_title}")
def read_book(book_title: str):
    for book in BOOKS:
        if book.get('title').lower() == book_title.lower():
            return book
    return {"message": "Book not found"}



#Using both Path and Query Parameters
@app.get("/books/{book_author}/")
def read_author_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').lower() == book_author.lower() and \
                book.get('category').lower() == category.lower():
            books_to_return.append(book)
    return books_to_return