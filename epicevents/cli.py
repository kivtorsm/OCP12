import click

from api import API

from apikey import (
    read_credentials,
    prompt_api_details,
    request_access_token,
    write_netrc,
)
from config import TWITTER_API
from display import Display

from models import Client, Contract, Event, Employee
from dao import ClientDAO, ContractDAO, EventDAO, EmployeeDAO
from views import ClientView


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


@cli.command("main")
def main_menu():
    view = ClientView()
    while True:
        choice = view.prompt_for_main_menu()
        if choice=='exit':
            exit()
        else:
            crud_menu(choice)


# @cli.command("client_crud")
def crud_menu(obj_type: str):
    view = ClientView()
    while True:
        choice = view.prompt_for_crud_menu(obj_type)
        match choice:
            case 'create':
                create(obj_type)
            case 'show_all':
                show_all(obj_type)
            case 'show_details':
                show_by_id(obj_type)
            case 'update':
                update(obj_type)
            case 'delete':
                delete(obj_type)
            case 'exit':
                break

        # commands = {
        #     'create_client': 'create_client()',
        #     'show_all_clients': 'show_all_clients()',
        #     'show_client_detail': 'show_client_by_id()',
        #     'update_client': 'update_client()',
        #     'delete_client': 'delete_client()',
        #     'exit': 'exit()'
        # }
        #
        # choice_command = commands[choice]
        # exec(choice_command)


def create(obj_type: str):
    view = ClientView()
    obj = None
    match obj_type:
        case 'client':
            obj_data = view.prompt_for_client_creation()
            obj = Client(
                first_name=obj_data['first_name'],
                last_name=obj_data['last_name'],
                email=obj_data['email'],
                telephone=obj_data['telephone'],
                company_name=obj_data['company_name'],
                commercial_id=obj_data['commercial_id'],
            )
            ClientDAO.add(obj)
    view.prompt_for_confirmation('create', obj_type, obj)


def show_all(obj_type: str):
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
    view = ClientView()
    view.show_obj_list(obj_list)


def get_object_by_id(obj_type: str, change: str):
    view = ClientView()
    obj = None
    obj_id = view.prompt_for_object_id(change, obj_type)
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


def show_by_id(obj_type: str):
    view = ClientView()
    obj = get_object_by_id(obj_type, 'show')
    view.show_details(obj)


def update(obj_type: str):
    view = ClientView()
    obj = get_object_by_id(obj_type, 'update')
    view.show_details(obj)
    field, new_value = view.prompt_for_object_field_update(obj)
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
    view.prompt_for_confirmation('update', obj_type, obj)


def delete(obj_type: str):
    view = ClientView()
    obj = get_object_by_id(obj_type, 'delete')
    view.show_details(obj)
    match obj_type:
        case 'client':
            ClientDAO.delete(ClientDAO, obj.id)
        case 'contract':
            ContractDAO.delete(ContractDAO, obj.id)
        case 'event':
            EventDAO.delete(EventDAO, obj.id)
        case 'employee':
            EmployeeDAO.delete(EmployeeDAO, obj.id)
    view.prompt_for_confirmation('delete', obj_type, obj)

if __name__ == "__main__":
    # start_db()
    # client = Client(first_name="Victor",
    #                 last_name="Serradilla",
    #                 email="nom.prenom@gmail.com",
    #                 telephone="+33666666666",
    #                 company_name="company",
    #                 commercial_id=1,
    #                 )
    # create_client()
    # print(get_client_by_id(1))
    #
    # client2 = Client(
    #     first_name="Victor",
    #     last_name="Mazuelas",
    #     email="nom.prenom@gmail.com",
    #     telephone="+33666666666",
    #     company_name="company",
    #     commercial_id=1,
    # )
    # update_client(1, client2)
    # get_all_clients()
    # delete_client(1)
    # # delete_client(2)
    # get_all_clients()

    cli()
