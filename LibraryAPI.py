import sqlite3
import json

BOOK_TABLE_TITLE_COL_INDEX       = 0
BOOK_TABLE_AUTHOR_COL_INDEX      = 1
BOOK_TABLE_MAJOR_GENRE_COL_INDEX = 2
BOOK_TABLE_MINOR_GENRE_COL_INDEX = 3
BOOK_TABLE_READ_COL_INDEX        = 4

class LibraryApi: 
    # Class Infrastructure Methods
    def __init__ (self):
        self.DbConnection = sqlite3.connect("library.db", check_same_thread=False)
        self.DbCursor     = self.DbConnection.cursor()
        return
    
    def __enter__ (self):
        return self 
    
    def __exit__ (self):
        self.DbConnection.close ()
        return

    # Python Backend Library Methods
    def CreateBookTable (self):
        self.DbCursor.execute ("CREATE TABLE IF NOT EXISTS Book(Title TEXT, Author TEXT)")
        self.DbConnection.commit ()
        return
    
    def DeleteTable (self):
        self.DbCursor.execute("delete from " + "book");
        return
    
    def AddBookToTable (self, Title, Author):
        query = ("""
        INSERT INTO book VALUES
            (?, ?)
        """)
        
        self.DbCursor.execute (query, (Title, Author))
        self.DbConnection.commit()
        
        print ("Added", f'"{Title}"', "by", Author)
        return
        
    def RemoveBookFromTable (self, Title):
        query = ("""
            DELETE FROM Book
            WHERE Title IN (?);
        """)
        
        self.DbCursor.execute (query, (Title))
        self.DbConnection.commit()       
        return 
    
    # Methods to interact between Javascript and Python
    def AddBookToTableInJsonFormat (self, BookJsonData):
        # Convert the book data in JSON format to a python dictionary
        BookDictData = json.loads (BookJsonData)

        # Add to Book Table
        self.AddBookToTable (BookDictData['title'], BookDictData['author'])
        
        # Return the latest list of books to frontend
        JsonDumpOfBooks = self.GetListofBooksInJsonFormat ()
        return JsonDumpOfBooks
        
    def GetListofBooksInJsonFormat (self):
        self.DbCursor.execute("SELECT title, author FROM book")
        books = [{"title": row[0], "author": row[1]} for row in self.DbCursor.fetchall()]
        return json.dumps(books)  # Send book list to frontend               
