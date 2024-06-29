from pydantic import BaseModel, EmailStr
from typing import List, Optional

class ChildBase(BaseModel):
    name: str
    age: int
    gender: str
    address: str
    school: str

class ChildCreate(ChildBase):
    pass

class Child(ChildBase):
    id: int

    class Config:
        from_attributes = True

class DonorBase(BaseModel):
    name: str
    email: str
    phone: str
    address: str

class DonorCreate(DonorBase):
    pass

class Donor(DonorBase):
    id: int

    class Config:
        from_attributes = True

class DonationBase(BaseModel):
    donor_id: int
    child_id: int
    amount: float
    date: str

class DonationCreate(DonationBase):
    pass

class Donation(DonationBase):
    id: int

    class Config:
        from_attributes = True

class User(BaseModel):
    id: str
    name: Optional[str] = None
    email: EmailStr
    picture: Optional[str] = None

    class Config:
        from_attributes = True
