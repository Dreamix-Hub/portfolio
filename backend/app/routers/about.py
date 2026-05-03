from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
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
    
# @router.patch("", response_model=AboutResponse)
# async def update_about(about_update: AboutUpdate, db: Annotated[AsyncSession, Depends(get_db)]):
#     about = await db.execute(
#         select(models.About)
#     )
#     about_exist = about.scalars().first()
#     # if not about_exist:
#     #     raise HTTPException(
#     #         status_code=status.HTTP_404_NOT_FOUND,
#     #         detail="Noting in about"
#     #     )
    
#     if 
#     about_exist.full_name = AboutUpdate.full_name
    
    
    