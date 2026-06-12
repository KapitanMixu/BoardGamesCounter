from pydantic import BaseModel


class ExpansionCreate(BaseModel):
    name: str


class ExpansionUpdate(BaseModel):
    name: str | None = None


class ExpansionOut(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}
