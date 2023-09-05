import os
import sentry_sdk

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

# Sentry
# functions_to_trace = [
#     {"qualified_name": "dao.EmployeeDAO.add"},
#     {"qualified_name": "dao.EmployeeDAO.update"},
#     {"qualified_name": "dao.ContractDAO.update"},
# ]

sentry_sdk.init(
    dsn="https://80080c29e56253234651359eb9f778db@o4505799371128832.ingest.sentry.io/4505821850828800",
    # functions_to_trace=functions_to_trace,
    # max_breadcrumbs=100,
    # debug=True,

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,

    # profiles_sampler=profiles_sampler,
)
