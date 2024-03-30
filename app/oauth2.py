from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import sechemaes, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

SECRET_KEY = "ak9aZUnOe(?E6!Vc.:dq}]D2.T@c?;&mCl8d5ZD7lKK99/PE)""1(<MuJ.neS%`"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10

oauth2_sechema = OAuth2PasswordBearer(tokenUrl="users/login")

def create_access_token(token_data: dict = {}):
    to_encode = token_data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def update_user_login_data(user: models.User, token: str, db: Session):
    user.current_token =  token
    user.last_action_time = datetime.utcnow()
    db.commit()

def verify_access_token(token: str, credentials_exception: HTTPException):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get('user_id')
        if not user_id:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return user_id

def get_current_user(token: str = Depends(oauth2_sechema)
                     , db: Session = Depends(database.get_db)):
    credentials_exception : HTTPException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                        detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    user_id = verify_access_token(token, credentials_exception)
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    user.last_action_time += timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    db.commit()
    return user
