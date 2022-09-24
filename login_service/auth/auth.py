from fastapi import HTTPException, Depends, APIRouter, Response

from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT

from ..models import User
from ..settings import Settings, get_db, AuthHandler
from ..schemas import UserLogin

authlogin = APIRouter()
settings = Settings()
auth_handler = AuthHandler()

@AuthJWT.load_config
def get_config():
    return settings


@authlogin.post('/login/')
async def login(user: UserLogin, response: Response, Authorize: AuthJWT = Depends(), db: Session=Depends(get_db)):
    db_user =  db.query(User).filter(User.username == user.username).first()
    if db_user is None:
        raise HTTPException(status_code=401, detail="Username or Password Invalid")
    else:
        if not auth_handler.verify_pwd(user.password, db_user.password):
            raise HTTPException(status_code=401, detail="Username or Password Invalid")
    access_token = Authorize.create_access_token(subject=db_user.username)
    refresh_token = Authorize.create_refresh_token(subject=db_user.username)
    #response.set_cookie(key="access_token_cookie", value=access_token, max_age=60*60*24, domain="127.0.0.1", path="/", secure=True, httponly=True, samesite="none")
    #response.set_cookie(key="refresh_token_cookie", value=refresh_token, max_age=60*60*24*30, domain="127.0.0.1", path="/", secure=True, httponly=True, samesite="none")
    Authorize.set_access_cookies(access_token, max_age=60*60, response=response)
    Authorize.set_refresh_cookies(refresh_token, max_age=60*60*24*30, response=response)
    return {"username":db_user.username, "access_token":access_token, "refresh_token":refresh_token}
