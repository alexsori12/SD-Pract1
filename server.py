from xmlrpc.server import SimpleXMLRPCServer
from multiprocessing import Process
from redis import Redis
from Worker import *

server = SimpleXMLRPCServer(('localhost', 9000))
server.register_introspection_functions()

WORKERS={}
WORKER_ID=0

redis = Redis()

def create_worker():
    global WORKERS
    global WORKER_ID

    proc = Process(target=worker.start_worker, args=(WORKER_ID,))
    proc.start()

    WORKERS[WORKER_ID] = proc
    WORKER_ID += 1

def delete_worker(id):
    global WORKERS
    Process = WORKERS[id].terminate()
    del WORKERS[id]
    print("Worker Borrado")

def numberOfWorkers():
    global WORKERS
    return len(WORKERS)

def list_workers():
    global WORKERS
    return WORKERS
    

def todo(param):
    # Encuarem a la cua de redis el metode
    return 0


server.register_function(create_worker, 'crearW')
server.register_function(delete_worker, 'borrarW')
server.register_function(todo, 'todo')

try:
    print('Use Control-C to exit')
    server.serve_forever()
except KeyboardInterrupt:
    print('Exiting')