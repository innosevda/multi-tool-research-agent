from src.database import models
from src.database.database import Base, engine

Base.metadata.create_all(engine)

print("Database tables created.")