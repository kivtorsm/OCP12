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

    def __repr__(self):
        return f"Contract {self.id}, client {self.client_id}, total_amount {self.total_amount}, " \
               f"due_amount {self.due_amount}"


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

    def __repr__(self):
        return f"Event {self.id}, " \
               f"client {self.client_id}, " \
               f"contract {self.contract_id}, " \
               f"start date {self.start_date}, " \
               f"end date {self.end_date}, " \
               f"location {self.location}, " \
               f"attendees {self.attendees_number}"


class Employee:
    __tablename__ = "employees"

    # Data columns
    id = Column(Integer, primary_key=True)
    first_name = Column(String(20))
    last_name = Column(String(20))
    email = Column(String(100))
    department_id = Column(Integer)
    encoded_hash = Column(String(64))

    def __repr__(self):
        return f"Employee {self.id}, first name {self.first_name}, last name {self.last_name}, " \
               f"email {self.email}, department id {self.department_id}"


class Department:
    __tablename__ = "departments"

    # Data columns
    id = Column(Integer, primary_key=True)
    name = Column(String(100))

    def __repr__(self):
        return f"Department {self.id}, name {self.name}"


class Permission:
    __tablename__ = "permissions"

    # Data columns
    id = Column(Integer, primary_key=True)
    name = Column(String(100))

    def __repr__(self):
        return f"Permission {self.id}, name {self.name}"


class DepartmentPermission:
    __tablename__ = "department_permissions"

    # Data columns
    id = Column(Integer, primary_key=True)
    department_id = Column(Integer)
    permission_id = Column(Integer)

    def __repr__(self):
        return f"Department permission {self.id}, department id {self.department_id}, " \
               f"permission id {self.permission_id}"
