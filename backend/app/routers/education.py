from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from .. import models
from ..schemas import (
    EducationCreate, 
    EducationUpdate, 
    EducationResponse
)


router = APIRouter()

@router.post("", response_model=EducationResponse, status_code=status.HTTP_201_CREATED)
async def add_qualification(education: EducationCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(models.Education).where(func.lower(models.Education.title) == education.title.lower())
    )
    existing_education = result.scalars().first()
    
    if existing_education is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="education already exist with same title"
        )
    
    new_education = models.Education(
        title=education.title.lower(),
        institute=education.institute.lower(),
        start_date=education.start_date,
        end_date=education.end_date
    )
    db.add(new_education)
    await db.commit()
    await db.refresh(new_education)
    return new_education

@router.get("", response_model=list[EducationResponse])
async def get_qualifications(db: Annotated[AsyncSession, Depends(get_db)]):        
    result = await db.execute(
        select(models.Education).order_by(desc(models.Education.start_date))
    )
    qualifications = result.scalars().all()
    
    if not qualifications:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no qualifications exist"
        )
    
    return qualifications

@router.patch("/{id}",response_model=EducationResponse)
async def update_qualification(id: int, education: EducationUpdate, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(models.Education).where(models.Education.id == id)
    )
    degree_exist = result.scalars().first()
    
    if not degree_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="qualification not exist"
        )
        
    update_education = education.model_dump(exclude_unset=True)
    
    for field_name, value in update_education.items():
        if field_name in ["title", "institute", "start_date", "end_date"] and value:
            value = value.lower() if isinstance(value, str) else value
        
        setattr(degree_exist, field_name, value)
    
    await db.commit()
    await db.refresh(degree_exist)
    
    return degree_exist