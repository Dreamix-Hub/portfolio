from .config import settings

import jwt
from pwdlib import PasswordHash

from datetime import datetime, UTC, timedelta
from .config import settings

password_hash = PasswordHash.recommended()

def hash_password(plain_password: str) -> str:
    return password_hash.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

def create_access_token(data: dict, expire_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    
    if expire_delta:
        expire = datetime.now(UTC) + timedelta()
    else:
        expire = datetime.now(UTC) + timedelta(minutes=settings.access_token_expires_min)
        
    to_encode.update({'exp': expire})
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key.get_secret_value(),
        algorithm=settings.algorithm
    )
    return encoded_jwt

