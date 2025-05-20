from app import database as db
from app.models import Category
from . import with_app_context


class CategoryPrototype:
    def __init__(self, name: str):
        self.name = name.strip().lower().replace("'", "")
        self.create()

    @with_app_context
    def get(self) -> Category | None:
        return db.session.execute(
            db.select(Category).filter_by(name=self.name)
        ).scalar_one_or_none()

    @with_app_context
    def create(self) -> Category | None:
        """Get a category, that exists in the database
        Returns a category specified by name, or a newly created one, or None
        if an error has occured."""
        # Check if category with name=<name> already exists
        existing_category = db.session.execute(
            db.select(Category).filter_by(name=self.name)
        ).scalar_one_or_none()
        if existing_category is not None:
            return existing_category
        # Create a new user
        print(f"Creating a category :\tname='{self.name}'.")
        new_category = Category(
            name = self.name,
        )
        db.session.add(new_category)
        db.session.commit()
        return new_category


