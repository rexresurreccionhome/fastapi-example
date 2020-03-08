from fastapi import FastAPI
from fastapi import Depends, Security, HTTPException
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

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.security.api_key import APIKeyHeader, APIKey
from authentication.schemas import (
    Token, 
    AuthUser, 
    AuthClient, 
    OAuth2ClientBearer,
    OAuth2ClientRequestForm,
)
from authentication.jwt import create_access_token, decode_access_token

import secrets
import base64

#inits
app = FastAPI()

#authentication

#apiKey: an application specific key that can come from a header (or query and cookie)
#Just showing that we can also pass it on headers.
#This is an alternative authentication for service to service api exchange
VALID_API_KEY = "am9obi5kb2U6cGFzczEyMzQ="
api_key_header = APIKeyHeader(name="staffing-gateway", auto_error=False)
async def get_key_header(api_key_header: str = Security(api_key_header)):
    correct_key_header = secrets.compare_digest(api_key_header, VALID_API_KEY)
    if correct_key_header:
        return api_key_header
    else:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Incorrect Key Header")

async def get_current_active_key(api_key: APIKey = Depends(get_key_header)):
    #TODO: implement real checking
    try:
        api_key_decoded = base64.b64decode(api_key_header)
    except Exception:
        api_key_decoded = ""

    return "scopes:read write"
 
#oauth2: all the OAuth2 ways to handle security (called "flows")
#password flow (Legacy)
#https://oauth.net/2/grant-types/password/
oauth2_password = OAuth2PasswordBearer(tokenUrl="/token/password")
@app.post("/token/password", response_model=Token)
async def tokenize_password(form_data: OAuth2PasswordRequestForm = Depends()):
    #TODO: Implement real user database search
    access_token = None
    correct_username = secrets.compare_digest(form_data.username, "john.doe")
    correct_password = secrets.compare_digest(form_data.password, "pass1234") #example only, hash this!
    if correct_username and correct_password:
        access_token = create_access_token(data={"sub": form_data.username})
    if not access_token:
        raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
    else:
        return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_password)):
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    #TODO: Implement real user database search
    user = AuthUser(** {
        "name": "John Doe",
        "username": "john.doe",
        "email": "john.doe@example.com",
        "disabled": False,
    })
    payload = decode_access_token(token)
    if payload.get("sub") != user.username:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: AuthUser = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user

#client credentials flow
#https://oauth.net/2/grant-types/client-credentials/
#https://www.oauth.com/oauth2-servers/access-tokens/client-credentials/
oauth2_client_creds = OAuth2ClientBearer(tokenUrl="/token/clientcreds")
@app.post("/token/clientcreds", response_model=Token)
async def tokenize_client_creds(form_data: OAuth2ClientRequestForm = Depends()):
    #TODO: Implement real client database search
    access_token = None
    correct_client_id = secrets.compare_digest(form_data.client_id, "123xyz")
    correct_secret = secrets.compare_digest(form_data.client_secret, "secret1234")
    if correct_client_id and correct_secret:
        access_token = create_access_token(data={"sub": form_data.client_id})
    if not access_token:
        raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Incorrect client ID or client secret",
                headers={"WWW-Authenticate": "Bearer"},
            )
    else:
        return {"access_token": access_token, "token_type": "bearer"}


async def get_current_client(token: str = Depends(oauth2_client_creds)):
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    #TODO: get client using the token
    client = AuthClient(** {
                "app": "Example App",
                "client_id": "123xyz",
                "email": "john.doe@example.com",
                "disabled": False,
            })
    payload = decode_access_token(token)
    if payload.get("sub") != client.client_id:
        raise credentials_exception
    return client

async def get_current_active_client(current_client: AuthClient = Depends(get_current_client)):
    if current_client.disabled:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Inactive Client")
    return current_client

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
@app.get("/auth/password", tags=["Auth Example"])
async def auth_password(current_user: AuthUser = Depends(get_current_active_user)):
    return {"greeting": f"Hello {current_user.name}!"}

@app.get("/auth/client_creds", tags=["Auth Example"])
async def auth_client_creds(current_client: AuthClient = Depends(get_current_active_client)):
    return {"app": f"Third-Party App {current_client.app}!"}

@app.get("/auth/key_header", tags=["Auth Example"])
async def auth_key_header(key_scope: str = Depends(get_current_active_key)):
    return key_scope


