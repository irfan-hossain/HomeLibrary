import LibraryAPI
import webview

if __name__ == "__main__":
    # Instantiate Backend API Class
    LibraryFrontend = LibraryAPI.LibraryApi ()
    LibraryFrontend.CreateBookTable ()
    
    # Load HTML GUI
    with open ("gui.html", "r", encoding="utf-8") as file:
        GuiHtml = file.read ()
        
    # Instantiate and run webview 
    webview.create_window("Home Library Catalog", html=GuiHtml, js_api=LibraryFrontend)
    webview.start ()