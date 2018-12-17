class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        # Maps a book object to it's rating
        self.books = {}

    def __repr__(self):
        return 'User: {}, email: {}, books read: {}'.format(self.name, self.email, self.books)

    def __eq__(self, other_user):
        if self.name == other_user.name and self.email == other_user.email:
            return True
        else:
            return False

    def get_email(self):
        return self.email

    def change_email(self, address: str):
        self.email = address
        print('Email address has been changed to {}'.format(address))

    def read_book(self, book, rating=None):
        self.books.update({book: rating})

    def get_average_rating(self):
        rating_total = 0
        rating_count = 0
        for book, rating in self.books.items():
            if rating:
                rating_count += 1
                rating_total += rating
        return rating_total / rating_count


class Book:
    def __init__(self, title: str, isbn: int):
        self.title = title
        self.isbn = isbn
        self.ratings = []

    def __eq__(self, other_book):
        if self.title == other_book.title and self.isbn == other_book.isbn:
            return True
        else:
            return False

    def __repr__(self):
        return "{}".format(self.title)

    def __hash__(self):
        return hash((self.title, self.isbn))

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, number: int):
        self.isbn = number
        print("{}'s ISBN has been changed to {}".format(self.title, self.isbn))

    def add_rating(self, rating: int):
        if 4 >= rating >= 0:
            self.ratings.append(rating)
        else:
            print("{} is an invalid rating".format(rating))

    def get_average_rating(self):
        rating_total = 0
        for rating in self.ratings:
            rating_total += rating
        return rating_total / len(self.ratings)

    def get_title(self):
        return self.title


class Fiction(Book):
    def __init__(self, title: str, author: str, isbn: int):
        Book.__init__(self, title, isbn)
        self.author = author

    def __repr__(self):
        return "{} by {}".format(self.title, self.author)

    def get_author(self):
        return self.author


class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn):
        Book.__init__(self, title, isbn)
        self.subject = subject
        self.level = level

    def __repr__(self):
        return "{}, a {} manual on {}".format(self.title, self.level, self.subject)

    def get_level(self):
        return self.level

    def get_subject(self):
        return self.subject


class TomeRater:
    def __init__(self):
        # email to user object
        self.users = {}
        # book to number of readers
        self.books = {}

    # Print behavior
    def __str__(self):
        return "TomeRater\n{}\n{}".format(self.users, self.books)

    def __eq__(self, other):
        if type(other) != TomeRater:
            raise TypeError("Object {} is not of type TomeRater".format(other))

        else:  # Compare the two objects
            if len(self.users) != len(other.users) or len(self.books) != len(other.books):
                return False

            for email, user_obj in self.users.items():
                other_user_obj = other.users.get(email)
                if user_obj != other_user_obj:
                    return False

            other_books = other.books.keys()
            for book in self.books.keys():
                if book not in other_books:
                    return False

            return True

    def create_book(self, title: str, isbn: int):
        return Book(title=title, isbn=isbn)

    def create_novel(self, title: str, author: str, isbn: int):
        return Fiction(title=title, author=author, isbn=isbn)

    def create_non_fiction(self, title: str, subject: str, level: str, isbn: int):
        return Non_Fiction(title=title, subject=subject, level=level, isbn=isbn)

    def add_book_to_user(self, book: Book, email: str, rating: int=None):
        user = self.users.get(email)
        if user:
            user.read_book(book, rating)
            if rating:
                book.add_rating(rating)
            if self.books.get(book):
                self.books.update({book: self.books[book] + 1})
            else:
                self.books.update({book: 1})
        else:
            print("No user with email {}!".format(email))

    def add_user(self, name: str, email: str, user_books: list=None):
        new_user = User(name=name, email=email)
        self.users.update({email: new_user})
        if user_books:
            for book in user_books:
                self.add_book_to_user(book=book, email=email)

    def print_catalog(self):
        print(self.books.keys())

    def print_users(self):
        print(self.users.values())

    def get_most_read_book(self):
        for book, reads in self.books.items():
            if 'most_read' not in locals():
                most_read = book
                most_reads = reads
            elif reads > most_reads:
                most_read = book
                most_reads = reads
        return most_read

    def highest_rated_book(self):
        book_list: list = self.books.keys()
        for book in book_list:
            if 'highest_rated' not in locals():
                highest_rated = book
            elif book.get_average_rating() > highest_rated.get_average_rating():
                highest_rated = book
        return highest_rated

    def most_positive_user(self):
        for email, user_obj in self.users.items():
            if 'most_positive' not in locals():
                most_positive = self.users.get(email)
            elif self.users.get(email).get_average_rating() > most_positive.get_average_rating():
                most_positive = self.users.get(email)
        return most_positive
