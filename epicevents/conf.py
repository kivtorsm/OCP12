import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from mysql import connector

# SQLAlchemy session construction
DB_ENGINE_ACCESS = "mysql+mysqlconnector://app:password@localhost/epic_events"
# DB_ENGINE_ACCESS = "sqlite:///database.db"
ENGINE = create_engine(DB_ENGINE_ACCESS)

Session = sessionmaker(bind=ENGINE)
session = Session()

Base = declarative_base()

# Secret location
absolute_path = os.path.dirname(__file__)
relative_path = '../.ssh/secret.txt'
full_path = os.path.join(absolute_path, relative_path)

with open(full_path) as f:
    SECRET = str(f.readlines())

# netrc location
HOST = "http://localhost:8000"

