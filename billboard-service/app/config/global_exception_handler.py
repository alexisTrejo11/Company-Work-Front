from http import HTTPStatus
from fastapi import FastAPI, Request
from app.shared.exceptions import DomainException, ApplicationException
from fastapi.responses import JSONResponse
import logging

app = FastAPI()

@app.exception_handler(DomainException)
async def handle_domain_exceptions(request: Request, exc: DomainException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.error_code,
                "message": exc.message,
                "details": exc.details
            }
        }
    )

@app.exception_handler(ApplicationException)
async def handle_application_exceptions(request: Request, exc: ApplicationException):
    logging.error(f"Application error: {exc}", exc_info=exc)
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.error_code,
                "message": "An internal error occurred"  
            }
        }
    )

@app.exception_handler(Exception)
async def handle_generic_exceptions(request: Request, exc: Exception):
    logging.error(f"Unexpected error: {exc}", exc_info=exc)
    
    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred"
            }
        }
    )
