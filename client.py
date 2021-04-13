import xmlrpc.client

server = xmlrpc.client.ServerProxy('http://localhost:9000')

print("Creamos Worker" % server.create_worker())
print("Creamos Worker" % server.create_worker())
print("Creamos Worker" % server.create_worker())