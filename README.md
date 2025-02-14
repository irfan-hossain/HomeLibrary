# HomeLibrary
## Description
This appliction is intended to be used to keep track of a home library. Books can be added to the library along with related attributes. The project makes use of Python for the backend, the PyWebView library for the user interface, and HTML/CSS/JavaScript for the frontend. SqlLite is used to store the table of books (the "Library") for easy access and storage. 


<p align="center">
  <img src="docs\BlockDiagram.drawio.png" />
</p>

# Feature Requirements
## Book Attributes 
Each book shall have the following attributes:
- Title
- Author 
- Genre (Fiction or Non-Fiction)
- Sub-Genre (Literature, Sci-Fi, Biography, Health, etc.)
- Rating (Scale of 1-5)
- IsRead (True or False)

## Program Functionality
The following actions can be done to the library:
- Add a Book
- Remove a Book
- Edit a Book
- Search for a Book
- View the library as a table, rows sortable by book attributes.

## UI Prototype
<p align="center">
  <img src="docs\UI_Prototype.drawio.png" />
</p>