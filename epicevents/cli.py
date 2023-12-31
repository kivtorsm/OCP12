import click
import jwt
import os
import textwrap
import stat

from datetime import datetime, timezone, timedelta

from argon2 import PasswordHasher, exceptions

from urllib.parse import urlparse

from models import start_db, Client, Contract, Event, Employee, Permission, DepartmentPermission, Department
from dao import ClientDAO, ContractDAO, EventDAO, EmployeeDAO, DepartmentPermissionDAO, PermissionDAO, DepartmentDAO
from views import CrudView, LoginView
from conf import SECRET, HOST, CREATE_TEST_DATA_PATH
from permissions import read_credentials, get_token_user_id

from permissions import is_allowed, is_authenticated

from mysql import connector


@click.group()
def cli():
    pass


@cli.command("login")
def login():
    """
    Instantiates login controller and launches authentication method
    """
    login = Login()
    login.authenticate()


class Login:
    """
    Login controller
    """
    def __init__(self):
        self.view = LoginView()

    def authenticate(self):
        """
        Authentication function
        """
        (email, password) = self.view.prompt_login_details()
        try:
            employee = self.get_employee(email)
        except IndexError:
            click.echo("\nAdresse mail et/ou mot de passe incorrect \n")
            exit()

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
            self.view.successful_login()

        except exceptions.VerifyMismatchError as err:
            click.echo(f"{err} : incorrect login or password")

    @staticmethod
    def get_employee(email):
        """
        Returns an employee with a given email
        """
        employee = EmployeeDAO.get_by_email(email)
        return employee

    @staticmethod
    def write_netrc(host: str, user: str, token: str):
        """
        Writes netrc file with authenticated user token info.
        """
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
    """
    General CRUD controller for all objects
    """
    def __init__(self):
        self.view = CrudView()

    @is_allowed
    def main_menu(self, objects_allowed: list = None):
        """
        Main menu controller. Allows user to enter CRUD options for a given object.
        """
        while True:
            choice = self.view.prompt_for_main_menu(objects_allowed)
            if choice == 'exit':
                exit()
            else:
                self.crud_menu(obj_type=choice)

    @is_allowed
    def crud_menu(self, obj_type: str, crud_actions_allowed: list = None):
        """
        Object controller with CRUD options allowed for the given user
        """
        while True:
            choice = self.view.prompt_for_crud_menu(obj_type, crud_actions_allowed=crud_actions_allowed)
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
                case 'filter_no_support':
                    self.filter_no_support()
                case 'filter_no_signature':
                    self.filter_no_signature(obj_type=obj_type)
                case 'filter_due_amount':
                    self.filter_due_amount(obj_type=obj_type)
                case 'filter_owned':
                    self.filter_owned(obj_type=obj_type)

    @is_allowed
    def filter_no_support(self, obj_type=None):
        """
        Filters all events with no support contact associated to the event.
        """
        obj_list = EventDAO.filter_no_support()
        self.view.show_obj_list(obj_list)

    @is_allowed
    def filter_no_signature(self, obj_type=None):
        """
        Filters unsigned contracts
        """
        obj_list = ContractDAO.filter_to_be_signed()
        self.view.show_obj_list(obj_list)

    @is_allowed
    def filter_due_amount(self, obj_type=None):
        """
        Filters contracts which have not been completely paid
        """
        obj_list = ContractDAO.filter_due_amount_higher_than_zero()
        self.view.show_obj_list(obj_list)

    @is_allowed
    def filter_owned(self, support_contact_id=None, obj_type=None):
        """
        Filters owned events by user. IE events for which the user is associated as a support contact.
        """
        obj_list = EventDAO.filter_owned(support_contact_id=support_contact_id)
        self.view.show_obj_list(obj_list)

    @is_allowed
    def create(self, obj_type: str):
        """
        Object creation controller
        """

        @is_allowed
        def get_input_data(obj_type: str, contract_id: int = None) -> dict:
            """
            Gets object data
            """
            obj_data = self.view.prompt_for_object_creation(obj_type)
            return obj_data

        contract_id = None

        if obj_type == 'event':
            contract_id = self.view.prompt_for_contract_id()
            obj_data = get_input_data(obj_type=obj_type, contract_id=contract_id)
        else:
            obj_data = get_input_data(obj_type=obj_type)

        obj = None

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
                    status="to_be_signed",
                )
                ContractDAO.add(obj)
            case 'event':
                contract = ContractDAO.get_by_id(contract_id)
                obj = Event(
                    client_id=contract.client_id,
                    contract_id=contract_id,
                    start_date=obj_data['start_date'],
                    end_date=obj_data['end_date'],
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

    @is_allowed
    def show_all(self, obj_type: str):
        """
        Shows all objects of a given type.
        """
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
        """
        Returns an object depending on the id.
        """
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

    @is_allowed
    def show_by_id(self, obj_type: str):
        """
        Shows object details with a given id
        """
        obj = self.get_object_by_id(obj_type, 'show')
        self.view.show_details(obj)

    @is_allowed
    def update(self, obj_type: str, obj: object, obj_fields_allowed: list = None):
        """
        Object update controller.
        """
        self.view.show_details(obj)
        field, new_value = self.view.prompt_for_object_field_update(obj, allowed_fields=obj_fields_allowed)

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
        """
        Object delete controller
        """
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
    """
    Launches app with the CRUD controller
    """
    obj_crud = ObjectsCrud()
    obj_crud.main_menu()


def execute_sql_script(filename):
    """
    Executes a sql script
    """
    # Open and read the file as a single buffer
    f = open(filename, 'r')
    sql_file = f.read()
    f.close()

    sql_commands = sql_file.split(';')

    DB_CONNEXION = connector.connect(
        host='localhost',
        user='app',
        passwd='password',
        database='epic_events'
    )

    cursor = DB_CONNEXION.cursor()

    for command in sql_commands:
        try:
            if command.strip() != '':
                cursor.execute(command)
        except IOError as msg:
            print(f"Command skipped: {msg}")

    DB_CONNEXION.commit()


if __name__ == "__main__":
    # start database on program start up
    start_db()

    # if the database is empty then initialise with test data
    if not EventDAO.get_all():
        click.echo('create_test_data')

        execute_sql_script(CREATE_TEST_DATA_PATH)

    # launch cli
    cli()
