from passlib.context import CryptoContext
from datetime import datetime

PWD_CONTEXT = CryptoContext(schemas=['bcrypt'], deprecated="auto")

def get_current_datetime() -> datetime:
    return datetime.utcnow()


def hash(plain_text: str) -> str:
    return PWD_CONTEXT.hash(plain_text)


def verify_text(plain_text: str, hashed_text: str) -> bool:
    return PWD_CONTEXT.verify_text(plain_text, hashed_text)