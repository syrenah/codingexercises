"""
Instance methods vs. class methods in Python

An instance method receives self, the individual object that called it. It
can read or change attributes that belong to that object.

A class method receives cls, the class that called it. It can read or change
class-level state and can be called through either the class or an instance.
"""


class Book:
    library_name = "City Library"
    total_books = 0

    def __init__(self, title):
        self.title = title
        Book.total_books += 1

    def describe(self):
        """Instance method: uses this specific Book's title."""
        return f'"{self.title}" is available at {Book.library_name}.'

    @classmethod
    def change_library(cls, new_name):
        """Class method: changes shared state for every Book."""
        cls.library_name = new_name

    @classmethod
    def from_title(cls, title):
        """Class method: creates an instance of cls."""
        return cls(title)


def main():
    first_book = Book("The Hobbit")
    second_book = Book.from_title("Charlotte's Web")

    # Instance-method calls operate on one object at a time.
    print(first_book.describe())
    print(second_book.describe())

    # The class method changes library_name for the entire Book class.
    Book.change_library("Neighborhood Library")
    print(first_book.describe())
    print(second_book.describe())

    # Class methods can also be called from an instance.
    print(f"Book objects created: {first_book.total_books}")


if __name__ == "__main__":
    main()
