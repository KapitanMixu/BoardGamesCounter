from pydantic import BaseModel


class PlayerCreate(BaseModel):
    name: str


class PlayerOut(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}
