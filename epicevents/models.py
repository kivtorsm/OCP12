from database import db

from sqlalchemy import Column, Integer, String, Float, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


Base = declarative_base()


class Event:
    __tablename__ = "event"

    # Data columns
    id = Column(Integer, primary_key=True)
    contract_id = Column(Integer, ForeignKey('contract.id'))
    contract = relationship('Contract')
    client_id = Column(Integer, ForeignKey('client.id'))
    client = relationship('Client')
    start_date = Column(db.DATETIME)
    end_date = Column(db.DATETIME)
    support_contact_id = Column(Integer, ForeignKey('employee.id'))
    support_contact = relationship('Employee')
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


class Contract(Base):
    __tablename__ = "contract"

    # Data columns
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('client.id'))
    client = relationship('Client')
    total_amount = Column(Float)
    due_amount = Column(Float)
    status = Column(String(20))
    events = relationship(Event, backref="events")

    # Audit columns
    created = Column(db.DATETIME)

    def __repr__(self):
        return f"Contract {self.id}, client {self.client.company_name}, total_amount {self.total_amount}, " \
               f"due_amount {self.due_amount}"


class Client(Base):
    __tablename__ = "client"

    # Data columns
    id = Column(Integer, primary_key=True)
    first_name = Column(String(30))
    last_name = Column(String(30))
    email = Column(String(100))
    telephone = Column(String(15))
    company_name = Column(String(50))
    commercial_id = Column(Integer, ForeignKey('employee.id'))
    contracts = relationship(Contract, backref='contracts')
    events = relationship(Event, backref='clients')

    # Audit columns
    created = Column(db.DATETIME)
    modified = Column(db.DATETIME)

    def __repr__(self):
        return "<Client(first_name='%s', last_name='%s', company_name='%s')>" % (
            self.first_name,
            self.last_name,
            self.company_name,
        )


class Employee:
    __tablename__ = "employee"

    # Data columns
    id = Column(Integer, primary_key=True)
    first_name = Column(String(20))
    last_name = Column(String(20))
    email = Column(String(100))
    department_id = Column(Integer, ForeignKey='department.id')
    department = relationship('Department')
    encoded_hash = Column(String(64))
    commercial_for = relationship(Client, backref='clients')
    support_contact_for = relationship(Event, backref='events')

    def __repr__(self):
        return f"Employee {self.id}, first name {self.first_name}, last name {self.last_name}, " \
               f"email {self.email}, department id {self.department_id}"


class DepartmentPermission:
    __tablename__ = "department_permission"

    # Data columns
    id = Column(Integer, primary_key=True)
    department_id = Column(Integer, ForeignKey='department.id')
    department = relationship('Department')
    permission_id = Column(Integer, ForeignKey='permission.id')
    permission = relationship('Permission')

    def __repr__(self):
        return f"Department permission {self.id}, department {self.deparment.name}, " \
               f"permission {self.permission.name}"


class Department:
    __tablename__ = "department"

    # Data columns
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    employees = relationship(Employee, backref='employees')
    department_permission = relationship(DepartmentPermission, backref='departmentpermissions')

    def __repr__(self):
        return f"Department {self.id}, name {self.name}"


class Permission:
    __tablename__ = "permission"

    # Data columns
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    department_permission = relationship(DepartmentPermission, backref='departmentpermissions')

    def __repr__(self):
        return f"Permission {self.id}, name {self.name}"


def start():
    engine = create_engine("mysql://app:password@localhost/epic_events")

    Session = sessionmaker(bind=engine)
    session = Session()

    Base.metadata.create_all(engine)
    return engine, session
