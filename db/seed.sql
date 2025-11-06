-- Sports Event Calendar — sample data .

BEGIN;

-- Sports
INSERT INTO sport (name) VALUES ('Football'), ('Ice Hockey');

-- Teams (unique per spor	t)
INSERT INTO team (sport_id, name)
VALUES
  ((SELECT id FROM sport WHERE name = 'Football'),  'Salzburg'),
  ((SELECT id FROM sport WHERE name = 'Football'),  'Sturm'),
  ((SELECT id FROM sport WHERE name = 'Ice Hockey'),'KAC'),
  ((SELECT id FROM sport WHERE name = 'Ice Hockey'),'Capitals');

-- Venues (example)
INSERT INTO venue (name, city, country)
VALUES
  ('Red Bull Arena', 'Salzburg', 'AT'),
  ('Eisarena',       'Klagenfurt', 'AT');

-- Events
-- Sat., 18.07.2025, 18:30, Football, Salzburg vs. Sturm
INSERT INTO event (sport_id, venue_id, starts_at, description, home_team_id, opponent_team_id)
VALUES (
  (SELECT id FROM sport WHERE name='Football'),
  (SELECT id FROM venue WHERE name='Red Bull Arena'),
  '2025-07-18 18:30:00+02',
  'League fixture',
  (SELECT t.id FROM team t JOIN sport s ON s.id=t.sport_id WHERE s.name='Football'   AND t.name='Salzburg'),
  (SELECT t.id FROM team t JOIN sport s ON s.id=t.sport_id WHERE s.name='Football'   AND t.name='Sturm')
);

-- Sun., 23.10.2025, 09:45, Ice Hockey, KAC vs. Capitals
INSERT INTO event (sport_id, venue_id, starts_at, description, home_team_id, opponent_team_id)
VALUES (
  (SELECT id FROM sport WHERE name='Ice Hockey'),
  (SELECT id FROM venue WHERE name='Eisarena'),
  '2025-10-23 09:45:00+02',
  'Regular season',
  (SELECT t.id FROM team t JOIN sport s ON s.id=t.sport_id WHERE s.name='Ice Hockey' AND t.name='KAC'),
  (SELECT t.id FROM team t JOIN sport s ON s.id=t.sport_id WHERE s.name='Ice Hockey' AND t.name='Capitals')
);

COMMIT;