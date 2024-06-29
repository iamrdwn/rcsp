from sqlalchemy.orm import Session
from . import models, schemas

def get_child(db: Session, child_id: int):
    return db.query(models.Child).filter(models.Child.id == child_id).first()

def get_children(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Child).offset(skip).limit(limit).all()

def create_child(db: Session, child: schemas.ChildCreate):
    db_child = models.Child(**child.dict())
    db.add(db_child)
    db.commit()
    db.refresh(db_child)
    return db_child

def get_donor(db: Session, donor_id: int):
    return db.query(models.Donor).filter(models.Donor.id == donor_id).first()

def get_donors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Donor).offset(skip).limit(limit).all()

def create_donor(db: Session, donor: schemas.DonorCreate):
    db_donor = models.Donor(**donor.dict())
    db.add(db_donor)
    db.commit()
    db.refresh(db_donor)
    return db_donor

def get_donation(db: Session, donation_id: int):
    return db.query(models.Donation).filter(models.Donation.id == donation_id).first()

def get_donations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Donation).offset(skip).limit(limit).all()

def create_donation(db: Session, donation: schemas.DonationCreate):
    db_donation = models.Donation(**donation.dict())
    db.add(db_donation)
    db.commit()
    db.refresh(db_donation)
    return db_donation
