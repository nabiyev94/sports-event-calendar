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

@router.get("/", response_class=HTMLResponse)
def index():
    return INDEX_HTML