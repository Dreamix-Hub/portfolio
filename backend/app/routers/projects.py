from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from .. import models
from ..schemas import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate
)

router = APIRouter()

@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
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

@router.patch("/{id}", response_model=ProjectResponse)
async def update_project(id: int, updated_data: ProjectUpdate, db: Annotated[AsyncSession, Depends(get_db)]):
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
            detail="project don't exist"
        )
    
    details = updated_data.model_dump(exclude_unset=True)
    
    # handle techstack_ids separately since it's a many-to-many relationship
    techstack_ids = details.pop("techstack_ids", None)
    
    for field_name, value in details.items():
        if field_name in ["title", "description"] and value:
            value = value.lower() if isinstance(value, str) else value
        
        setattr(project_exist, field_name, value)
    
    # update techstacks if provided
    if techstack_ids is not None:
        # clear existing techstacks
        project_exist.techstack.clear()
        # fetch and add new techstacks
        techstacks = await db.execute(
            select(models.TechStack).filter(models.TechStack.id.in_(techstack_ids))
        )
        for tech in techstacks.scalars().all():
            project_exist.techstack.append(tech)
        
    await db.commit()
    
    # clear session cache entirely
    db.expunge_all()
    
    # fetch fresh project with eagerly loaded relationships
    result = await db.execute(
        select(models.Project).where(models.Project.id == id).options(
            selectinload(models.Project.category),
            selectinload(models.Project.techstack)
        )
    )
    updated_project = result.scalars().first()
    return updated_project
    