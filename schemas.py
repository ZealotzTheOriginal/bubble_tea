from pydantic import BaseModel

class BubbleTeaCreate(BaseModel):
    name: str
    temperature: str
    price: float
    active: bool = True

class BubbleTeaResponse(BaseModel):
    id: int
    name: str
    temperature: str
    price: float
    active: bool

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: int
    name: str
    surname: str
    email: str

    class Config:
        from_attributes = True