from typing import List
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from .. import crud, models, schemas
from ..auth import get_current_user_dep
from ..database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/children",
    tags=["children"]
)

templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Child, dependencies=[Depends(get_current_user_dep)])
def create_child(child: schemas.ChildCreate, db: Session = Depends(get_db)):
    return crud.create_child(db=db, child=child)


@router.get("/", response_model=List[schemas.Child], dependencies=[Depends(get_current_user_dep)])
def read_children(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    children = crud.get_children(db, skip=skip, limit=limit)
    return children


@router.get("/{child_id}", response_model=schemas.Child, dependencies=[Depends(get_current_user_dep)])
def read_child(child_id: int, db: Session = Depends(get_db), ):
    db_child = crud.get_child(db, child_id=child_id)
    if db_child is None:
        raise HTTPException(status_code=404, detail="Child not found")
    return db_child

@router.get("/template/", response_model=List[schemas.Child])
def read_children_template(request: Request, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    children = crud.get_children(db, skip=skip, limit=limit)
    return templates.TemplateResponse("children/list.html", {"request": request, "children": children})
