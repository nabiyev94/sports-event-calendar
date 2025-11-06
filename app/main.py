from fastapi import FastAPI
from .routers import status, events, home

app = FastAPI(title="Sports Event Calendar")

app.include_router(status.router)
app.include_router(events.router)
app.include_router(home.router)