from pydantic import BaseModel


class VehicleResponse(BaseModel):

    id: int

    vehicle_number: str

    status: str

    class Config:
        from_attributes = True