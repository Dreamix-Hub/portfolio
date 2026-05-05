from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from .. import models
from ..schemas import (
    BlogCreate, 
    BlogResponse, 
    BlogUpdate
)

router = APIRouter()

@router.post("", response_model=BlogResponse)
async def create_blog(blog_data: BlogCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    # check if category exist 
    result = await db.execute(
        select(models.BlogCategory).where(models.BlogCategory.id == blog_data.category_id)
    )
    category_exist = result.scalars().first()
    
    if not category_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"no category exist with id {blog_data.category_id}"
        )
        
    new_blog = models.Blog(
        title=blog_data.title,
        content=blog_data.content,
        category_id=blog_data.category_id,
        is_draft=blog_data.is_draft
    )
    
    
    db.add(new_blog)
    await db.commit()
    await db.refresh(new_blog, ["category"])
    
    return new_blog

# this api route serve Admin return all the blogs drafted + published
@router.get("", response_model=list[BlogResponse])
async def get_all_blogs(db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(models.Blog).options(
            selectinload(models.Blog.category)
        )
    )
    blog_exist = result.scalars().all()
    
    if not blog_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no blog in the database"
        )
    
    return blog_exist

@router.patch("/{id}", response_model=BlogResponse)
async def update_blog(id: int, blog_data: BlogUpdate, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(models.Blog).where(models.Blog.id == id).options(
            selectinload(models.Blog.category)
        )
    )
    blog_exist = result.scalars().first()
    
    if not blog_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="blog not found in the db"
        )
    
    data = blog_data.model_dump(exclude_unset=True)
    
    for field_name, value in data.items():
        if field_name in ["title", "content", "category_id", "is_draft"] and value:
            value = value.lower() if isinstance(value, str) else value
        setattr(blog_exist, field_name, value)
    
    await db.commit()
    await db.refresh(blog_exist, ["category"])
    return blog_exist
    
