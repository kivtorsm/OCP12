from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DB_ENGINE_ACCESS = "mysql://app:password@localhost/epic_events"
ENGINE = create_engine(DB_ENGINE_ACCESS)

Session = sessionmaker(bind=ENGINE)
SESSION = Session()

Base = declarative_base()
