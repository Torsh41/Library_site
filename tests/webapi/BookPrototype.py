from app import database as db
from app.models import Book, ModerationRequest
from . import with_app_context
import datetime


class BookPrototype:
    def __init__(self, name: str, user_id: int, category_id: int,
                 author="", description="", isbn="", reference_url="",
                 publishing_house="", release_date=datetime.datetime.now(),
                 count_of_chapters=0,
                 moderation_request_status=ModerationRequest.STATUS_OPEN):
        self.name = name.strip().lower().replace("'", "")
        self.author = author.strip().lower()
        self.description = description.strip()
        self.category_id = category_id
        self.user_id = user_id
        self.isbn = isbn.strip()
        self.reference_url = reference_url.strip()
        self.publishing_house = publishing_house.strip()
        # self.timestamp = datetime.datetime.now()
        self.release_date = release_date
        self.count_of_chapters = count_of_chapters
        self.moderation_request_status = moderation_request_status
        self.create()

    @with_app_context
    def get(self) -> Book | None:
        return db.session.execute(
            db.select(Book).filter_by(name=self.name)
        ).scalar_one_or_none()

    @with_app_context
    def get_moderation(self) -> ModerationRequest | None:
        return db.session.execute(
            db.select(ModerationRequest).filter_by(book=self.get())
        ).scalar_one_or_none()

    @with_app_context
    def create(self) -> Book | None:
        """Get a book, that exists in the database
        Returns a book specified by name, or a newly created one, or None if an
        error has occured."""
        # Check if book with name=<name> already exists
        existing_book = db.session.execute(
            db.select(Book).filter_by(name=self.name)
        ).scalar_one_or_none()
        if existing_book is not None:
            return existing_book
        # Create a new user
        print(f"Creating a book :\tname='{self.name}', author='{self.author}'.")
        moderation_request = ModerationRequest(_status=self.moderation_request_status)
        new_book = Book(
            name = self.name,
            author = self.author,
            description = self.description,
            isbn = self.isbn,
            reference_url = self.reference_url,
            publishing_house = self.publishing_house,
            # timestamp = self.timestamp,
            release_date = self.release_date,
            count_of_chapters = self.count_of_chapters,
            category_id = self.category_id,
            user_id = self.user_id,
            moderation_request = moderation_request
        )
        new_book.default_cover()
        db.session.add(moderation_request)
        db.session.add(new_book)
        db.session.commit()
        return new_book


