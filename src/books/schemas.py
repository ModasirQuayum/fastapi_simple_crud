from pydantic import BaseModel
from datetime import datetime

class BookSchema(BaseModel):
    uid:str
    title:str
    author:str
    publisher:str
    published_date: datetime
    page_count:int
    language:str

class BookUpdateSchema(BaseModel):
    title:str
    author:str
    publisher:str
    page_count:int
    language:str


class BookCreateModel(BaseModel):
    title:str
    author:str
    publisher:str
    published_date: str
    page_count:int
    language:str