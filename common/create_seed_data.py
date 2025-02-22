from sqlalchemy.orm import Session
import uuid
from passlib.context import CryptContext

from models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str):
    return pwd_context.hash(password)


def seed_data(session: Session):
    count = session.query(User).count()

    if count == 0:
        admin = User(
            id=uuid.uuid4(),
            firstname="Admin",
            lastname="user",
            email="admin@gmail.com",
            is_admin=True,
            activated=True
        )
        admin.set_password("Test1234")
        session.add(admin)

        session.commit()

        print("Admin user created")
    else:
        print("Data already exists, skipping seed.")
