from app import database as db
from app.models import User, Role
from werkzeug.test import Client, TestResponse
from . import with_app_context, extract_csrf_token


class UserPrototype:
    def __init__(self, name: str, email: str, password: str, role: Role):
        self.name = name.strip().replace("'", "")
        self.email = email.strip().lower()
        self.password = password
        self.role = role
        self.user = self.register()

    def copy(self):
        """Get a deep copy of the object <self>.
        Can be used to make sure the user is registered in the given testcase."""
        return UserPrototype(self.name, self.email, self.password, self.role)

    def get(self):
        return self.user

    @with_app_context
    def register(self) -> User | None:
        """Get a registered user.
        Returns an existing user specified by name, or a newly created one,
        or None if an error has occured."""
        # Check if user with username=<username> already exists
        existing_user = db.session.execute(
            db.select(User).filter_by(username=self.name)
        ).scalar_one_or_none()
        if existing_user is not None:
            return existing_user
        # Create a new user
        print(f"Registration - Test User:\tusername='{self.name}', " +
              f"email='{self.email}', pwd={self.password}'.")
        new_user = User(
            username = self.name,
            email = self.email,
            password = self.password,
            role = self.role,
            confirmed = True
        )
        new_user.default_ava()
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def login(self, client: Client) -> TestResponse:
        """The client recieves a cookie for user authentication."""
        # Extract CSRF token from the /auth/login page (the ugly way)
        response = client.post("/auth/login")
        csrf_token = extract_csrf_token(response.data.decode("utf-8"))
        # Log in
        response = client.post("/auth/login", data={
            "csrf_token": csrf_token,
            "email": self.email,
            "password": self.password
        })
        return response

# Create User Prototypes with different user roles
test_user = UserPrototype("User1", "user1@user.user", "123456", Role.USER)
test_admin = UserPrototype("Admin1", "admin1@admin.admin", "123456", Role.ADMIN)
test_moderator = UserPrototype("Moderator1", "moderator1@moderator.moderator", "123456", Role.MODERATOR)
test_teacher = UserPrototype("Teacher1", "teacher1@teacher.teacher", "123456", Role.TEACHER)


