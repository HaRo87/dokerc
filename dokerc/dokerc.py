import click


@click.group()
def cli():
    pass


@click.command()
def info():
    click.echo('DokerC a small CLI client for the Doker Backend.')
    click.echo('Checkout https://haro87.github.io/doker-meta for further info.')


cli.add_command(info)
