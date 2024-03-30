from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


from .. import sechemaes, models, database, oauth2, utils


router = APIRouter(
    prefix="/users", 
    tags=["User"]
)

def is_user_exists(user_details : sechemaes.UserCreate
                   , db: Session = Depends(database.get_db)
                   ) -> bool :
    conditions = or_(models.User.username == user_details.username, 
                     models.User.email == user_details.email) 
    user = db.query(models.User).filter(conditions).first()
    if not user:
        return False
    return True
    
    
@router.post("/login", response_model =sechemaes.Token)
def login(user_credentials : OAuth2PasswordRequestForm = Depends()
          , db: Session = Depends(database.get_db)) :
    """
    OAuth2PasswordRequestForm has only username and password fields
    for my application username can be both email or username
    """
    conditions = or_(models.User.username == user_credentials.username, models.User.email == user_credentials.username)
    user = db.query(models.User).filter(conditions).first()
    validated_credentials =  (user is not None and utils.verify(user_credentials.password, user.password))
    if not validated_credentials:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    token = oauth2.create_access_token({
        "user_id" : user.id
    })
    oauth2.update_user_login_data(user, token)
    return {"access_token" : access_token}

@router.post("/signUp", response_model=sechemaes.UserGet, status_code=status.HTTP_201_CREATED)
def create_user(user_details: sechemaes.UserCreate
                , db: Session = Depends(database.get_db)
                ):
    if is_user_exists(user_details):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with provided details already exists")
    new_user = models.User(**user_details.dict())
    db.add(new_user)
    db.commit()
    db.refresh()
    return new_user