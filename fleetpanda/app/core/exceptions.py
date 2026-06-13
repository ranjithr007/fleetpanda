from fastapi import Request
from fastapi.responses import JSONResponse


class FleetPandaException(Exception):

    def __init__(
        self,
        error_code: str,
        message: str,
        status_code: int = 400,
    ):
        self.error_code = error_code
        self.message = message
        self.status_code = status_code


class NotFoundException(FleetPandaException):

    def __init__(self, error_code, message="Resource not found"):
        super().__init__(
            error_code=error_code,
            message=message,
            status_code=404,
        )


class ConflictException(FleetPandaException):

    def __init__(self, error_code, message="Business conflict"):
        super().__init__(
            error_code=error_code,
            message=message,
            status_code=409,
        )


class ValidationException(FleetPandaException):

    def __init__(self, error_code, message="Validation failed"):
        super().__init__(
            error_code=error_code,
            message=message,
            status_code=400,
        )

class AccessDeniedException(FleetPandaException):

    def __init__(self, error_code, message="Access denied"):
        super().__init__(
            error_code=error_code,
            message=message,
            status_code=403,
        )
async def fleet_exception_handler(
    request: Request,
    exc: FleetPandaException,
):

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error_code": exc.error_code,
            "message": exc.message,
            "path": str(request.url.path),
        },
    )