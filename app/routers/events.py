from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..db import get_db
from .. import schemas
from ..services import events_service
from ..mappers.event_mapper import to_event_out

router = APIRouter()

@router.get("/events", response_model=list[schemas.EventOut])
def list_events(
    db: Session = Depends(get_db),
    sport: str | None = None,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    rows = events_service.list_events(db, sport=sport, limit=limit, offset=offset)
    return [to_event_out(e) for e in rows]

@router.get("/events/{event_id}", response_model=schemas.EventOut)
def get_event(event_id: int, db: Session = Depends(get_db)):
    e = events_service.get_event_by_id(db, event_id)
    if not e:
        raise HTTPException(status_code=404, detail="Event not found")
    return to_event_out(e)

@router.post("/events", response_model=schemas.EventOut, status_code=201)
def create_event(payload: schemas.EventCreate, db: Session = Depends(get_db)):
    try:
        e = events_service.create_event(db, payload)
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))
    return to_event_out(e)