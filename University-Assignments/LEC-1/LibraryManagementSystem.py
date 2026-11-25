from abc import ABC, abstractmethod
from datetime import date, timedelta


# Abstract base class: every person has a name and a validated email.
class Person(ABC):
    def __init__(self, name, email):
        self.name = name
        self.email = email

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not isinstance(value, str) or "@" not in value or "." not in value.split("@")[-1]:
            raise ValueError("Please enter a valid email address.")
        self._email = value

    @abstractmethod
    def get_role(self):
        """Return the person's role in the library."""
        pass

    def __str__(self):
        return f"{self.name} <{self.email}>"


class Member(Person):
    def __init__(self, member_id, name, email):
        super().__init__(name, email)
        self.member_id = member_id
        self._active = True
        self._loans = []

    @property
    def active(self):
        return self._active

    def get_role(self):
        return f"Library member (ID: {self.member_id})"

    def add_loan(self, loan):
        self._loans.append(loan)

    def __str__(self):
        return f"Member {self.member_id}: {self.name} ({self.email})"


class Librarian(Person):
    def __init__(self, employee_id, name, email):
        super().__init__(name, email)
        self.employee_id = employee_id

    def get_role(self):
        return f"Librarian (Employee ID: {self.employee_id})"

    def __str__(self):
        return f"Librarian {self.employee_id}: {self.name}"


class Book:
    def __init__(self, isbn, title, author, copies=1):
        if copies < 0:
            raise ValueError("Copies cannot be negative.")
        self.isbn = isbn
        self.title = title
        self.author = author
        self._available_copies = copies

    @property
    def available_copies(self):
        return self._available_copies

    def borrow_copy(self):
        if self._available_copies <= 0:
            raise ValueError(f'No available copies of "{self.title}".')
        self._available_copies -= 1

    def return_copy(self):
        self._available_copies += 1

    def __str__(self):
        return (f'"{self.title}" by {self.author} '
                f'(ISBN: {self.isbn}, available: {self.available_copies})')


class Loan:
    def __init__(self, loan_id, book, member, days=14):
        if not isinstance(book, Book):
            raise TypeError("A loan must be for a Book.")
        if not isinstance(member, Member):
            raise TypeError("A loan must belong to a Member.")
        if not member.active:
            raise ValueError("This member is not active.")