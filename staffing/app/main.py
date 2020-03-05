from fastapi import FastAPI

from starlette.requests import Request
from starlette.responses import Response
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_204_NO_CONTENT,
    HTTP_301_MOVED_PERMANENTLY,
    HTTP_304_NOT_MODIFIED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_405_METHOD_NOT_ALLOWED,
)

from database.database import get_db
from staff.routers import router as staff_router
from client.routers import router as client_router

#inits
app = FastAPI()

#include routers
app.include_router(
    staff_router,
    prefix="/staff",
    tags=["staff"],
    dependencies=[],#check staff privileges?
    responses={HTTP_404_NOT_FOUND: {"description": "Staff content not found"}},
)
app.include_router(
    client_router,
    prefix="/client",
    tags=["client"],
    dependencies=[],#check client privileges?
    responses={HTTP_404_NOT_FOUND: {"description": "Client content not found"}},
)
#default pages
@app.get("/")
async def root():
    return {"hello": "world"}


