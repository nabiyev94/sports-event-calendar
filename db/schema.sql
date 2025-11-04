BEGIN;

-- 1) Master data
CREATE TABLE sport (
  id   SERIAL PRIMARY KEY,
  name VARCHAR(80) NOT NULL UNIQUE
);

CREATE TABLE team (
  id       SERIAL PRIMARY KEY,
  sport_id INT NOT NULL REFERENCES sport(id),
  name     VARCHAR(120) NOT NULL,
  CONSTRAINT ux_team_name_per_sport UNIQUE (sport_id, name)
);

CREATE TABLE venue (
  id      SERIAL PRIMARY KEY,
  name    VARCHAR(120) NOT NULL,
  city    VARCHAR(120),
  country VARCHAR(2)
);

-- 2) Events
CREATE TABLE event (
  id               SERIAL PRIMARY KEY,
  sport_id         INT NOT NULL REFERENCES sport(id),
  venue_id         INT REFERENCES venue(id),
  starts_at        TIMESTAMPTZ NOT NULL,
  description      TEXT,
  home_team_id     INT NOT NULL REFERENCES team(id),
  opponent_team_id INT NOT NULL REFERENCES team(id),
  CONSTRAINT chk_event_distinct_teams CHECK (home_team_id <> opponent_team_id)
);

-- 3) Performance indexes
CREATE INDEX ix_event_sport      ON event(sport_id);
CREATE INDEX ix_event_venue      ON event(venue_id);
CREATE INDEX ix_event_starts_at  ON event(starts_at);

-- 4) Enforce “teams belong to the event’s sport” (composite FKs)
--    Make (team.id, team.sport_id) unique, then reference it from event.
CREATE UNIQUE INDEX ux_team_id_sport ON team(id, sport_id);

ALTER TABLE event
  ADD CONSTRAINT fk_event_home_team_same_sport
  FOREIGN KEY (home_team_id, sport_id)
  REFERENCES team(id, sport_id),
  ADD CONSTRAINT fk_event_opponent_team_same_sport
  FOREIGN KEY (opponent_team_id, sport_id)
  REFERENCES team(id, sport_id);

COMMIT;