import click

from src.apikey import prompt_api_details
@click.group()
def cli():
    """
    Slice of ML or sliceofml is your little 🍰 of ML.
    """


@cli.command("login")
@click.option("--relogin", "-r", is_flag=True)
def login(relogin):
    (client_id, client_secret, app_name) = prompt_api_details()

    click.echo(f"""🔑 Your Super Secret Credentials 🔑
        Client ID: {client_id}
        Client Secret: {client_secret}
        App Name: {app_name}""")

@cli.command("slice")
@click.option("--daily", "frequency", flag_value="daily", default=True)
@click.option("--weekly", "frequency", flag_value="weekly")
def slice(frequency):
    click.echo(frequency)
