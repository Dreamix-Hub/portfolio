from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, asc
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..schemas import ContactCreate, ContactUpdate, ContactResponse
from .. import models

router = APIRouter()


@router.post("", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def send_message(form_data: ContactCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    
    new_message = models.Contact(
        name=form_data.name.lower(),
        email=form_data.email.lower(),
        subject=form_data.subject.lower(),
        message=form_data.message.lower()
    ) 
    
    db.add(new_message)
    await db.commit()
    await db.refresh(new_message)
    return new_message

@router.get("", response_model=list[ContactResponse])
async def get_messages(db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(models.Contact).order_by(asc(models.Contact.is_read))
    )
    
    messages = result.scalars().all()
    
    if not messages:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no message found in inbox"
        )
    
    return messages

@router.get("/{id}", response_model=list[ContactResponse])
async def get_message(id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(models.Contact).where(models.Contact.id == id)
    )
    
    messages = result.scalars().all()
    
    if not messages:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no message found in inbox"
        )
    
    return messages

@router.patch("/{id}", response_model=ContactResponse)
async def mark_as_read(id: int, message: ContactUpdate, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(models.Contact).where(models.Contact.id == id)
    )
    msg = result.scalars().first()
    
    if not msg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="message not found"
        )
        
    if msg.is_read == False:
        msg.is_read = message.is_read
        
    await db.commit()
    await db.refresh(msg)
    return msg

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(models.Contact).where(models.Contact.id == id)
    )
    message = result.scalars().first()
    
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no message exist"
        )
    
    await db.delete(message)
    await db.commit()
    