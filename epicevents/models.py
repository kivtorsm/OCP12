import datetime

from typing import List

from sqlalchemy import Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func

from conf import Base, ENGINE


class Event(Base):
    __tablename__ = "event"

    # Data columns
    id: Mapped[int] = mapped_column(primary_key=True)
    contract_id: Mapped[int] = mapped_column(ForeignKey('contract.id'))
    contract: Mapped["Contract"] = relationship(back_populates='events')
    client_id: Mapped[int] = mapped_column(ForeignKey('client.id'))
    client: Mapped["Client"] = relationship(back_populates='events')
    start_date: Mapped[str] = mapped_column(String(10))
    end_date: Mapped[str] = mapped_column(String(10))
    support_contact_id: Mapped[int] = mapped_column(ForeignKey('employee.id'))
    support_contact: Mapped["Employee"] = relationship(back_populates='events')
    location: Mapped[str] = mapped_column(String(100))
    attendees_number: Mapped[str] = mapped_column(Integer)
    notes: Mapped[str] = mapped_column(String(2048))

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
    client: Mapped["Client"] = relationship(back_populates='contracts')
    total_amount: Mapped[float] = mapped_column(Float)
    due_amount: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String(20))
    events: Mapped[List["Event"]] = relationship(
        back_populates="contract",
    )

    # Audit columns
    created: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    def __repr__(self):
        return f"Contract {self.id}, client {self.client.company_name}, total_amount {self.total_amount}, " \
               f"due_amount {self.due_amount}"


class Client(Base):
    __tablename__ = "client"

    # Data columns
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(100))
    telephone: Mapped[str] = mapped_column(String(15))
    company_name: Mapped[str] = mapped_column(String(50))
    commercial_id: Mapped[int] = mapped_column(ForeignKey('employee.id'))
    commercial: Mapped["Employee"] = relationship(back_populates='clients')
    contracts: Mapped[List["Contract"]] = relationship(
        back_populates="client",
    )
    events: Mapped[List["Event"]] = relationship(
        back_populates="client",
    )

    # Audit columns
    created: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    modified: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    def __repr__(self):
        return "<Client(id = '%s', first_name='%s', last_name='%s', company_name='%s')>" % (
            self.id,
            self.first_name,
            self.last_name,
            self.company_name,
        )


class Employee(Base):
    __tablename__ = "employee"

    # Data columns
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(20))
    last_name: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(100))
    department_id: Mapped[int] = mapped_column(ForeignKey('department.id'))
    department: Mapped["Department"] = relationship(back_populates='employees')
    encoded_hash: Mapped[str] = mapped_column(String(100))
    clients: Mapped[List["Client"]] = relationship(
        back_populates="commercial",
    )
    events: Mapped[List["Event"]] = relationship(
        back_populates="support_contact",
    )

    def __repr__(self):
        return f"Employé {self.id}, Prénom: {self.first_name}, nom: {self.last_name}, " \
               f"email: {self.email}, département: {self.department.name}"


class DepartmentPermission(Base):
    __tablename__ = "department_permission"

    # Data columns
    id: Mapped[int] = mapped_column(primary_key=True)
    department_id: Mapped[int] = mapped_column(ForeignKey('department.id'))
    department: Mapped["Department"] = relationship(back_populates='department_permissions')
    permission_id: Mapped[int] = mapped_column(ForeignKey('permission.id'))
    permission: Mapped["Permission"] = relationship(back_populates='department_permissions')

    def __repr__(self):
        return f"(Department permission {self.id}, department {self.department.name}, " \
               f"crud action {self.permission.crud_action}," \
               f"object type {self.permission.object_type}," \
               f"object list {self.permission.object_list}," \
               f"object field {self.permission.object_field})"


class Department(Base):
    __tablename__ = "department"

    # Data columns
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    employees: Mapped[List["Employee"]] = relationship(
        back_populates="department",
    )
    department_permissions: Mapped[List["DepartmentPermission"]] = relationship(
        back_populates="department",
    )

    def __repr__(self):
        return f"Department {self.id}, name {self.name}"


class Permission(Base):
    __tablename__ = "permission"

    # Data columns
    id: Mapped[int] = mapped_column(primary_key=True)
    object_type: Mapped[str] = mapped_column(String(100))
    crud_action: Mapped[str] = mapped_column(String(20))
    object_type: Mapped[str] = mapped_column(String(30))
    object_list: Mapped[str] = mapped_column(String(20))
    object_field: Mapped[str] = mapped_column(String(300))
    department_permissions: Mapped[List["DepartmentPermission"]] = relationship(
        back_populates="permission",
    )

    def __repr__(self):
        return f"Permission {self.id}, crud action {self.crud_action}, " \
               f"object type {self.object_type}, " \
               f"object list {self.object_list}, " \
               f"object field {self.object_field}"


def start_db():
    Base.metadata.create_all(ENGINE)
