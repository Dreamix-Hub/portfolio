from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from .. import models
from ..schemas import (
    Token,
    AdminResponse,
    AdminCreate
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


@router.post("/register", response_model=AdminResponse, status_code=status.HTTP_201_CREATED)
async def create_admin(admin_details: AdminCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(models.Admin).where(models.Admin.username == admin_details.username)
    )
    admin_exist = result.scalars().first()

    if admin_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin already exist"
        )
    
    new_admin = models.Admin(
        username=admin_details.username,
        password_hash=hash_password(admin_details.password)
    )
    
    db.add(new_admin)
    await db.commit()
    await db.refresh(new_admin)
    return new_admin


