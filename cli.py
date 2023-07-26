import click


@click.group()
def cli():
    """
    Slice of ML or sliceofml is your little 🍰 of ML.
    """


@cli.command("login")
@click.option("--relogin", "-r", is_flag=True)
def login(relogin):
    click.echo(relogin)


@cli.command("slice")
@click.option("--daily", "frequency", flag_value="daily", default=True)
@click.option("--weekly", "frequency", flag_value="weekly")
def slice(frequency):
    click.echo(frequency)
