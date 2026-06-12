from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request

from app.api.routes.admin import (
    vehicles,
    allocations,
    fleet,
    dashboard,
    analytics,
    optimization,
    routes,
    audit,
)
from app.api.routes.driver import deliveries, tracking, shifts, incidents
from app.events.register import register_events
from app.core.exceptions import (
    FleetPandaException,
    fleet_exception_handler,
)

app = FastAPI(title="FleetPanda API")


app.include_router(vehicles.router)
app.include_router(allocations.router)
app.include_router(deliveries.router)
app.include_router(tracking.router)
app.include_router(shifts.router)
app.include_router(fleet.router)
app.include_router(incidents.router)
app.include_router(dashboard.router)
app.include_router(analytics.router)
app.include_router(optimization.router)
app.include_router(routes.router)
app.include_router(audit.router)

app.add_exception_handler(
    FleetPandaException,
    fleet_exception_handler,
)


@app.get("/")
def health():

    return {"system": "FleetPanda", "version": "1.0", "status": "running"}


@app.on_event("startup")
def startup():

    register_events()


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):

    print("ERROR:", exc)

    return JSONResponse(status_code=500, content={"error": str(exc)})