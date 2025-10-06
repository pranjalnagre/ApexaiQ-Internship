class Book:
    """
    Represents a book with a title, author, and availability status.
    """

    def __init__(self, title, author):
        """
        Initialize a new Book object.

        Returns:
        None
        """
        self.title = title
        self.author = author
        self.is_borrowed = False

    def __str__(self):
        """
        Return a string representation of the book with its status.

        Returns:
            str: The book's title, author, and availability status.
        """
        status = "Borrowed" if self.is_borrowed else "Available"
        return f"{self.title} by {self.author} - {status}"


class Member:
    """
    Represents a library member who can borrow books.
    """

    def __init__(self, name):
        """
        Initialize a new Member object.

        Returns:
        None
        """
        self.name = name
        self.borrowed_books = []

    def borrow_book(self, book, library):
        """
        Borrow a book from the library.

        Returns:
        None
        """
        if library.lend_book(book):
            self.borrowed_books.append(book)
            print(f"{self.name} borrowed '{book.title}'")
        else:
            print(f"'{book.title}' is not available")

    def return_book(self, book, library):
        """
        Return a borrowed book to the library.

        Returns:
        None
        """
        if book in self.borrowed_books:
            library.return_book(book)
            self.borrowed_books.remove(book)
            print(f"{self.name} returned '{book.title}'")
        else:
            print(f"{self.name} doesn't have '{book.title}'")


class Library:
    """
    Represents a library that manages books.
    """

    def __init__(self):
        """
        Initialize an empty Library object.
        """
        self.books = []

    def add_book(self, book):
        """
        Add a new book to the library.

        Returns:
        None
        """
        self.books.append(book)

    def lend_book(self, book):
        """
        Lend a book to a member if available.

        Returns:
            bool: True if the book was lent, False otherwise.
        """
        if book in self.books and not book.is_borrowed:
            book.is_borrowed = True
            return True
        return False

    def return_book(self, book):
        """
        Mark a book as returned.

        Returns:
        None
        """
        if book in self.books:
            book.is_borrowed = False

    def show_available_books(self):
        """
        Display all available (not borrowed) books in the library.
        """
        print("\nAvailable Books:")
        for book in self.books:
            if not book.is_borrowed:
                print(book)

    def find_book(self, title):
        """
        Find a book in the library by its title.

        Returns:
            Book or None: The matching book if found, otherwise None.
        """
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None




library = Library()


book1 = Book("Atomic Habits", "James Clear")
book2 = Book("Harry Potter", "J.K. Rowling")
book3 = Book("Alchemist", "Paulo Coelho")

library.add_book(book1)
library.add_book(book2)
library.add_book(book3)


member_name = input("Enter your name: ")
member = Member(member_name)


library.show_available_books()


title = input("\nEnter the book name you want to borrow: ")
book_to_borrow = library.find_book(title)

if book_to_borrow:
    member.borrow_book(book_to_borrow, library)
else:
    print("Book not found in library!")


library.show_available_books()
