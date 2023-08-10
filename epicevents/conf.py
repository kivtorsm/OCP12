from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DB_ENGINE_ACCESS = "mysql+mysqlconnector://app:password@localhost/epic_events"
# DB_ENGINE_ACCESS = "sqlite:///database.db"
ENGINE = create_engine(DB_ENGINE_ACCESS)

Session = sessionmaker(bind=ENGINE)
session = Session()

Base = declarative_base()
