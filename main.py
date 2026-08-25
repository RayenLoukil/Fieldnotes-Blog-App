from contextlib import asynccontextmanager
from fastapi import FastAPI, status, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from config import settings

# database
from database import engine, get_db

# routers
from router import posts, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()

## Initialize the FastAPI app
## Initialize the FastAPI app
app = FastAPI(
    title="Fieldnotes API",
    description="A pure JSON Blog API for posting about tech and sharing knowledge",
    version="1.0.0",
    lifespan=lifespan,
)

# ---------------------------------------------------------
# CORS configuration (Allows React dev server to communicate)
# ---------------------------------------------------------
origins = settings.cors_origins.split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from pathlib import Path
from fastapi.staticfiles import StaticFiles

Path("static/profile_pics").mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")



@app.get("/api/health", tags=["System"])
async def health_check(db: Annotated[AsyncSession, Depends(get_db)]):
    try:
        await db.execute(text("SELECT 1"))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database unreachable"
        )
    return {"status": "healthy", "message": "Fieldnotes API is fully operational"}


# Include API Routers
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(posts.router, prefix="/api/posts", tags=["Posts"])


# ---------------------------------------------------------
# Global JSON Exception Handlers
# ---------------------------------------------------------

@app.exception_handler(StarletteHTTPException)
def http_exception_handler(request: Request, exception: StarletteHTTPException):
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "error": {
                "message": exception.detail,
                "status_code": exception.status_code
            }
        }
    )


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "message": "Validation failed",
                "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                "details": exception.errors()
            }
        }
    )


@app.exception_handler(Exception)
def global_exception_handler(request: Request, exception: Exception):
    # In production, log this exception details to terminal/logs
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "message": "Internal server error",
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
            }
        }
    )