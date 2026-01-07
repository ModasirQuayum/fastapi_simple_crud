from typing import List
from fastapi import APIRouter, Depends,status
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.books.models import Book
from src.books.service import BookService
from src.db.main import get_session
from .schemas import BookCreateModel, BookUpdateSchema
book_router = APIRouter()

@book_router.get('/',response_model=List[Book])
async def get_all_book(session:AsyncSession=Depends(get_session)):
    books = await BookService().get_all_books(session)
    return books

@book_router.get('/{book_uid}')
async def get_book(book_uid:str,session:AsyncSession=Depends(get_session)):
    book = await BookService().get_book(book_uid,session)
    return book

@book_router.post('/create',status_code=status.HTTP_201_CREATED)
async def create_book(book_data:BookCreateModel,session:AsyncSession=Depends(get_session))->dict:
    new_book = await BookService().create_book(book_data,session)
    return new_book

@book_router.patch('/{book_uid}')
async def update_book(book_uid:str,book_update_data:BookUpdateSchema,session:AsyncSession=Depends(get_session))->dict:
    updated_book = await BookService().update_book(book_uid,book_update_data,session)
    
    return updated_book

@book_router.get('/delete/{book_uid}')
async def delete_book(book_uid:str,session:AsyncSession=Depends(get_session))->dict:
    response = await BookService().delete_book(book_uid,session)
    return response
