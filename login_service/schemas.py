from .settings import SetBaseModel

class UserLogin(SetBaseModel):
    username : str
    password : str