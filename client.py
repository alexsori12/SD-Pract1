import xmlrpc.client
import click

server = xmlrpc.client.ServerProxy('http://localhost:9000')

@click.group()
def cli():
    pass

@cli.command()
def create():
    server.crear()

@cli.command()
def number():
    click.echo("Numero de Workers: "+ str(server.numero())) 

@cli.command()
def lista():
    server.lista()

@click.command()
@click.argument('id')
def delete(id):
    server.borrar(int(id))

@click.command()
@click.argument('urls', nargs=-1)
def tasca1(urls):
    server.tasca('op1',urls)

@click.command()
@click.argument('urls', nargs=-1)
def tasca2(urls):
    server.tasca('op2',urls)

cli.add_command(tasca1)
cli.add_command(tasca2)
cli.add_command(delete)

if __name__ == '__main__':
    cli()