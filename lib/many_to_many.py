class Author:
    all_authors = []
    def __init__(self, name):
        self.name = name
        self._contracts = []
        Author.all_authors.append(self)

    def contracts(self):
        return [contract for contract in Contract.all if contract.author == self]
    
    def books(self):
        return [contract.book for contract in Contract.all if contract.author == self]
    
    def sign_contract(self, book, date, royalties):
        """Create and return a new contract for this author"""
        if not isinstance(book, Book):
            raise Exception("Book must be an instance of the Book class")
    
        # Just create and return the contract 
        contract = Contract(self, book, date, royalties)
        return contract
    
    def total_royalties(self):
        return sum(contract.royalties for contract in Contract.all if contract.author == self)


class Book:
    all_books = []
    def __init__(self, title):
        self.title = title
        Book.all_books.append(self)
    
    def contracts(self):
        return [contract for contract in Contract.all if contract.book == self]
    
    def authors(self):
        return [contract.author for contract in Contract.all if contract.book == self]

from datetime import datetime, date as Date

class Contract:
    all = []

    def __init__(self, author, book, date, royalties: int):
        self.author = author
        self.book = book
        self.date = date
        self.royalties = royalties

        Contract.all.append(self)

    # --- properties ---

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, author):
        # prefer specific error types
        if not isinstance(author, Author):
            raise TypeError("Author must be an instance of the Author class")
        self._author = author

    @property
    def book(self):
        return self._book

    @book.setter
    def book(self, book):
        if not isinstance(book, Book):
            raise TypeError("Book must be an instance of the Book class")
        self._book = book

    @property
    def date(self):
        # keep returning the original string for compatibility if needed
        return self._date

    @date.setter
    def date(self, date_value):
        # Accept either a date string "dd/mm/YYYY" or a datetime.date object
        if isinstance(date_value, str):
            try:
                parsed = datetime.strptime(date_value, "%d/%m/%Y").date()
            except ValueError:
                raise ValueError("Date string must be in format 'dd/mm/YYYY'")
            self._date = date_value
            self.date_obj = parsed
        elif isinstance(date_value, Date):
            # store normalized string and date_obj
            self._date = date_value.strftime("%d/%m/%Y")
            self.date_obj = date_value
        else:
            raise TypeError("Date must be a string 'dd/mm/YYYY' or a datetime.date object")

    @property
    def royalties(self):
        return self._royalties

    @royalties.setter
    def royalties(self, royalties):
        if not isinstance(royalties, int):
            raise TypeError("Royalties must be an integer")
        self._royalties = royalties

    # --- class methods ---

    @classmethod
    def contracts_by_date(cls, date_value):
        """
        Return all Contract instances whose date matches date_value,
        sorted chronologically (ascending).
        date_value may be a string 'dd/mm/YYYY' or a datetime.date object.
        """
        # normalize target
        if isinstance(date_value, str):
            try:
                target = datetime.strptime(date_value, "%d/%m/%Y").date()
            except ValueError:
                raise ValueError("Date string must be in format 'dd/mm/YYYY'")
        elif isinstance(date_value, Date):
            target = date_value
        else:
            raise TypeError("Date must be a string 'dd/mm/YYYY' or a datetime.date object")

        # sort all contracts by their date_obj and return those matching target
        sorted_contracts = sorted(cls.all, key=lambda c: c.date_obj)
        return [c for c in sorted_contracts if c.date_obj == target]
