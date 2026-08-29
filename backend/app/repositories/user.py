from uuid import UUID
from sqlalchemy.orm import Session
from app.models.auth import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str):
        """Get a user by email."""
        return self.db.query(User).filter(User.email == email).first()

    def create(self, email: str, full_name: str, password_hash: str):
        """Create a new user."""
        new_user = User(email=email, full_name=full_name, password_hash=password_hash)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def get_by_id(self, user_id: UUID) -> User | None:
        """Return the user for the given ID, or None if not found."""
        return self.db.query(User).filter(User.id == user_id).first()
