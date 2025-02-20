import sqlite3
import webview
import json 

BOOK_TABLE_TITLE_COL_INDEX       = 0
BOOK_TABLE_AUTHOR_COL_INDEX      = 1
BOOK_TABLE_GENRE_COL_INDEX       = 2
BOOK_TABLE_IS_READ_COL_INDEX     = 3
BOOK_TABLE_DATE_READ_COL_INDEX   = 4
BOOK_TABLE_RATING_COL_INDEX      = 5

class HomeLibraryApi: 
    #
    # Class Infrastructure Methods
    #
    def __init__ (self):
        self.DbConnection = sqlite3.connect("library.db", check_same_thread=False)
        self.DbCursor     = self.DbConnection.cursor()
        return
    
    def __enter__ (self):
        return self 
    
    def __exit__ (self):
        self.DbConnection.close ()
        return

    #
    # Python Backend Library Methods
    #
    def CreateBookTable (self):
        self.DbCursor.execute ("CREATE TABLE IF NOT EXISTS Book(Title TEXT, Author TEXT, Genre TEXT, IsRead TEXT, DateRead TEXT, Rating TEXT)")
        self.DbConnection.commit ()
        return
    
    def AddBookToTable (self, Title, Author, Genre, IsRead, DateRead, Rating):
        query = ("""
        INSERT INTO book VALUES
            (?, ?, ?, ?, ?, ?)
        """)
        
        self.DbCursor.execute (query, (Title, Author, Genre, IsRead, DateRead, Rating))
        self.DbConnection.commit()
        
        return
        
    def RemoveBookFromTable (self, Title):
        query = ("""
        DELETE FROM Book
            WHERE Title=?
        """)
        
        self.DbCursor.execute (query, (Title,))
        self.DbConnection.commit()       
        return 
    
    #
    # Methods to interact between Javascript and Python
    #
    def AddBookToTableJs (self, BookJsonData):
        # Convert the book data in JSON format to a python dictionary
        BookDictData = json.loads (BookJsonData)

        # Add to Book Table
        self.AddBookToTable (
            BookDictData['title'], 
            BookDictData['author'], 
            BookDictData['genre'], 
            BookDictData['isread'],
            BookDictData['dateread'],
            BookDictData['rating']
        )
        
        # Return the latest list of books to frontend
        JsonDumpOfBooks = self.GetListofBooksJs ()
        return JsonDumpOfBooks

    def RemoveBookFromTableJs (self, BookJsonData):
        # Convert the book data in JSON format to a python dictionary
        BookDictData = json.loads (BookJsonData)
        
        # Remove Book From Table
        Title = str(BookDictData['title'])
        self.RemoveBookFromTable (Title)
        
        # Return the latest list of books to frontend
        JsonDumpOfBooks = self.GetListofBooksJs ()
        return JsonDumpOfBooks

    def GetListofBooksJs (self):
        # Query for Book Data
        self.DbCursor.execute("SELECT title, author, genre, isread, dateread, rating FROM book")
        
        # Organize table into python list of dicts
        Books = [
            {"title"    : row[BOOK_TABLE_TITLE_COL_INDEX], 
             "author"   : row[BOOK_TABLE_AUTHOR_COL_INDEX],
             "genre"    : row[BOOK_TABLE_GENRE_COL_INDEX],
             "isread"   : row[BOOK_TABLE_IS_READ_COL_INDEX],
             "dateread" : row[BOOK_TABLE_DATE_READ_COL_INDEX],
             "rating"   : row[BOOK_TABLE_RATING_COL_INDEX]} 
            for row in self.DbCursor.fetchall()
        ]
        
        # Re-Format List to JSON
        return json.dumps(Books)  # Send book list to frontend               

    def SearchJs (self, BookJsonData):
        # Convert the book data in JSON format to a python dictionary
        BookDictData = json.loads (BookJsonData)

        # Add to Book Table
        BookTitle = BookDictData['title']
        
        # Query for Book Data
        self.DbCursor.execute("SELECT title, author, genre, isread, dateread, rating FROM book")
        
        # Organize table into python list of dicts
        Books = [
            {"title"    : row[BOOK_TABLE_TITLE_COL_INDEX], 
             "author"   : row[BOOK_TABLE_AUTHOR_COL_INDEX],
             "genre"    : row[BOOK_TABLE_GENRE_COL_INDEX],
             "isread"  : row[BOOK_TABLE_IS_READ_COL_INDEX],
             "date_read": row[BOOK_TABLE_DATE_READ_COL_INDEX],
             "rating"   : row[BOOK_TABLE_RATING_COL_INDEX]} 
            for row in self.DbCursor.fetchall()
        ]
                
        # Search for book data based on title.
        Result = None
        for book in Books:
            if book['title'] == BookTitle:
                print ("found", BookTitle)
                Result = [book]
                break;

        # Return book data as only element in list
        return json.dumps(Result)  # Send book list to frontend     
                
if __name__ == "__main__":
    # Instantiate Backend API Class
    LibraryFrontend = HomeLibraryApi ()
    LibraryFrontend.CreateBookTable ()
    
    # Load HTML GUI
    with open ("index.html", "r", encoding="utf-8") as file:
        GuiHtml = file.read ()
        
    # Instantiate and run webview 
    webview.create_window("Home Library Catalog", html=GuiHtml, js_api=LibraryFrontend)
    webview.start ()
