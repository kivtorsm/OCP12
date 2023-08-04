import click

from sqlalchemy.orm import sessionmaker

from api import API

from apikey import (
    read_credentials,
    prompt_api_details,
    request_access_token,
    write_netrc,
)
from config import TWITTER_API
from display import Display

from models import start_db, Client
from dao import ClientDAO


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


@cli.command("slice")
@click.option(
    "--daily",
    "frequency",
    flag_value="daily",
    default=True,
    help="Fetch the Top ML tweets for the past 24 hours.",
)
@click.option(
    "--weekly",
    "frequency",
    flag_value="weekly",
    help="Fetch the Top ML tweets for the past 7 days.",
)
def slice(frequency):
    display = Display()
    credentials = read_credentials(TWITTER_API)
    if credentials is None:
        display.error("Please login before running this command! ❌")
        return
    tweets = API(credentials[0], credentials[1], TWITTER_API).query(frequency)
    display.tweetsAsTable(tweets, frequency)


def create_client():
    client = Client(first_name="Victor",
                    last_name="Serradilla",
                    email="nom.prenom@gmail.com",
                    telephone="+33666666666",
                    company_name="company",
                    commercial_id=1,
                    )
    ClientDAO.client_add(client)


def get_all_clients():
    [print(client) for client in ClientDAO.client_get_all()]


def get_client_by_id(client_id: int):
    return ClientDAO.client_get_by_id(client_id)


def update_client(client_id: int, client2: Client):
    # client_dao = ClientDAO()
    ClientDAO.client_update(ClientDAO, client_id, last_name=client2.last_name)


def delete_client(client_id: int):
    # client_dao = ClientDAO()
    ClientDAO.client_delete(ClientDAO, client_id)


if __name__ == "__main__":
    # start_db()
    client = Client(first_name="Victor",
                    last_name="Serradilla",
                    email="nom.prenom@gmail.com",
                    telephone="+33666666666",
                    company_name="company",
                    commercial_id=1,
                    )
    create_client()
    print(get_client_by_id(1))

    client2 = Client(
        first_name="Victor",
        last_name="Mazuelas",
        email="nom.prenom@gmail.com",
        telephone="+33666666666",
        company_name="company",
        commercial_id=1,
    )
    update_client(1, client2)
    get_all_clients()
    delete_client(1)
    # delete_client(2)
    get_all_clients()

    # cli()

