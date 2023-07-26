class Client:
    def __init__(
        self,
        client_id=None,
        first_name=None,
        last_name=None,
        email=None,
        telephone=None,
        company_name=None,
        created=None,
        modified=None,
        commercial_id=None,
    ):
        client_id = client_id
        first_name = first_name
        last_name = last_name
        email = email
        telephone = telephone
        company_name = company_name
        created = created
        modified = modified
        commercial_id = commercial_id


class Contract:
    def __init__(
        self,
        contract_id=None,
        client_id=None,
        total_amount=None,
        due_amount=None,
        created=None,
        status=None,
    ):
        contract_id = contract_id
        client_id = client_id
        total_amount = total_amount
        due_amount = due_amount
        created = created
        status = status


class Event:
    def __init__(
        self,
        event_id=None,
        contract_id=None,
        client_id=None,
        start_date=None,
        end_date=None,
        support_contact_id=None,
        location=None,
        attendees=None,
        notes=None,
    ):
        event_id = event_id
        contract_id = contract_id
        client_id = client_id
        start_date = start_date
        end_date = end_date
        support_contact_id = support_contact_id
        location = location
        attendees = attendees
        notes = notes


class Employee:
    def __init__(
        self,
        employee_id=None,
        first_name=None,
        last_name=None,
        email=None,
        department_id=None,
        encoded_hash=None,
    ):
        employee_id = employee_id
        first_name = first_name
        last_name = last_name
        email = email
        department_id = department_id
        encoded_hash = encoded_hash

    def authenticate(self):
        pass


class Department:
    def __init__(
        self,
        department_id=None,
        name=None,
    ):
        department_id = department_id
        name = name


class Permission:
    def __init__(
        self,
        permission_id=None,
        name=None,
    ):
        permission_id = permission_id
        name = name


class DepartmentPermission:
    def __init__(
        self,
        department_permission_id=None,
        department_id=None,
        permission_id=None,
    ):
        department_permission_id = department_permission_id
        department_id = department_id
        permission_id = permission_id
