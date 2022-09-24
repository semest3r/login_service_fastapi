from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session
from fastapi_jwt_auth.exceptions import AuthJWTException
from .settings import SessionLocal, engine
from .auth.auth import authlogin
from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
app.include_router(authlogin)