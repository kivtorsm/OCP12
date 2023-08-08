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

from models import Client
from dao import ClientDAO
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


@cli.command("client_crud")
def client_crud_menu():
    view = ClientView()
    while True:
        choice = view.prompt_for_client_crud_menu()
        commands = {
            'create_client': 'create_client()',
            'show_all_clients': 'show_all_clients()',
            'show_client_detail': 'show_client_by_id()',
            'update_client': 'update_client()',
            'delete_client': 'delete_client()',
            'exit': 'exit()'
        }

        choice_command = commands[choice]
        exec(choice_command)


def create_client():
    view = ClientView()
    client_data = view.prompt_for_client_creation()
    client = Client(
        first_name=client_data['first_name'],
        last_name=client_data['last_name'],
        email=client_data['email'],
        telephone=client_data['telephone'],
        company_name=client_data['company_name'],
        commercial_id=client_data['commercial_id'],
    )
    # print(client)
    ClientDAO.client_add(client)
    # TODO : retour utilisateur confirmation création client


def show_all_clients():
    clients = ClientDAO.client_get_all()
    view = ClientView()
    view.show_client_list(clients)



def show_client_by_id():
    view = ClientView()
    action = "show"
    client_id = view.prompt_for_client_id(action)
    client = ClientDAO.client_get_by_id(client_id)
    view.show_client_details(client)


def update_client():
    view = ClientView()
    action = "delete"
    client_id = view.prompt_for_client_id(action)
    client = ClientDAO.client_get_by_id(client_id)
    view.show_client_details(client)
    field, new_value = view.prompt_for_client_field_update(client)
    command = f"ClientDAO.client_update(ClientDAO, client_id, {field}='{new_value}')"
    exec(command)
    # TODO : généraliser à n'importe quel champ


def delete_client():
    view = ClientView()
    action = "delete"
    client_id = view.prompt_for_client_id(action)

    ClientDAO.client_delete(ClientDAO, client_id)


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
