from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from passlib.context import CryptContext
from pydantic import BaseModel

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:password@127.0.0.1:5432/db_name"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
class SetBaseModel(BaseModel):
    class Config:
        orm_mode = True
        
class Settings(BaseModel):
    authjwt_secret_key: str= "secret"
    authjwt_token_location: set= {"cookies"}
    authjwt_cookie_domain: str=".127.0.0.1"
    authjwt_cookie_secure: bool=True
    authjwt_cookie_samesite: str="lax"
    authjwt_cookie_csrf_protect:bool=False
    
class AuthHandler():
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    def get_pwd_hash(self, password):
        return self.pwd_context.hash(password)
    def verify_pwd(self, plain_pwd, hashed_pwd):
        return self.pwd_context.verify(plain_pwd, hashed_pwd)        
