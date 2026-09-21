from database import Base, engine
from models import User

# "Create the tables described by my models if they don't already exist."
# using Alchemy 
Base.metadata.create_all(engine)

print("Tables created!")