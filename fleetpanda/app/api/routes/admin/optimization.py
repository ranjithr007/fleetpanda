from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session


from app.database.session import get_db
from app.services.optimization_service import OptimizationService

router = APIRouter(prefix="/optimization", tags=["Optimization"])


@router.get("/drivers/recommend")
def recommend_driver(db: Session = Depends(get_db)):

    return OptimizationService(db).recommend_driver()


@router.get("/vehicles/recommend")
def recommend_vehicle(db: Session = Depends(get_db)):

    return OptimizationService(db).recommend_vehicle()