from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase 

import os
from dotenv import load_dotenv

load_dotenv()

# connecting to postgreSQL database
local_database_url = os.getenv("DATABASE_URL")
engine = create_engine(local_database_url)

class Base(DeclarativeBase):
    pass
