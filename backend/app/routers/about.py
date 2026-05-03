from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from .. import models
from ..schemas import (
    AboutResponse,
    AboutUpdate
)

router = APIRouter()

@router.get("", response_model=AboutResponse)
async def get_about(db: Annotated[AsyncSession, Depends(get_db)]):
    about = await db.execute(
        select(models.About)
    )
    about_exist = about.scalars().first()
    
    if not about_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Noting in about"
        )
    return about_exist
    
@router.patch("", response_model=AboutResponse)
async def update_about(about_update: AboutUpdate, db: Annotated[AsyncSession, Depends(get_db)]):
    about = await db.execute(
        select(models.About)
    )
    about_exist = about.scalars().first()
    
    if not about_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Noting in about"
        )
    
    # Only update fields that were actually provided in the request
    update_data = about_update.model_dump(exclude_unset=True)
    
    for field_name, value in update_data.items():
        # Lowercase string fields where appropriate
        if field_name in ["full_name", "headline", "description", "email_public", "github_link", "linkedin_link"] and value:
            value = value.lower() if isinstance(value, str) else value
        
        setattr(about_exist, field_name, value)
        
    await db.commit()
    await db.refresh(about_exist)
    return about_exist
    