from fastapi import APIRouter, Depends, HTTPException, Request, Security
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas
from ..auth import get_current_user, get_current_user_dep
from ..database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/donors",
    tags=["donors"])

templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Donor, dependencies=[Depends(get_current_user_dep)])
def create_donor(donor: schemas.DonorCreate,  db: Session = Depends(get_db)):
    return crud.create_donor(db=db, donor=donor)

@router.get("/", response_model=List[schemas.Donor], dependencies=[Depends(get_current_user_dep)])
def read_donors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    donors = crud.get_donors(db, skip=skip, limit=limit)
    return donors

@router.get("/{donor_id}", response_model=schemas.Donor, dependencies=[Depends(get_current_user_dep)])
def read_donor(donor_id: int, db: Session = Depends(get_db)):
    db_donor = crud.get_donor(db, donor_id=donor_id)
    if db_donor is None:
        raise HTTPException(status_code=404, detail="Donor not found")
    return db_donor

@router.get("/template/")
def read_children_template(request: Request, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    donors = crud.get_donors(db, skip=skip, limit=limit)
    return templates.TemplateResponse("donors/list.html", {"request": request, "donors": donors})
