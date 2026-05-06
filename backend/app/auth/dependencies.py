from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models import Admin
from .jwt import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[AsyncSession, Depends(get_db)]) -> Admin:
    
    username_exist = verify_access_token(token)
    
    if username_exist is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid or expire token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    result = await db.execute(
        select(Admin).where(Admin.username == username_exist)
    )
    username = result.scalars().first()
    
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid or expire token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return username

CurrentUser = Annotated[Admin, Depends(get_current_user)]  # type alias