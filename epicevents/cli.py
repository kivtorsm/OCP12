import click
import jwt
import os
import textwrap
import stat

from typing import Tuple, Union
from datetime import datetime, timezone, timedelta

from argon2 import PasswordHasher, exceptions

from urllib.parse import urlparse

from display import Display

from models import start_db, Client, Contract, Event, Employee, Permission, DepartmentPermission, Department
from dao import ClientDAO, ContractDAO, EventDAO, EmployeeDAO, DepartmentPermissionDAO, PermissionDAO, DepartmentDAO
from views import CrudView, LoginView
from conf import session

display = Display()

HOST = "http://localhost:8000"

absolute_path = os.path.dirname(__file__)
relative_path = '../.ssh/secret.txt'
full_path = os.path.join(absolute_path, relative_path)

with open(full_path) as f:
    SECRET = str(f.readlines())


@click.group()
def cli():
    pass


def find_netrc_token(machine: str, raise_errors=False):
    NETRC_FILES = (".netrc", "_netrc")
    netrc_file = os.environ.get("NETRC")
    if netrc_file is not None:
        netrc_locations = (netrc_file,)
    else:
        netrc_locations = ("~/{}".format(f) for f in NETRC_FILES)

    try:
        from netrc import netrc, NetrcParseError

        netrc_path = None

        for f in netrc_locations:
            try:
                loc = os.path.expanduser(f)
            except KeyError:
                return

            if os.path.exists(loc):
                netrc_path = loc
                break

        if netrc_path is None:
            return

        ri = urlparse(machine)

        host = ri.netloc.split(":")[0]

        try:
            _netrc = netrc(netrc_path).authenticators(host)
            if _netrc:
                login_i = 0 if _netrc[0] else 1
                return (_netrc[login_i], _netrc[2])
        except (NetrcParseError, IOError):
            if raise_errors:
                raise

    except (ImportError, AttributeError):
        pass


def read_credentials(machine: str) -> Union[Tuple[str, str], None]:
    user, token = None, None
    auth = find_netrc_token(machine, True)
    if auth and auth[0] and auth[1]:
        user = auth[0]
        token = auth[1]
        return (user, token)


def get_token_payload(token):
    return jwt.decode(token, key=SECRET, algorithms="HS256")


def get_token():
    credentials = read_credentials(HOST)
    return credentials[1]


def get_token_user_id():
    token = get_token()
    payload = get_token_payload(token)
    user = EmployeeDAO.get_by_email(payload['email'])
    return user.id


def is_authenticated(func):
    def wrapper():
        credentials = read_credentials(HOST)
        existing_token = credentials is not None
        if existing_token:
            try:
                jwt.decode(credentials[1], key=SECRET, algorithms="HS256")
                if func is not None:
                    func()
                # return True
            except jwt.ExpiredSignatureError:
                click.echo(f"Connexion expirée, connectez-vous à nouveau.")
                # return False
        # else:
        #     return False
    return wrapper


def is_allowed(func):
    allowed = "client_create"

    def wrapper(*args, **kwargs):

        if func.__name__ == ('show_all' or 'show_details'):
            func(*args, **kwargs)
        else:
            # Check which object types the user is allowed to create
            credentials = read_credentials(HOST)
            token = credentials[1]
            payload = get_token_payload(token)
            department_id = payload['department_id']
            department = DepartmentDAO.get_by_id(department_id)
            department_permissions = department.department_permissions
            employee_id = EmployeeDAO.get_by_email(payload['email']).id
            EMPLOYEE_FIELD_NAMES = {
                'contract': f"client.commercial_id={employee_id}",
                'event': f"support_contact_id={employee_id}",
                'client': f"commercial_id={employee_id}",
            }
            obj_type_allowed = [
                dpt_perm.permission.object_type
                for dpt_perm in department_permissions
                if dpt_perm.permission.crud_action == func.__name__
            ]

            if func.__name__ == ('create' or 'delete'):
                # Verify that the object type creation requested in the function is in the list of types allowed
                if kwargs['obj_type'] in obj_type_allowed:
                    func(*args, **kwargs)
                else:
                    click.echo("not allowed '\n")
            elif func.__name__ == 'update':
                # check if user has permission for that type of object
                if kwargs['obj_type'] in obj_type_allowed:
                    # objects allowed in database
                    objects_allowed = [
                        dpt_perm.permission.object_list
                        for dpt_perm in department_permissions
                        if dpt_perm.permission.crud_action == func.__name__
                    ]
                    object_list_allowed = None

                    # construction of command string to get list of allowed objects
                    # general case (all)
                    match objects_allowed[0]:
                        case 'all':
                            match kwargs['obj_type']:
                                case 'client':
                                    object_list_allowed = ClientDAO.get_all()
                                case 'contract':
                                    object_list_allowed = ContractDAO.get_all()
                                case 'event':
                                    object_list_allowed = EventDAO.get_all()
                    # other cases
                    match objects_allowed[0]:
                        case 'owned':
                            match kwargs['obj_type']:
                                case 'client':
                                    object_list_allowed = ClientDAO.filter_by_attr(commercial_id=employee_id)
                                case 'contract':
                                    object_list_allowed = ContractDAO.filter_by_attr(client__commercial_id=employee_id)
                                case 'event':
                                    object_list_allowed = EventDAO.filter_by_attr(support_contact_id=employee_id)

                    # check if the object included in the attributes is included in the allowed_list
                    if kwargs['obj'] in object_list_allowed:
                        # fields allowed in database
                        fields_allowed = [
                            dpt_perm.permission.object_field
                            for dpt_perm in department_permissions
                            if dpt_perm.permission.crud_action == func.__name__
                        ][0]
                        if fields_allowed == 'all':
                            fields_allowed = None
                        func(*args, **kwargs, obj_fields_allowed=fields_allowed)

    return wrapper


@cli.command("login")
def login():
    login = Login()
    login.authenticate()


class Login:
    def __init__(self):
        self.view = LoginView()

    def authenticate(self):
        (email, password) = self.view.prompt_login_details()
        employee = self.get_employee(email)

        try:
            password_hasher = PasswordHasher()
            password_hasher.verify(employee.encoded_hash, password)
            payload = {
                "email": email,
                "department_id": employee.department_id,
                "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=500)
            }
            token = jwt.encode(payload=payload, key=SECRET)

            self.write_netrc(HOST, email, token)
            read_credentials(HOST)
            self.view.succesful_login()

        except exceptions.VerifyMismatchError as err:
            display.error(f"{err} : incorrect login or password")

    @staticmethod
    def get_employee(email):
        employee = EmployeeDAO.get_by_email(email)
        return employee

    @staticmethod
    def write_netrc(host: str, user: str, token: str):
        normalized_host = urlparse(host).netloc.split(":")[0]
        if normalized_host != "localhost" and "." not in normalized_host:
            return None
        machine_line = "machine %s" % normalized_host
        path = os.path.expanduser("~/.netrc")
        orig_lines = None
        with open(path) as f:
            orig_lines = f.read().strip().split("\n")
        with open(path, "w") as f:
            if orig_lines:
                skip = 0
                for line in orig_lines:
                    if line == "machine " or machine_line in line:
                        skip = 2
                    elif skip:
                        skip -= 1
                    else:
                        f.write("%s\n" % line)
            f.write(
                textwrap.dedent(
                    """\
            machine {host}
              login {user}
              password {token}
            """
                ).format(host=normalized_host, user=user, token=token)
            )
        os.chmod(os.path.expanduser("~/.netrc"), stat.S_IRUSR | stat.S_IWUSR)
        return True


class ObjectsCrud:
    def __init__(self):
        self.view = CrudView()

    def main_menu(self):
        while True:
            choice = self.view.prompt_for_main_menu()
            if choice == 'exit':
                exit()
            else:
                self.crud_menu(choice)

    def crud_menu(self, obj_type: str):
        while True:
            choice = self.view.prompt_for_crud_menu(obj_type)
            match choice:
                case 'create':
                    self.create(obj_type=obj_type)
                case 'show_all':
                    self.show_all(obj_type=obj_type)
                case 'show_details':
                    self.show_by_id(obj_type=obj_type)
                case 'update':
                    obj = self.get_object_by_id(obj_type, 'update')
                    self.update(obj_type=obj_type, obj=obj)
                case 'delete':
                    self.delete(obj_type=obj_type)
                case 'exit':
                    break

    @is_allowed
    def create(self, obj_type: str):
        obj = None
        obj_data = self.view.prompt_for_object_creation(obj_type)
        match obj_type:
            case 'client':
                commercial_id = get_token_user_id()
                obj = Client(
                    first_name=obj_data['first_name'],
                    last_name=obj_data['last_name'],
                    email=obj_data['email'],
                    telephone=obj_data['telephone'],
                    company_name=obj_data['company_name'],
                    commercial_id=commercial_id,
                )
                ClientDAO.add(obj)
            case 'contract':
                obj = Contract(
                    client_id=obj_data['client_id'],
                    total_amount=obj_data['total_amount'],
                    due_amount=obj_data['due_amount'],
                    status=obj_data['status'],
                )
                ContractDAO.add(obj)
            case 'event':
                obj = Event(
                    client_id=obj_data['client_id'],
                    contract_id=obj_data['contract_id'],
                    start_date=obj_data['start_date'],
                    end_date=obj_data['end_date'],
                    support_contact_id=obj_data['support_contact_id'],
                    location=obj_data['location'],
                    attendees_number=obj_data['attendees_number'],
                    notes=obj_data['notes'],
                )
                EventDAO.add(obj)
            case 'employee':
                ph = PasswordHasher()
                obj_data["encoded_hash"] = ph.hash(obj_data['encoded_hash'])
                obj = Employee(
                    first_name=obj_data['first_name'],
                    last_name=obj_data['last_name'],
                    email=obj_data['email'],
                    department_id=obj_data['department_id'],
                    encoded_hash=obj_data['encoded_hash'],
                )
                EmployeeDAO.add(obj)
        self.view.prompt_for_confirmation('create', obj_type, obj)

    def show_all(self, obj_type: str):
        obj_list = []
        match obj_type:
            case 'client':
                obj_list = ClientDAO.get_all()
            case 'contract':
                obj_list = ContractDAO.get_all()
            case 'event':
                obj_list = EventDAO.get_all()
            case 'employee':
                obj_list = EmployeeDAO.get_all()
        self.view.show_obj_list(obj_list)

    def get_object_by_id(self, obj_type: str, change: str):
        obj = None
        obj_id = self.view.prompt_for_object_id(change, obj_type)
        match obj_type:
            case 'client':
                obj = ClientDAO.get_by_id(obj_id)
            case 'contract':
                obj = ContractDAO.get_by_id(obj_id)
            case 'event':
                obj = EventDAO.get_by_id(obj_id)
            case 'employee':
                obj = EmployeeDAO.get_by_id(obj_id)
        return obj

    def show_by_id(self, obj_type: str):
        obj = self.get_object_by_id(obj_type, 'show')
        self.view.show_details(obj)

    @is_allowed
    def update(self, obj_type: str, obj: object, obj_fields_allowed: list = None):

        self.view.show_details(obj)
        field, new_value = self.view.prompt_for_object_field_update(obj, obj_fields_allowed)
        command = ""
        match obj_type:
            case 'client':
                command = f"ClientDAO.update(ClientDAO, obj.id, {field}='{new_value}')"
            case 'contract':
                command = f"ContractDAO.update(ContractDAO, obj.id, {field}='{new_value}')"
            case 'event':
                command = f"EventDAO.update(EventDAO, obj.id, {field}='{new_value}')"
            case 'employee':
                command = f"EmployeeDAO.update(EmployeeDAO, obj.id, {field}='{new_value}')"
        exec(command)
        self.view.prompt_for_confirmation('update', obj_type, obj)

    def delete(self, obj_type: str):
        obj = self.get_object_by_id(obj_type, 'delete')
        self.view.show_details(obj)
        match obj_type:
            case 'client':
                ClientDAO.delete(ClientDAO, obj.id)
            case 'contract':
                ContractDAO.delete(ContractDAO, obj.id)
            case 'event':
                EventDAO.delete(EventDAO, obj.id)
            case 'employee':
                EmployeeDAO.delete(EmployeeDAO, obj.id)
        self.view.prompt_for_confirmation('delete', obj_type, obj)


@cli.command("start")
@is_authenticated
def start():
    obj_crud = ObjectsCrud()
    obj_crud.main_menu()


if __name__ == "__main__":
    start_db()
    cli()
