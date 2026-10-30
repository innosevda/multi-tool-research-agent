from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

import os
from dotenv import load_dotenv

load_dotenv()

# connecting to postgreSQL database
local_database_url = os.getenv("DATABASE_URL")
if not local_database_url:
    raise RuntimeError("DATABASE_URL must be set in the environment or .env file")

engine = create_engine(local_database_url)

# when FastAPI recieves a request, we'll create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()