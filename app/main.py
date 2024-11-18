"""
Main app configuration and entry point
"""

from fastapi import FastAPI, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from pydantic_extra_types.phone_numbers import PhoneNumber
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from app.core.config import settings
from app.web_api.v1 import v1_router

PhoneNumber.phone_format = 'E164'

# FastApi config
app = FastAPI(
    debug=settings.DEBUG,
    # title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
    openapi_url="/api/v1/openapi.json" if settings.DEBUG else None,
    redoc_url=None,
    docs_url=None
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD"],
        allow_headers=['Content-Type', 'Authorization'],
    )


@app.get("/api/v1/docs", include_in_schema=False)
async def get_docs():
    """
    Workaround to move docs at /api/v1/docs
    """
    if settings.DEBUG:
        return get_swagger_ui_html(openapi_url="/api/v1/openapi.json",
                                   title="Swagger")
    return HTTPException(status_code=404)


app.include_router(v1_router, prefix="/api/v1")
app.mount('/' + settings.IMAGE_SERVING_LOCATION,
          StaticFiles(directory=settings.IMAGE_STORAGE_LOCATION),
          name="static")
