from sqlalchemy.orm import Session
from sqlalchemy import select
from . import models

def get_or_create_venue(db: Session, name: str | None, city: str | None, country: str | None):
    if not name:
        return None
    v = db.scalars(select(models.Venue).where(models.Venue.name == name)).first()
    if v:
        return v
    v = models.Venue(name=name, city=city, country=country)
    db.add(v)
    db.flush()
    return v

def resolve_sport(db: Session, sport_name: str) -> models.Sport | None:
    return db.scalars(select(models.Sport).where(models.Sport.name == sport_name)).first()

def resolve_team_in_sport(db: Session, sport_id: int, team_name: str) -> models.Team | None:
    return db.scalars(
        select(models.Team).where(
            models.Team.sport_id == sport_id,
            models.Team.name == team_name
        )
    ).first()