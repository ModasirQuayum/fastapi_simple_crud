from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.config import Config
from sqlmodel import SQLModel
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(
    url=Config.DATABASE_URL,
    echo=True
)

async def init_db():
    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)
        

async def get_session()->AsyncSession:
    Session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    async with Session() as session:
        yield session