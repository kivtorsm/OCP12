import click

from argon2 import PasswordHasher

from api import API

from apikey import (
    read_credentials,
    prompt_api_details,
    request_access_token,
    write_netrc,
)
from config import TWITTER_API
from display import Display

from models import start_db, Client, Contract, Event, Employee
from dao import ClientDAO, ContractDAO, EventDAO, EmployeeDAO
from views import CrudView


@click.group()
def cli():
    pass


@cli.command("login")
@click.option("--relogin", "-r", is_flag=True, help="Force a relogin.")
def login(relogin):
    apikey_configured = read_credentials(TWITTER_API) is not None
    if relogin:
        apikey_configured = False
    if not apikey_configured:
        try:
            (client_id, client_secret, app_name) = prompt_api_details()
            token = request_access_token(client_id, client_secret)
            write_netrc(TWITTER_API, app_name, token)
            click.echo("You've sucessfully logged in ✅")
        except Exception:
            click.echo("Failed to fetch your token, check your credentials! ❌")
    else:
        click.echo(
            "You're already logged in! 🔑 \nTry --relogin to update your credentials!"
        )


@cli.command("start")
def start():
    obj_crud = ObjectsCrud()
    obj_crud.main_menu()


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
                    self.create(obj_type)
                case 'show_all':
                    self.show_all(obj_type)
                case 'show_details':
                    self.show_by_id(obj_type)
                case 'update':
                    self.update(obj_type)
                case 'delete':
                    self.delete(obj_type)
                case 'exit':
                    break

    def create(self, obj_type: str):
        obj = None
        obj_data = self.view.prompt_for_object_creation(obj_type)
        match obj_type:
            case 'client':
                obj = Client(
                    first_name=obj_data['first_name'],
                    last_name=obj_data['last_name'],
                    email=obj_data['email'],
                    telephone=obj_data['telephone'],
                    company_name=obj_data['company_name'],
                    commercial_id=obj_data['commercial_id'],
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

    def update(self, obj_type: str):
        obj = self.get_object_by_id(obj_type, 'update')
        self.view.show_details(obj)
        field, new_value = self.view.prompt_for_object_field_update(obj)
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


if __name__ == "__main__":
    start_db()
    cli()
