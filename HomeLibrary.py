import sqlite3
import json
import webview

BOOK_TABLE_TITLE_COL_INDEX       = 0
BOOK_TABLE_AUTHOR_COL_INDEX      = 1

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
        self.AddBookToTable (BookDictData['title'], BookDictData['author'])
        
        # Return the latest list of books to frontend
        JsonDumpOfBooks = self.GetListofBooksJs ()
        return JsonDumpOfBooks

    def RemoveBookFromTableJs (self, BookJsonData):
        # Convert the book data in JSON format to a python dictionary
        BookDictData = json.loads (BookJsonData)
        
        # Add to Book Table
        Title = str(BookDictData['title'])
        self.RemoveBookFromTable (Title)
        
        # Return the latest list of books to frontend
        JsonDumpOfBooks = self.GetListofBooksJs ()
        return JsonDumpOfBooks

    def GetListofBooksJs (self):
        # Query for Book Data
        self.DbCursor.execute("SELECT title, author FROM book")
        
        # Organize table into python list of dicts
        books = [{"title": row[BOOK_TABLE_TITLE_COL_INDEX], "author": row[BOOK_TABLE_AUTHOR_COL_INDEX]} for row in self.DbCursor.fetchall()]
        
        # Re-Format List to JSON
        return json.dumps(books)  # Send book list to frontend               

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