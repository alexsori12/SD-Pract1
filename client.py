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
def suma(urls):
    click.echo("Resultat Suma "+ str(server.tasca('suma',urls))) 
    
@click.command()
@click.argument('urls', nargs=-1)
def count(urls):
     click.echo("Resultat Count "+ str(server.tasca('count',urls)))

@click.command()
@click.argument('urls', nargs=-1)
def wordcount(urls):
     click.echo("Resultat Count "+ str(server.tasca('wordcount',urls)))

cli.add_command(wordcount)
cli.add_command(suma)
cli.add_command(count)
cli.add_command(delete)

if __name__ == '__main__':
    cli()