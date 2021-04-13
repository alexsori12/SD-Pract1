import xmlrpc.client

server = xmlrpc.client.ServerProxy('http://localhost:9000')
print("hola")
print("Creamos Worker" % server.crear())
print("adeu1")
print("Creamos Worker" % server.tasca("maria","pepe"))
print("adeu")