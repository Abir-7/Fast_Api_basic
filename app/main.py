from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from app.controller.auth_controller import router as user_route
from app.core.database import init_db
from contextlib import asynccontextmanager



app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # This runs on startup
    await init_db()
    yield
    # This runs on shutdown (optional cleanup)


app.include_router(user_route)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.exception_handler(IntegrityError)
async def db_integrity_error_handler(request: Request, exc: IntegrityError):
    detail = str(exc.orig)
    if "email" in detail.lower():  # handles duplicate email
        return JSONResponse(status_code=400, content={"detail": "Email already exists"})
    return JSONResponse(status_code=500, content={"detail": f"Database error: {detail}"})


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500,content={"detail": f"Unexpected error: {str(exc)}"})



