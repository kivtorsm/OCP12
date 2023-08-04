from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Client, Employee, Contract, Event, Department, Permission, DepartmentPermission

from conf import session


class ClientDAO:
    @staticmethod
    def client_get_all():
        return session.query(Client).all()

    @staticmethod
    def client_get_by_id(client_id: int) -> Client:
        return session.query(Client).get(client_id)

    @staticmethod
    def client_add(client: Client) -> None:
        session.add(client)
        session.commit()

    def client_update(
            self,
            client_id: int,
            commercial_id: int = None,
            company_name: str = None,
            email: str = None,
            first_name: str = None,
            last_name: str = None,
            telephone: str = None
    ):
        db_client = self.client_get_by_id(client_id)
        db_client.commercial_id = commercial_id if commercial_id else db_client.commercial_id
        db_client.company_name = company_name if company_name else db_client.company_name
        db_client.email = email if email else db_client.email
        db_client.last_name = last_name if last_name else db_client.last_name
        db_client.first_name = first_name if first_name else db_client.first_name
        db_client.telephone = telephone if telephone else db_client.telephone
        session.commit()

    def client_delete(self, client_id: int):
        client_db = self.client_get_by_id(client_id)
        session.delete(client_db)
        session.commit()


class ContractDAO:
    @staticmethod
    def contract_get_all():
        return Contract.query.all()

    @staticmethod
    def contract_get_by_id(contract_id: str) -> Contract:
        return Contract.query \
            .filter_by(id=contract_id) \
            .first()

    @staticmethod
    def contract_add(contract: Contract, session) -> None:
        session.add(contract)
        session.commit()

    @staticmethod
    def contract_update():
        pass

    @staticmethod
    def contract_delete():
        pass


class EventDAO:
    @staticmethod
    def event_get_all():
        return Event.query.all()

    @staticmethod
    def event_get_by_id(event_id: str) -> Event:
        return Event.query \
            .filter_by(id=event_id) \
            .first()

    @staticmethod
    def event_add(event: Event, session) -> None:
        session.add(event)
        session.commit()

    @staticmethod
    def event_update():
        pass

    @staticmethod
    def event_delete():
        pass


class EmployeeDAO:
    @staticmethod
    def employee_get_all():
        return Employee.query.all()

    @staticmethod
    def employee_get_by_id(employee_id: str) -> Employee:
        return Employee.query \
            .filter_by(id=employee_id) \
            .first()

    @staticmethod
    def employee_add(employee: Employee, session) -> None:
        session.add(employee)
        session.commit()

    @staticmethod
    def employee_update(self):
        pass

    @staticmethod
    def employee_delete(self):
        pass


class DepartmentDAO:
    @staticmethod
    def department_get_all():
        return Department.query.all()

    @staticmethod
    def department_get_by_id(department_id: str) -> Department:
        return Department.query \
            .filter_by(id=department_id) \
            .first()

    @staticmethod
    def department_add(department: Department, session) -> None:
        session.add(department)
        session.commit()

    @staticmethod
    def department_update(self):
        pass

    @staticmethod
    def department_delete(self):
        pass


class PermissionDAO:
    @staticmethod
    def permission_get_all():
        return Permission.query.all()

    @staticmethod
    def permission_get_by_id(permission_id: str) -> Permission:
        return Permission.query \
            .filter_by(id=permission_id) \
            .first()

    @staticmethod
    def permission_add(permission: Permission, session) -> None:
        session.add(permission)
        session.commit()

    @staticmethod
    def permission_update(self):
        pass

    @staticmethod
    def permission_delete(self):
        pass


class DepartmentPermissionDAO:
    @staticmethod
    def department_permission_get_all():
        return DepartmentPermission.query.all()

    @staticmethod
    def department_permission_get_by_id(department_permission_id: str) -> DepartmentPermission:
        return DepartmentPermission.query \
            .filter_by(id=department_permission_id) \
            .first()

    @staticmethod
    def department_permission_add(department_permission: DepartmentPermission, session) -> None:
        session.add(department_permission)
        session.commit()

    @staticmethod
    def department_permission_update(self):
        pass

    @staticmethod
    def department_permission_delete(self):
        pass
