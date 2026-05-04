from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from .. import models
from ..schemas import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate
)

router = APIRouter()

@router.post("", response_model=ProjectResponse)
async def add_project(project_details: ProjectCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    # check if category exist
    category_check = await db.execute(
        select(models.ProjectCategory).where(models.ProjectCategory.id == project_details.category_id)
    )
    category_exist = category_check.scalars().first()
    
    if not category_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="category not found in project_categories table"
        )
    
    # check if tech stack ids exist 
    for id in project_details.techstack_ids:
        techstack_check = await db.execute(
            select(models.TechStack).where(models.TechStack.id == id)
        )
        techstack_exist = techstack_check.scalars().first()
        
        if not techstack_exist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
               detail=f"tech stack with id {id} not found in techstack table"
            )
    
    # creating a project
    new_project = models.Project(
        title=project_details.title.lower(),
        description=project_details.description.lower(),
        live_link=project_details.live_link,
        github_link=project_details.github_link,
        featured=project_details.featured,
        category_id=project_details.category_id
    )
    # first fetch the actual object from the tech_stacks table using passed ids
    result = await db.execute(
        select(models.TechStack).filter(models.TechStack.id.in_(project_details.techstack_ids))
    )
    tech_items = list(result.scalars().all())
    
    # assign directly to the relationship, sqlalchemy will insert it in the project_techstack table and handle all association things
    new_project.techstack = tech_items
    
    db.add(new_project)
    await db.commit()
    # eagerly loading relationships
    await db.refresh(new_project, ["category", "techstack"])
    return new_project
