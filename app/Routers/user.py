from fastapi import FastApi, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


from .. import sechemaes, models, database, oauth2, utils


router = APIRouter(
    prefix="/users", 
    tags=["User"]
)

@router.post("/login", respone_model = sechemaes.Token)
def login(user_credentials : OAuth2PasswordRequestForm = Depends()
          , db: Session = Depends(database.get_db)) :
    """
    OAuth2PasswordRequestForm has only username and password fields
    for my application username can be both email or username
    """
    conditions = or_(models.User.user_name == user_credentials.username, models.User.email == user_credentials.username)
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