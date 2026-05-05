from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy import select
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

# /api/blogs?category_id=1
@router.get("", response_model=list[BlogResponse])
async def get_blogs(db: Annotated[AsyncSession, Depends(get_db)], category_id: int | None = None):
    
    # if query parameter comes in
    if category_id:
        result = await db.execute(
            select(models.BlogCategory).where(models.BlogCategory.id == category_id)
        )
        category_exist = result.scalars().first()
        if not category_exist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"no category exist with id {category_id}"
            )
        
        blog = await db.execute(
            select(models.Blog).where(models.Blog.category_id == category_id).options(
                selectinload(models.Blog.category)
            )
        )
        blog_exist = blog.scalars().all()
        
        return blog_exist
    
    result = await db.execute(
        select(models.Blog).options(
            selectinload(models.Blog.category)
        )
    )
    blog_exist = result.scalars().all()
    
    if not blog_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no blog exist, db is empty"
        )
    
    return blog_exist

