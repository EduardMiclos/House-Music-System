from models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'sqlite:///songs.db'

engine = create_engine(DATABASE_URL, echo=True)

# Now, creating all the tables in the database
Base.metadata.create_all(engine)

# Creating a session maker to manage database sessions
Session = sessionmaker(bind = engine)
session = Session()