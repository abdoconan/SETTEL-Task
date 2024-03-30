from passlib.context import CryptContext
from datetime import datetime

PWD_CONTEXT = CryptContext(schemes=['bcrypt'], deprecated="auto")

def get_current_datetime() -> datetime:
    return datetime.utcnow()


def hash(plain_text: str) -> str:
    return PWD_CONTEXT.hash(plain_text)


def verify_text(plain_text: str, hashed_text: str) -> bool:
    return PWD_CONTEXT.verify(plain_text, hashed_text)