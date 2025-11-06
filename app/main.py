from __future__ import annotations
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from .db import get_db
from . import models, schemas
from .crud import resolve_sport, resolve_team_in_sport, get_or_create_venue

app = FastAPI(title="Sports Event Calendar")

# ---- Status check (DB connectivity) ----
@app.get("/status")
def check_status(db: Session = Depends(get_db)):
    # simple lightweight query to ensure connection works
    db.execute(select(models.Sport).limit(1))
    return {"status": "ok"}

# ---- Utility to map ORM to DTO ----
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

# ---- GET /events (list + filter + pagination) ----
@app.get("/events", response_model=list[schemas.EventOut])
def list_events(
    db: Session = Depends(get_db),
    sport: str | None = None,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    stmt = (
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
        stmt = (
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
    rows = db.scalars(stmt).all()
    return [to_event_out(e) for e in rows]

# ---- GET /events/{id} ----
@app.get("/events/{event_id}", response_model=schemas.EventOut)
def get_event(event_id: int, db: Session = Depends(get_db)):
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
    e = db.scalars(stmt).first()
    if not e:
        raise HTTPException(status_code=404, detail="Event not found")
    return to_event_out(e)

# ---- POST /events ----
@app.post("/events", response_model=schemas.EventOut, status_code=201)
def create_event(payload: schemas.EventCreate, db: Session = Depends(get_db)):
    # 1) sport must exist
    sport = resolve_sport(db, payload.sport)
    if not sport:
        raise HTTPException(status_code=400, detail="Sport does not exist")

    # 2) teams must exist in that sport and be different
    home = resolve_team_in_sport(db, sport.id, payload.home_team)
    opp  = resolve_team_in_sport(db, sport.id, payload.opponent_team)
    if not home or not opp:
        raise HTTPException(status_code=400, detail="Team not found in specified sport")
    if home.id == opp.id:
        raise HTTPException(status_code=400, detail="home_team and opponent_team must be different")

    # 3) venue is optional: find or create
    venue = get_or_create_venue(db, payload.venue, payload.city, payload.country) if payload.venue else None

    # 4) persist
    e = models.Event(
        sport_id=sport.id,
        venue_id=venue.id if venue else None,
        starts_at=payload.starts_at,  # timezone-aware datetime expected by schema
        description=payload.description,
        home_team_id=home.id,
        opponent_team_id=opp.id,
    )
    db.add(e)
    db.commit()
    db.refresh(e)

    # load relationships for response
    db.refresh(e)
    return to_event_out(e)

# ---- Minimal Frontend: "/" lists events in a table ----
INDEX_HTML = """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8"/>
    <title>Sports Event Calendar</title>
    <style>
      body { font-family: system-ui, sans-serif; margin: 24px; }
      nav { margin-bottom: 16px; }
      table { border-collapse: collapse; width: 100%; }
      th, td { border: 1px solid #ddd; padding: 8px; }
      th { background: #f5f5f5; text-align: left; }
      .muted { color: #666; }
    </style>
  </head>
  <body>
    <nav>
      <strong>Sports Calendar</strong> |
      <a href="/">Home</a> |
      <a href="#" class="muted">Add Event (placeholder)</a> |
      <a href="#" class="muted">About (placeholder)</a>
    </nav>
    <h1>Upcoming Events</h1>
    <table id="events">
      <thead>
        <tr>
          <th>#</th>
          <th>Date/Time</th>
          <th>Sport</th>
          <th>Home</th>
          <th>Opponent</th>
          <th>Venue</th>
          <th>City</th>
          <th>Country</th>
          <th>Description</th>
        </tr>
      </thead>
      <tbody></tbody>
    </table>
    <script>
      async function load() {
        const res = await fetch('/events');
        const data = await res.json();
        const tb = document.querySelector('#events tbody');
        tb.innerHTML = '';
        data.forEach((e, idx) => {
          const tr = document.createElement('tr');
          tr.innerHTML = `
            <td>${idx + 1}</td>
            <td>${new Date(e.starts_at).toLocaleString()}</td>
            <td>${e.sport}</td>
            <td>${e.home_team}</td>
            <td>${e.opponent_team}</td>
            <td>${e.venue ?? ''}</td>
            <td>${e.city ?? ''}</td>
            <td>${e.country ?? ''}</td>
            <td>${e.description ?? ''}</td>
          `;
          tb.appendChild(tr);
        });
      }
      load();
    </script>
  </body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def index():
    return INDEX_HTML
