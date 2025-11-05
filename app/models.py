# app/models.py
from __future__ import annotations
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, UniqueConstraint

Base = declarative_base()

class Sport(Base):
    __tablename__ = "sport"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)

    teams = relationship("Team", back_populates="sport")
    events = relationship("Event", back_populates="sport")


class Team(Base):
    __tablename__ = "team"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sport_id: Mapped[int] = mapped_column(ForeignKey("sport.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)

    __table_args__ = (
        UniqueConstraint("sport_id", "name", name="ux_team_name_per_sport"),
    )

    sport = relationship("Sport", back_populates="teams")
    home_events = relationship("Event", foreign_keys="Event.home_team_id", back_populates="home_team")
    opponent_events = relationship("Event", foreign_keys="Event.opponent_team_id", back_populates="opponent_team")


class Venue(Base):
    __tablename__ = "venue"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    city: Mapped[str | None] = mapped_column(String(120))
    country: Mapped[str | None] = mapped_column(String(2))

    events = relationship("Event", back_populates="venue")


class Event(Base):
    __tablename__ = "event"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sport_id: Mapped[int] = mapped_column(ForeignKey("sport.id"), nullable=False)
    venue_id: Mapped[int | None] = mapped_column(ForeignKey("venue.id"))
    starts_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    home_team_id: Mapped[int] = mapped_column(ForeignKey("team.id"), nullable=False)
    opponent_team_id: Mapped[int] = mapped_column(ForeignKey("team.id"), nullable=False)

    sport = relationship("Sport", back_populates="events")
    venue = relationship("Venue", back_populates="events")
    home_team = relationship("Team", foreign_keys=[home_team_id])
    opponent_team = relationship("Team", foreign_keys=[opponent_team_id])