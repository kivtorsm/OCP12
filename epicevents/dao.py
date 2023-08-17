import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

from models import Client, Employee, Contract, Event, Department, Permission, DepartmentPermission

from conf import session


class ClientDAO:
    @staticmethod
    def get_all():
        return session.query(Client).all()

    @staticmethod
    def get_by_id(client_id: int) -> Client:
        return session.query(Client).get(client_id)

    @staticmethod
    def add(client: Client) -> None:
        session.add(client)
        session.commit()

    def update(
            self,
            client_id: int,
            commercial_id: int = None,
            company_name: str = None,
            email: str = None,
            first_name: str = None,
            last_name: str = None,
            telephone: str = None
    ):
        db_client = self.get_by_id(client_id)
        db_client.commercial_id = commercial_id if commercial_id else db_client.commercial_id
        db_client.company_name = company_name if company_name else db_client.company_name
        db_client.email = email if email else db_client.email
        db_client.last_name = last_name if last_name else db_client.last_name
        db_client.first_name = first_name if first_name else db_client.first_name
        db_client.telephone = telephone if telephone else db_client.telephone
        session.commit()

    def delete(self, client_id: int):
        client_db = self.get_by_id(client_id)
        session.delete(client_db)
        session.commit()


class ContractDAO:
    @staticmethod
    def get_all():
        return session.query(Contract).all()

    @staticmethod
    def get_by_id(contract_id: int) -> Contract:
        return session.query(Contract).get(contract_id)

    @staticmethod
    def add(contract: Contract) -> None:
        session.add(contract)
        session.commit()

    def update(
            self,
            contract_id,
            client_id: int = None,
            total_amount: float = None,
            due_amount: float = None,
            status: str = None,
    ):
        db_contract = self.get_by_id(contract_id)
        db_contract.client_id = client_id if client_id else db_contract.client_id
        db_contract.total_amount = total_amount if total_amount else db_contract.total_amount
        db_contract.due_amount = due_amount if due_amount else db_contract.due_amount
        db_contract.status = status if status else db_contract.status
        session.commit()

    def delete(self, contract_id):
        contract_db = self.get_by_id(contract_id)
        session.delete(contract_db)
        session.commit()


class EventDAO:
    @staticmethod
    def get_all():
        return session.query(Event).all()

    @staticmethod
    def get_by_id(event_id: str) -> Event:
        return session.query(Event).get(event_id)

    @staticmethod
    def add(event: Event) -> None:
        session.add(event)
        session.commit()

    def update(
            self,
            event_id,
            contract_id: int = None,
            client_id: int = None,
            start_date: str = None,
            end_date: str = None,
            support_contact_id: int = None,
            location: str = None,
            attendees_number: int = None,
            notes: str = None,
    ):
        db_event = self.get_by_id(event_id)
        db_event.contract_id = contract_id if contract_id else db_event.contract_id
        db_event.client_id = client_id if client_id else db_event.client_id
        db_event.start_date = start_date if start_date else db_event.start_date
        db_event.end_date = end_date if end_date else db_event.end_date
        db_event.support_contact_id = support_contact_id if support_contact_id else db_event.support_contact_id
        db_event.location = location if location else db_event.location
        db_event.attendees_number = attendees_number if attendees_number else db_event.attendees_number
        db_event.notes = notes if notes else db_event.notes
        session.commit()

    def delete(self, event_id: int):
        event_db = self.get_by_id(event_id)
        session.delete(event_db)
        session.commit()


class EmployeeDAO:
    @staticmethod
    def get_all():
        return session.query(Employee).all()

    @staticmethod
    def get_by_id(employee_id: str) -> Employee:
        return session.query(Employee).get(employee_id)

    @staticmethod
    def get_by_email(employee_email: str) -> Employee:
        return session.query(Employee).filter_by(email=employee_email)[0]

    @staticmethod
    def add(employee: Employee) -> None:
        session.add(employee)
        session.commit()

    def update(
            self,
            employee_id,
            first_name: str = None,
            last_name: str = None,
            email: str = None,
            department_id: int = None,
            encoded_hash: str = None,

    ):
        db_employee = self.get_by_id(employee_id)
        db_employee.first_name = first_name if first_name else db_employee.first_name
        db_employee.last_name = last_name if last_name else db_employee.last_name
        db_employee.email = email if email else db_employee.email
        db_employee.department_id = department_id if department_id else db_employee.department_id
        db_employee.encoded_hash = encoded_hash if encoded_hash else db_employee.encoded_hash

        session.commit()

    def delete(self, employee_id: int):
        employee_db = self.get_by_id(employee_id)
        session.delete(employee_db)
        session.commit()

#
# class DepartmentDAO:
#     @staticmethod
#     def get_all():
#         return Department.query.all()
#
#     @staticmethod
#     def get_by_id(department_id: str) -> Department:
#         return Department.query \
#             .filter_by(id=department_id) \
#             .first()
#
#     @staticmethod
#     def add(department: Department, session) -> None:
#         session.add(department)
#         session.commit()
#
#     @staticmethod
#     def update(self):
#         pass
#
#     @staticmethod
#     def delete(self):
#         pass
#
#
# class PermissionDAO:
#     @staticmethod
#     def get_all():
#         return Permission.query.all()
#
#     @staticmethod
#     def get_by_id(permission_id: str) -> Permission:
#         return Permission.query \
#             .filter_by(id=permission_id) \
#             .first()
#
#     @staticmethod
#     def add(permission: Permission, session) -> None:
#         session.add(permission)
#         session.commit()
#
#     @staticmethod
#     def update(self):
#         pass
#
#     @staticmethod
#     def delete(self):
#         pass
#
#
# class DepartmentPermissionDAO:
#     @staticmethod
#     def get_all():
#         return DepartmentPermission.query.all()
#
#     @staticmethod
#     def get_by_id(department_permission_id: str) -> DepartmentPermission:
#         return DepartmentPermission.query \
#             .filter_by(id=department_permission_id) \
#             .first()
#
#     @staticmethod
#     def add(department_permission: DepartmentPermission, session) -> None:
#         session.add(department_permission)
#         session.commit()
#
#     @staticmethod
#     def update(self):
#         pass
#
#     @staticmethod
#     def delete(self):
#         pass
