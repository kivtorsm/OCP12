from database import db

from typing import List

from sqlalchemy import Column, Integer, String, Float, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Mapped, mapped_column


Base = declarative_base()


class Event:
    __tablename__ = "event"

    # Data columns
    id: Mapped[int] = mapped_column(primary_key=True)
    contract_id: Mapped[int] = mapped_column(ForeignKey('contract.id'))
    contract: Mapped["Contract"] = relationship(back_populates='contracts')
    client_id: Mapped[int] = mapped_column(ForeignKey('client.id'))
    client: Mapped["Client"] = relationship(back_populates='clients')
    start_date = Column(db.DATETIME)
    end_date = Column(db.DATETIME)
    support_contact_id: Mapped[int] = mapped_column(ForeignKey('employee.id'))
    support_contact: Mapped["Employee"] = relationship(back_populates='support_contacts')
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
    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey('client.id'))
    client: Mapped["Client"] = relationship(back_populates='clients')
    total_amount = Column(Float)
    due_amount = Column(Float)
    status = Column(String(20))
    events: Mapped[List["Event"]] = relationship(
        back_populates="contract",
    )

    # Audit columns
    created = Column(db.DATETIME)

    def __repr__(self):
        return f"Contract {self.id}, client {self.client.company_name}, total_amount {self.total_amount}, " \
               f"due_amount {self.due_amount}"


class Client(Base):
    __tablename__ = "client"

    # Data columns
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name = Column(String(30))
    last_name = Column(String(30))
    email = Column(String(100))
    telephone = Column(String(15))
    company_name = Column(String(50))
    commercial_id: Mapped[int] = mapped_column(ForeignKey('employee.id'))
    commercial: Mapped["Employee"] = relationship(back_populates='commercials')
    contracts: Mapped[List["Contract"]] = relationship(
        back_populates="client",
    )
    events: Mapped[List["Event"]] = relationship(
        back_populates="client",
    )

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
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name = Column(String(20))
    last_name = Column(String(20))
    email = Column(String(100))
    department_id: Mapped[int] = mapped_column(ForeignKey='department.id')
    department: Mapped["Department"] = relationship(back_populates='departments')
    encoded_hash = Column(String(64))
    clients: Mapped[List["Client"]] = relationship(
        back_populates="employee",
    )
    events: Mapped[List["Event"]] = relationship(
        back_populates="employee",
    )

    def __repr__(self):
        return f"Employee {self.id}, first name {self.first_name}, last name {self.last_name}, " \
               f"email {self.email}, department id {self.department_id}"


class DepartmentPermission:
    __tablename__ = "department_permission"

    # Data columns
    id: Mapped[int] = mapped_column(primary_key=True)
    department_id: Mapped[int] = mapped_column(ForeignKey='department.id')
    department: Mapped["Department"] = relationship(back_populates='departments')
    permission_id: Mapped[int] = mapped_column(ForeignKey='permission.id')
    permission: Mapped["Permission"] = relationship(back_populates='permissions')
    def __repr__(self):
        return f"Department permission {self.id}, department {self.deparment.name}, " \
               f"permission {self.permission.name}"


class Department:
    __tablename__ = "department"

    # Data columns
    id: Mapped[int] = mapped_column(primary_key=True)
    name = Column(String(100))
    employees: Mapped[List["Employee"]] = relationship(
        back_populates="department",
    )
    department_permissions: Mapped[List["DepartmentPermission"]] = relationship(
        back_populates="department",
    )

    def __repr__(self):
        return f"Department {self.id}, name {self.name}"


class Permission:
    __tablename__ = "permission"

    # Data columns
    id: Mapped[int] = mapped_column(primary_key=True)
    name = Column(String(100))
    department_permissions: Mapped[List["DepartmentPermission"]] = relationship(
        back_populates="permission",
    )

    def __repr__(self):
        return f"Permission {self.id}, name {self.name}"


def start():
    engine = create_engine("mysql://app:password@localhost/epic_events")

    Session = sessionmaker(bind=engine)
    session = Session()

    Base.metadata.create_all(engine)
    return engine, session
