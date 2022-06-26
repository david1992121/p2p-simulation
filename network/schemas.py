from pydantic import BaseModel, Field


class JoinInfo(BaseModel):
    capacity: int = Field(default=0, title="Capacity of the node", le=3, ge=0)


class LeaveInfo(BaseModel):
    id: int = Field(title="Identifier of the node to remove", gt=0)
