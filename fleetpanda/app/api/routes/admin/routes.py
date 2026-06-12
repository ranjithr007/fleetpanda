from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session


from app.database.session import get_db

from app.services.route_service import RouteService

router = APIRouter(prefix="/routes", tags=["Route Optimization"])


@router.post("/optimize/{shift_id}")
def optimize(shift_id: int, db: Session = Depends(get_db)):

    return RouteService(db).optimize_route(shift_id)