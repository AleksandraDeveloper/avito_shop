from pydantic import BaseModel, Field, ConfigDict

class SendCoinRequest(BaseModel):
    toUser: str
    amount: int = Field(gt=0)
    model_config = ConfigDict(from_attributes=True)