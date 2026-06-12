from pydantic import BaseModel


class DeliveryStatusUpdate(BaseModel):

    status: str


class DeliveryResponse(BaseModel):

    id: int

    driver_id: int

    status: str

    class Config:
        from_attributes = True