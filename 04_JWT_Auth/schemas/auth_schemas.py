from pydantic import BaseModel


class SignupRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email : str
    password : str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


    
