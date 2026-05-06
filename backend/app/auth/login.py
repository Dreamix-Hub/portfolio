from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from .. import models
from ..schemas import (
    AdminCreate,
    AdminLogin,
    AdminResponse
)

from utlis import hash_password

router = APIRouter()

@router.post("", response_model=AdminResponse)
async def create_admin(admin_details: AdminCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(models.Admin).where(models.Admin.username == admin_details.username)
    )
    admin_exist = result.scalars().first()
    
    if not admin_exist:
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