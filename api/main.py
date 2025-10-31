from fastapi import FastAPI
from postgres_version.routers import earthquake_routes as pg_routes
from mongo_version.routers import earthquake_routes as mongo_routes

app = FastAPI(title="Earthquake API (Postgres + Mongo)")

# Mount both routes
app.include_router(pg_routes.router, prefix="/postgres", tags=["PostgreSQL"])
app.include_router(mongo_routes.router, prefix="/mongo", tags=["MongoDB"])

@app.get("/")
def root():
    return {"message": "Welcome to Earthquake API"}
