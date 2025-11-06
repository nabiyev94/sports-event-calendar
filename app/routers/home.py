# app/routers/home.py
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

INDEX_HTML = """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8"/>
    <title>Sports Event Calendar</title>
    <style>
      body { font-family: system-ui, sans-serif; margin: 24px; max-width: 1100px; }
      nav { margin-bottom: 16px; }
      table { border-collapse: collapse; width: 100%; }
      th, td { border: 1px solid #ddd; padding: 8px; }
      th { background: #f5f5f5; text-align: left; }
      .muted { color: #666; }
      a { margin-right: 10px; }
      .btn { padding: 6px 10px; border: 1px solid #ccc; background:#fafafa; cursor:pointer; }
    </style>
  </head>
  <body>
    <nav>
      <strong>Sports Calendar</strong> |
      <a href="/">Home</a>
      <a href="/add">Add Event</a>
      <a href="/about">About</a>
    </nav>
    <h1>Upcoming Events</h1>
    <div style="margin:8px 0 16px;">
      <label>Filter by sport:
        <input id="sportFilter" placeholder="e.g. Football"/>
      </label>
      <button class="btn" onclick="load()">Apply</button>
    </div>
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
        const sport = document.getElementById('sportFilter').value.trim();
        const url = sport ? '/events?sport=' + encodeURIComponent(sport) : '/events';
        const res = await fetch(url);
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

ADD_HTML = """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8"/>
    <title>Add Event — Sports Calendar</title>
    <style>
      body { font-family: system-ui, sans-serif; margin: 24px; max-width: 720px; }
      nav { margin-bottom: 16px; }
      form { display: grid; grid-template-columns: 1fr 1fr; gap: 12px 16px; }
      label { display: flex; flex-direction: column; font-weight: 600; }
      input, textarea, select { padding: 8px; font: inherit; }
      .full { grid-column: 1 / -1; }
      .row { display:flex; gap:12px; }
      .muted { color: #666; font-weight: normal; }
      .btn { padding: 8px 12px; border: 1px solid #ccc; background:#fafafa; cursor:pointer; }
      .error { color: #b00020; margin-top: 10px; }
      .ok { color: #0a7a0a; margin-top: 10px; }
    </style>
  </head>
  <body>
    <nav>
      <strong>Sports Calendar</strong> |
      <a href="/">Home</a>
      <a href="/add">Add Event</a>
      <a href="/about">About</a>
    </nav>

    <h1>Add Event</h1>
    <p class="muted">Note: <em>Sport</em> and <em>Team</em> names must already exist in the database (from your seed data).</p>

    <form id="f">
      <label>Sport
        <input name="sport" placeholder="Football" required />
      </label>
      <label>Date & Time
        <input name="starts_at" type="datetime-local" required />
      </label>

      <label>Home team
        <input name="home_team" placeholder="Salzburg" required />
      </label>
      <label>Opponent team
        <input name="opponent_team" placeholder="Sturm" required />
      </label>

      <label>Venue <span class="muted">(optional)</span>
        <input name="venue" placeholder="Red Bull Arena" />
      </label>
      <label>City <span class="muted">(optional)</span>
        <input name="city" placeholder="Salzburg" />
      </label>

      <label>Country (2-letter) <span class="muted">(optional)</span>
        <input name="country" maxlength="2" placeholder="AT" />
      </label>
      <label class="full">Description <span class="muted">(optional)</span>
        <textarea name="description" rows="3" placeholder="Opening match of the season"></textarea>
      </label>

      <div class="row full">
        <button class="btn" type="button" onclick="submitForm()">Create</button>
        <a class="btn" href="/">Cancel</a>
      </div>
      <div id="msg" class="full"></div>
    </form>

    <script>
      function toISOWithTZ(dtLocalValue) {
        const [date, time] = dtLocalValue.split('T');
        if (!date || !time) return null;
        const dt = new Date(dtLocalValue);
        const pad = n => String(n).padStart(2,'0');
        const offMin = -dt.getTimezoneOffset();
        const sign = offMin >= 0 ? '+' : '-';
        const abs = Math.abs(offMin);
        const offH = pad(Math.floor(abs/60));
        const offM = pad(abs % 60);
        return `${dt.getFullYear()}-${pad(dt.getMonth()+1)}-${pad(dt.getDate())}T${pad(dt.getHours())}:${pad(dt.getMinutes())}:${pad(dt.getSeconds())}${sign}${offH}:${offM}`;
      }

      async function submitForm() {
        const form = document.getElementById('f');
        const msg = document.getElementById('msg');
        msg.className = ''; msg.textContent = '';

        const data = Object.fromEntries(new FormData(form).entries());
        if (!data.sport || !data.home_team || !data.opponent_team || !data.starts_at) {
          msg.className = 'error'; msg.textContent = 'Please fill all required fields.'; return;
        }
        const iso = toISOWithTZ(data.starts_at);
        if (!iso) { msg.className='error'; msg.textContent='Invalid date/time.'; return; }

        const payload = {
          sport: data.sport.trim(),
          home_team: data.home_team.trim(),
          opponent_team: data.opponent_team.trim(),
          starts_at: iso,
          venue: (data.venue || '').trim() || null,
          city: (data.city || '').trim() || null,
          country: (data.country || '').trim() || null,
          description: (data.description || '').trim() || null
        };

        try {
          const res = await fetch('/events', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
          });
          if (!res.ok) {
            const err = await res.json().catch(()=>({detail:'Unknown error'}));
            throw new Error(err.detail || ('HTTP ' + res.status));
          }
          msg.className = 'ok';
          msg.textContent = 'Event created. Redirecting…';
          setTimeout(()=> location.href = '/', 700);
        } catch (e) {
          msg.className = 'error';
          msg.textContent = 'Failed to create event: ' + e.message;
        }
      }
    </script>
  </body>
</html>
"""

ABOUT_HTML = """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8"/>
    <title>About — Sports Event Calendar</title>
    <style>
      body { font-family: system-ui, sans-serif; margin: 24px; max-width: 700px; line-height: 1.6; }
      nav { margin-bottom: 16px; }
      a { margin-right: 10px; }
      .muted { color: #666; }
    </style>
  </head>
  <body>
    <nav>
      <strong>Sports Calendar</strong> |
      <a href="/">Home</a>
      <a href="/add">Add Event</a>
      <a href="/about">About</a>
    </nav>

    <h1>About This Project</h1>
    <p>The <strong>Sports Event Calendar</strong> is a simple full-stack web application created as part of the
    <em>Sportradar Backend Coding Academy</em> challenge. It demonstrates:</p>

    <ul>
      <li>Database modeling and normalization using PostgreSQL.</li>
      <li>Implementation of a FastAPI backend for event management.</li>
      <li>A lightweight HTML frontend to display and add sports events.</li>
      <li>Clean separation of concerns between data models, routes, and services.</li>
    </ul>

    <p>This project showcases core programming skills including REST API design, ORM usage,
    database relationships, and interactive frontend development without heavy frameworks.</p>

    <p class="muted">Developed by <strong>Ramazan Nabiyev</strong> — 2025</p>
  </body>
</html>
"""

@router.get("/", response_class=HTMLResponse)
def index():
    return INDEX_HTML

@router.get("/add", response_class=HTMLResponse)
def add_event():
    return ADD_HTML

@router.get("/about", response_class=HTMLResponse)
def about():
    return ABOUT_HTML