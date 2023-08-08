from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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
        return Contract.query.all()

    @staticmethod
    def get_by_id(contract_id: str) -> Contract:
        return Contract.query \
            .filter_by(id=contract_id) \
            .first()

    @staticmethod
    def add(contract: Contract, session) -> None:
        session.add(contract)
        session.commit()

    @staticmethod
    def update():
        pass

    @staticmethod
    def delete():
        pass


class EventDAO:
    @staticmethod
    def get_all():
        return Event.query.all()

    @staticmethod
    def get_by_id(event_id: str) -> Event:
        return Event.query \
            .filter_by(id=event_id) \
            .first()

    @staticmethod
    def add(event: Event, session) -> None:
        session.add(event)
        session.commit()

    @staticmethod
    def update():
        pass

    @staticmethod
    def delete():
        pass


class EmployeeDAO:
    @staticmethod
    def get_all():
        return Employee.query.all()

    @staticmethod
    def get_by_id(employee_id: str) -> Employee:
        return Employee.query \
            .filter_by(id=employee_id) \
            .first()

    @staticmethod
    def add(employee: Employee, session) -> None:
        session.add(employee)
        session.commit()

    @staticmethod
    def update(self):
        pass

    @staticmethod
    def delete(self):
        pass


class DepartmentDAO:
    @staticmethod
    def get_all():
        return Department.query.all()

    @staticmethod
    def get_by_id(department_id: str) -> Department:
        return Department.query \
            .filter_by(id=department_id) \
            .first()

    @staticmethod
    def add(department: Department, session) -> None:
        session.add(department)
        session.commit()

    @staticmethod
    def update(self):
        pass

    @staticmethod
    def delete(self):
        pass


class PermissionDAO:
    @staticmethod
    def get_all():
        return Permission.query.all()

    @staticmethod
    def get_by_id(permission_id: str) -> Permission:
        return Permission.query \
            .filter_by(id=permission_id) \
            .first()

    @staticmethod
    def add(permission: Permission, session) -> None:
        session.add(permission)
        session.commit()

    @staticmethod
    def update(self):
        pass

    @staticmethod
    def delete(self):
        pass


class DepartmentPermissionDAO:
    @staticmethod
    def get_all():
        return DepartmentPermission.query.all()

    @staticmethod
    def get_by_id(department_permission_id: str) -> DepartmentPermission:
        return DepartmentPermission.query \
            .filter_by(id=department_permission_id) \
            .first()

    @staticmethod
    def add(department_permission: DepartmentPermission, session) -> None:
        session.add(department_permission)
        session.commit()

    @staticmethod
    def update(self):
        pass

    @staticmethod
    def delete(self):
        pass
