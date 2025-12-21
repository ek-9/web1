from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# mysql+aiomysql://USER:PASSWORD@HOST:PORT/DBNAME
MYSQL_URL = os.getenv(
    "MYSQL_URL",
    "mysql+aiomysql://root:0000@localhost:3306/webp"
)

engine = create_async_engine(
    MYSQL_URL,
    echo=True,
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()

# FastAPI 의존성
async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()