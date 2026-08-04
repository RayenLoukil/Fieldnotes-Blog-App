from fastapi import FastAPI, status

## database
from database import  engine , Base

#routers
from router import posts , users


## Create the database tables
Base.metadata.create_all(bind=engine)

## Initialize the FastAPI app
app = FastAPI(
    title="Fieldnotes API",
    description="A Blog API for posting about tech and sharing knowledge",
    version="1.0.0",
)

@app.get("/")
def health_check():
    return {"message" : "ok"}



app.include_router(users.router , prefix="/api/users" , tags=["Users"])
app.include_router(posts.router , prefix="/api/posts" , tags=["Posts"])




#HTTP Exception Handler 
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi import Request

#Validation Error Handler
from fastapi.exceptions import RequestValidationError 


# Global HTTP Exception Handler
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


# Global Validation Error Handler
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


# Global Unexpected Error Handler
@app.exception_handler(Exception)
def global_exception_handler(request: Request, exception: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "message": "Internal server error",
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
            }
        }
    )
    
    
