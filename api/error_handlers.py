from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from project_dummy.errors import SerializedException
from config import logger


def http_error_handler(_: Request, exc: HTTPException) -> JSONResponse:
    logger.warning(f"http error, {exc.detail}")
    return JSONResponse({
        "code": 1,
        "message": "http error",
        "data": None,
    },
        status_code=exc.status_code
    )


def validation_error_handler(
    _: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    logger.warning(f"validation error, {exc.errors()}")
    return JSONResponse(
        {
            "code": 2,
            "message": "validation error",
            "data": None
        },
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
    )


def common_error_handler(
    _: Request,
    exc: SerializedException,
) -> JSONResponse:
    error_resp = exc.serialize()
    logger.warning(f"error resp with traceback {error_resp}")
    return JSONResponse({
        "code": error_resp['code'],
        "message": error_resp['message'],
        "data": None
    }, status_code=500)
