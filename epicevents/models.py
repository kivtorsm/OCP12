from database import db

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import deferred, declarative_base
from sqlalchemy.dialects.mysql import LONGBLOB


Base = declarative_base()


class Client(Base):
    __tablename__ = "clients"

    # Data columns
    id = Column(Integer, primary_key=True)
    first_name = Column(String(30))
    last_name = Column(String(30))
    email = Column(String(100))
    telephone = Column(String(15))
    company_name = Column(String(50))
    commercial_id = Column(Integer)

    # Audit columns
    created = Column(db.DATETIME)
    modified = Column(db.DATETIME)

    def __repr__(self):
        return "<Client(first_name='%s', last_name='%s', company_name='%s')>" % (
            self.first_name,
            self.last_name,
            self.company_name,
        )


class Contract(Base):
    __tablename__ = "contracts"

    # Data columns
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer)
    total_amount = Column(Float)
    due_amount = Column(Float)
    status = Column(String(20))

    # Audit columns
    created = Column(db.DATETIME)


class Event:
    __tablename__ = "events"

    # Data columns
    id = Column(Integer, primary_key=True)
    contract_id = Column(Integer)
    client_id = Column(Integer)
    start_date = Column(db.DATETIME)
    end_date = Column(db.DATETIME)
    support_contact_id = Column(Integer)
    location = Column(String(100))
    attendees_number = Column(Integer)
    notes = Column(String(2048))


class Employee:
    __tablename__ = "employees"

    # Data columns
    id = Column(Integer, primary_key=True)
    first_name = Column(String(20))
    last_name = Column(String(20))
    email = Column(String(100))
    department_id = Column(Integer)
    encoded_hash = Column(String(64))


class Department:
    __tablename__ = "departments"

    # Data columns
    id = Column(Integer, primary_key=True)
    name = Column(String(100))


class Permission:
    __tablename__ = "permissions"

    # Data columns
    id = Column(Integer, primary_key=True)
    name = Column(String(100))


class DepartmentPermission:
    __tablename__ = "department_permissions"

    # Data columns
    id = Column(Integer, primary_key=True)
    department_id = Column(Integer)
    permission_id = Column(Integer)
