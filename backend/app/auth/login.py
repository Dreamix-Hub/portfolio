from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from .. import models
from ..schemas import (
    Token
)

from .utils import hash_password, verify_password
from .jwt import create_access_token
from ..config import settings

router = APIRouter()

@router.post("", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(models.Admin).where(
            func.lower(models.Admin.username) == form_data.username.lower()
        )
    )
    username_exist = result.scalars().first()
    
    if not username_exist or not verify_password(form_data.password, username_exist.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
        
    expires = timedelta(minutes=settings.access_token_expires_min)
    access_token = create_access_token(
        data={"sub": str(form_data.username)},
        expire_delta=expires
    )
    
    return Token(access_token=access_token, token_type="bearer")
