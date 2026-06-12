from pydantic import BaseModel


class ShiftStartRequest(BaseModel):

    driver_id: int

    vehicle_id: int