from pydantic import BaseModel, EmailStr


class AuthSchema(BaseModel):
    email: EmailStr
    password: str


class UpdatePasswordSchema(BaseModel):
    old_password: str
    new_password: str


class Token(BaseModel):
    access_token: str
    token_type: str
