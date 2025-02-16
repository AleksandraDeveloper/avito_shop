from pydantic import BaseModel, ConfigDict

class AuthRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str
    password: str

class AuthResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    token: str