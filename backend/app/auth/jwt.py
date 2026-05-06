import jwt

from datetime import datetime, UTC, timedelta
from ..config import settings


def create_access_token(data: dict, expire_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    
    if expire_delta:
        expire = datetime.now(UTC) + expire_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=settings.access_token_expires_min)
        
    to_encode.update({'exp': expire})
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key.get_secret_value(),
        algorithm=settings.algorithm
    )
    return encoded_jwt

def verify_access_token(token: str) -> str | None:
    
    try:
        payload = jwt.decode(
            token,
            settings.secret_key.get_secret_value(),
            algorithms=[settings.algorithm],
            options={"require": ["exp", "sub"]}
        )
    except jwt.InvalidTokenError:
        return None
    else:
        return payload.get("sub")