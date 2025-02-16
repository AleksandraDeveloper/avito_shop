from pydantic import BaseModel, ConfigDict

class ErrorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    detail: str