from pydantic import BaseModel
from datetime import date


class AllocationRequest(BaseModel):

    vehicle_id: int

    driver_id: int

    allocation_date: date



class AllocationResponse(BaseModel):

    id: int

    vehicle_id: int

    driver_id: int

    allocation_date: date

    status: str


    class Config:
        from_attributes = True