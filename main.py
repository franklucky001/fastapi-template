from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from project_dummy.errors import SerializedException
from api.error_handlers import http_error_handler, validation_error_handler, common_error_handler
from api.routes import *
from config import app_config


def create_application() -> FastAPI:
    application = FastAPI(
        title=app_config.PROJECT_NAME,
        debug=app_config.DEBUG,
        version=app_config.VERSION
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=app_config.ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(SerializedException, common_error_handler)
    application.add_exception_handler(RequestValidationError, validation_error_handler)
    application.include_router(index_router)
    return application


app = create_application()



