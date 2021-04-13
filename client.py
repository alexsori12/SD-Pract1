import xmlrpc.client

server = xmlrpc.client.ServerProxy('http://localhost:9000')
server.crear()
server.tasca("maria","pepe")