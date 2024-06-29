from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas
from ..auth import get_current_user_dep
from ..database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/donations",
    tags=["donations"],
)

# templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Donation, dependencies=[Depends(get_current_user_dep)])
def create_donation(donation: schemas.DonationCreate, db: Session = Depends(get_db)):
    return crud.create_donation(db=db, donation=donation)

@router.get("/", response_model=List[schemas.Donation], dependencies=[Depends(get_current_user_dep)])
def read_donations(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    donations = crud.get_donations(db, skip=skip, limit=limit)
    return donations


@router.get("/{donation_id}", response_model=schemas.Donation, dependencies=[Depends(get_current_user_dep)])
def read_donation(donation_id: int, db: Session = Depends(get_db)):
    db_donation = crud.get_donation(db, donation_id=donation_id)
    if db_donation is None:
        raise HTTPException(status_code=404, detail="Donation not found")
    return db_donation

@router.get("/template/", response_model=List[schemas.Donation])
def read_children_template(request: Request, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    donations = crud.get_donations(db, skip=skip, limit=limit)
    return templates.TemplateResponse("donations/list.html", {"request": request, "donations": donations})