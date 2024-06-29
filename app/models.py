from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from .database import Base

class Child(Base):
    __tablename__ = "children"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    gender = Column(String)
    address = Column(String)
    school = Column(String)

class Donor(Base):
    __tablename__ = "donors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    address = Column(String)

class Donation(Base):
    __tablename__ = "donations"

    id = Column(Integer, primary_key=True, index=True)
    donor_id = Column(Integer, ForeignKey("donors.id"))
    child_id = Column(Integer, ForeignKey("children.id"))
    amount = Column(Float)
    date = Column(String)

    donor = relationship("Donor", back_populates="donations")
    child = relationship("Child", back_populates="donations")

Donor.donations = relationship("Donation", back_populates="donor")
Child.donations = relationship("Donation", back_populates="child")
