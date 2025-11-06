from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from .. import models, schemas
from ..crud import resolve_sport, resolve_team_in_sport, get_or_create_venue

def list_events(db: Session, sport: str | None, limit: int, offset: int) -> list[models.Event]:
    base = (
        select(models.Event)
        .options(
            selectinload(models.Event.sport),
            selectinload(models.Event.venue),
            selectinload(models.Event.home_team),
            selectinload(models.Event.opponent_team),
        )
        .order_by(models.Event.starts_at)
        .limit(limit)
        .offset(offset)
    )
    if sport:
        base = (
            select(models.Event)
            .join(models.Event.sport)
            .where(models.Sport.name == sport)
            .options(
                selectinload(models.Event.sport),
                selectinload(models.Event.venue),
                selectinload(models.Event.home_team),
                selectinload(models.Event.opponent_team),
            )
            .order_by(models.Event.starts_at)
            .limit(limit)
            .offset(offset)
        )
    return db.scalars(base).all()

def get_event_by_id(db: Session, event_id: int) -> models.Event | None:
    stmt = (
        select(models.Event)
        .where(models.Event.id == event_id)
        .options(
            selectinload(models.Event.sport),
            selectinload(models.Event.venue),
            selectinload(models.Event.home_team),
            selectinload(models.Event.opponent_team),
        )
    )
    return db.scalars(stmt).first()

def create_event(db: Session, payload: schemas.EventCreate) -> models.Event:
    #  sport must exist
    sport = resolve_sport(db, payload.sport)
    if not sport:
        raise ValueError("Sport does not exist")

    #  teams must exist in that sport and be different
    home = resolve_team_in_sport(db, sport.id, payload.home_team)
    opp  = resolve_team_in_sport(db, sport.id, payload.opponent_team)
    if not home or not opp:
        raise ValueError("Team not found in specified sport")
    if home.id == opp.id:
        raise ValueError("home_team and opponent_team must be different")

    #  venue optional (create if provided)
    venue = None
    if payload.venue:
        venue = get_or_create_venue(db, payload.venue, payload.city, payload.country)

    # persist
    e = models.Event(
        sport_id=sport.id,
        venue_id=venue.id if venue else None,
        starts_at=payload.starts_at,
        description=payload.description,
        home_team_id=home.id,
        opponent_team_id=opp.id,
    )
    db.add(e)
    db.commit()
    db.refresh(e)
    return e