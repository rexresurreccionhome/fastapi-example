from datetime import datetime, timedelta
from fastapi.exceptions import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED
from jwt import PyJWTError
import jwt
import os
import time


SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "5523c00f64df3d1c9002f1f5d6e5a5c254190d41cb9b606daec68028e8d9198f")
ALGORITHM = os.environ.get("JWT_ALGO", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("JWT_EXPIRES", 30)


#Copy paste from https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    credentials_exception = HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid Token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp: str = payload.get("exp")
        #print("Expires in {} secs".format(int(exp - time.time())))
        if exp is None or exp <= time.time():
            raise credentials_exception
        return payload
    except PyJWTError:
        raise credentials_exception

