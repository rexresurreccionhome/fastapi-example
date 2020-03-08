from typing import List, Optional

from fastapi import Form, Header
from fastapi.exceptions import HTTPException
from fastapi.openapi.models import OAuth2 as OAuth2Model, OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param

from pydantic import BaseModel

from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from starlette.requests import Request



class Token(BaseModel):
    access_token: str
    token_type: str


class AuthUser(BaseModel):
    name: str
    email: str
    username: str
    disabled: bool


class AuthClient(BaseModel):
    app: str
    email: str
    client_id: str
    disabled: bool


#There is an issue with swagger unable to submit client_id and client_secret in the Body or Header requests
#But this has has been tested to work using a direct curl outside of docs
# E.g. curl -X POST "http://localhost:5000/token/clientcreds" -H "accept: application/json" \
#           -H "Content-Type: application/x-www-form-urlencoded" \
#           -d "grant_type=&client_id=123xyz&client_secret=secret1234&scope="
class OAuth2ClientRequestForm:
    def __init__(
        self,
        grant_type: str = Form(None, regex="client_credentials"),
        client_id: str = Form(...),
        client_secret: str = Form(...),
        scope: str = Form(""),
    ):
        self.grant_type = grant_type
        self.scopes = scope.split()
        self.client_id = client_id
        self.client_secret = client_secret


#This is almost an exact copy of OAuth2ClientPasswordBearer. The only difference is the clientCredential parameter in OAuthFlowsModel
#In fast, the OAuth2PasswordRequestForm also has a client_id and client_secret fields as optional
#Client Credential is different from Password flow because it does not have to collect the user's password
class OAuth2ClientBearer(OAuth2):
        def __init__(
            self,
            tokenUrl: str,
            scheme_name: str = None,
            scopes: dict = None,
            auto_error: bool = True,
        ):
            if not scopes:
                scopes = {}
            flows = OAuthFlowsModel(clientCredentials={"tokenUrl": tokenUrl, "scopes": scopes})
            super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

        async def __call__(self, request: Request) -> Optional[str]:
            authorization: str = request.headers.get("Authorization")
            scheme, param = get_authorization_scheme_param(authorization)
            if not authorization or scheme.lower() != "bearer":
                if self.auto_error:
                    raise HTTPException(
                        status_code=HTTP_401_UNAUTHORIZED,
                        detail="Not authenticated",
                        headers={"WWW-Authenticate": "Bearer"},
                                                                                                                                                                                                                    )
                else:
                    return None
            return param

