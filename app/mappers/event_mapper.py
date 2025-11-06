from .. import models, schemas

def to_event_out(e: models.Event) -> schemas.EventOut:
    return schemas.EventOut(
        id=e.id,
        sport=e.sport.name,
        home_team=e.home_team.name,
        opponent_team=e.opponent_team.name,
        venue=e.venue.name if e.venue else None,
        city=e.venue.city if e.venue else None,
        country=e.venue.country if e.venue else None,
        starts_at=e.starts_at,
        description=e.description
    )