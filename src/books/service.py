from datetime import datetime
from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from .models import Book
from sqlmodel import select,desc
from .schemas import BookCreateModel, BookUpdateSchema
class BookService:
    async def get_all_books(self,session:AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.execute(statement)
        return result.scalars().all()
    
    async def get_book(self,book_uid:str,session:AsyncSession):
        statement = select(Book).where(Book.uid == book_uid)
        result = await session.execute(statement)
        
        book = result.scalar_one_or_none()
        
        if not book:
            return HTTPException(status_code=404,detail="Book not Found")
        return book.model_dump()
    
    async def create_book(self,book_data:BookCreateModel,session:AsyncSession):
        data = book_data.model_dump()
        new_book = Book(
            **data
        )
        new_book.published_date = datetime.strptime(data['published_date'],"%Y-%m-%d")
        session.add(new_book)
        await session.commit()
        await session.refresh(new_book)
        
        return new_book
    
    async def update_book(self,book_uid:str,updated_book:BookUpdateSchema,session:AsyncSession):
        statement = select(Book).where(Book.uid == book_uid)
        result = await session.execute(statement)
        updated_data = result.scalar_one_or_none()
        data = updated_book.model_dump()
        
        for k,v in data.items():
            setattr(updated_data,k,v)
        await session.commit()
        await session.refresh(updated_data)
        
        return updated_data.model_dump()
    
    async def delete_book(self,book_uid:str,session:AsyncSession):
        statement = select(Book).where(Book.uid == book_uid)
        result = await session.execute(statement)
        deleted_data = result.scalar_one_or_none()
        if deleted_data is not None:
            await session.delete(deleted_data)
            await session.commit()
            return {"message": "Book Record deleted"}
        else:
            return {"message": "error occured"}           