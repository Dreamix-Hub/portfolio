from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from .. import models
from ..schemas import (
    ProjectResponse
)

router = APIRouter()


# /api/projects?category_id=1
@router.get("", response_model=list[ProjectResponse])
async def get_projects(db: Annotated[AsyncSession, Depends(get_db)], category_id: int | None = None):
    
    # if category_id provided return all projects having that specific category id
    if category_id:
        # check category exist in ProjectCategory table
        result = await db.execute(
            select(models.ProjectCategory).where(models.ProjectCategory.id == category_id)
        )
        category_exist = result.scalars().first()
        if not category_exist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"invalid category {category_id}, not found in table"
            )
        
        projects = await db.execute(
            select(models.Project).filter(models.Project.category_id == category_id).options(
                selectinload(models.Project.category),
                selectinload(models.Project.techstack)
            )
        ) 
        all_projects = projects.scalars().all()
        
        if not all_projects:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="no project exist with this category"
            )
        
        return all_projects
    
    
    # eagerly loading all the relationships and the project data
    result = await db.execute(
        select(models.Project).options(
            selectinload(models.Project.category),
            selectinload(models.Project.techstack)
        )
    )
    all_projects = result.scalars().all()
    
    return all_projects


@router.get("/{id}", response_model=ProjectResponse)
async def get_single_project(id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(models.Project).where(models.Project.id == id).options(
            selectinload(models.Project.category),
            selectinload(models.Project.techstack)
        )
    )
    project_exist = result.scalars().first()
    
    if not project_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="project not found in the db"
        )
    
    return project_exist