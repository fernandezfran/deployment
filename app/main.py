import typing as t

import fastapi
import fastapi.middleware.cors
import loguru

from app.api import api_router
from app.config import settings, setup_app_logging

# setup logging as early as possible
setup_app_logging(config=settings)


app = fastapi.FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

root_router = fastapi.APIRouter()


@root_router.get("/")
def index(request: fastapi.Request) -> t.Any:
    """Basic HTML response."""
    body = (
        "<html>"
        "<body style='padding: 10px;'>"
        "<h1>Welcome to the API</h1>"
        "<div>"
        "Check the docs: <a href='/docs'>here</a>"
        "</div>"
        "</body>"
        "</html>"
    )

    return fastapi.responses.HTMLResponse(content=body)


app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        fastapi.middleware.cors.CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


if __name__ == "__main__":
    # Use this for debugging purposes only
    loguru.logger.warning(
        "Running in development mode. Do not run like this in production."
    )
    import uvicorn

    uvicorn.run(app, host="localhost", port=8001, log_level="debug")
