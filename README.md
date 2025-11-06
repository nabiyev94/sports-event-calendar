# 🏟️ Sports event calendar that allows events to be added and categorized based on  sports.

A simple full-stack web application for managing and displaying sports events.  
It was created as a challenge to demonstrate backend design, database modeling, and web development skills using **Python (FastAPI)** and **PostgreSQL**.

---

## 📘 Overview

The Sports Event Calendar allows users to:
- View all upcoming sports events.
- Filter events by sport type.
- Add new events through an HTML form or API endpoint.
- Access data served from a relational database.

The backend is implemented with **FastAPI** and **SQLAlchemy ORM**.  
The frontend is a lightweight HTML interface rendered directly by FastAPI.

---

## 🧩 Features

- PostgreSQL database designed in **3rd Normal Form (3NF)**  
- Entity-Relationship Diagram (ERD) with four core tables:
  - `sport`, `team`, `venue`, and `event`
- REST API:
  - `GET /events` – list or filter events  
  - `GET /events/{id}` – get a single event  
  - `POST /events` – create a new event  
  - `GET /status` – check database connection  
- Frontend pages:
  - `/` – list events  
  - `/add` – add a new event  
  - `/about` – project information

---

### Technical Decisions and Assumptions

FastAPI was chosen for its speed, clarity, and automatic documentation.

SQLAlchemy ORM provides clear object-relational mapping and minimizes raw SQL.

PostgreSQL was chosen for its reliability and strong relational integrity features.

Minimal Frontend was kept HTML-only (no frameworks) for simplicity and transparency.

The Sportradar style guide suggests using an underscore prefix for foreign key columns (for example: _sport_id, _venue_id, _home_team_id, _opponent_team_id). But in this implementation, standard modern naming is applied instead (e.g., sport_id, venue_id, home_team_id, opponent_team_id) to ensure clarity and compatibility with common ORM frameworks (such as SQLAlchemy and Django ORM).

Both conventions are functionally equivalent — the chosen style prioritizes readability, maintainability, and industry-standard practices.

### 🧠 Future Improvements

If given more time, I would do the following things:

Adding user authentication and role-based permissions.

Enabling editing/deleting events.

Adding a proper frontend using React or Vue.

Deploying on Docker + Render or Railway.

Writing tests to verify my code works as expected. For example, I would involve unit tests in the process.

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/sports-event-calendar.git
cd sports-event-calendar


### 2️⃣ Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # (on Windows: venv\Scripts\activate)

### 3️⃣ Install dependencies
pip install -r requirements.txt

### 4️⃣ Set up the database

Make sure PostgreSQL is installed and running locally.

Create a database (you can use pgAdmin or psql):

CREATE DATABASE sports_calendar;


Then run the schema and seed data:

psql -U postgres -d sports_calendar -f db/schema.sql
psql -U postgres -d sports_calendar -f db/seed.sql

### 5️⃣ Configure environment

Create a file named .env in the project root:

DATABASE_URL=postgresql+psycopg://postgres:<YourPassword>@localhost:5432/sports_calendar


###.6️⃣ Run the app
uvicorn app.main:app --reload


Visit the app:

Home → http://127.0.0.1:8000

Add Event → http://127.0.0.1:8000/add

About → http://127.0.0.1:8000/about

Docs (Swagger UI) → http://127.0.0.1:8000/docs