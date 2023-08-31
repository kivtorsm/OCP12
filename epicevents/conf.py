import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from mysql import connector

# SQLAlchemy session construction
# DB_CONNEXION_STRING
absolute_path = os.path.dirname(__file__)
relative_path = '../.ssh/db_connexion.txt'
full_path = os.path.join(absolute_path, relative_path)

with open(full_path) as f:
    DB_ENGINE_ACCESS = f.readlines()[0]

ENGINE = create_engine(DB_ENGINE_ACCESS)

Session = sessionmaker(bind=ENGINE)
session = Session()

Base = declarative_base()

# Test data location
absolute_path = os.path.dirname(__file__)
relative_path = '../tests/test_data.sql'
CREATE_TEST_DATA_PATH = os.path.join(absolute_path, relative_path)

# Secret location
absolute_path = os.path.dirname(__file__)
relative_path = '../.ssh/secret.txt'
full_path = os.path.join(absolute_path, relative_path)

with open(full_path) as f:
    SECRET = str(f.readlines())

# netrc location
HOST = "http://localhost:8000"

