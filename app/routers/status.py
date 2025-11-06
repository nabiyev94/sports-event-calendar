from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..db import get_db
from .. import models

router = APIRouter()

@router.get("/status")
def check_status(db: Session = Depends(get_db)):
    db.execute(select(models.Sport).limit(1))
    return {"status": "ok"}