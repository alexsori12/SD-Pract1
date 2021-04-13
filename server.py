from xmlrpc.server import SimpleXMLRPCServer
from multiprocessing import Process
import worker
from redis import Redis
import json


server = SimpleXMLRPCServer(('localhost', 9000), allow_none=True)
server.register_introspection_functions()


WORKERS={}
WORKER_ID=0

redisS = Redis()


def start_worker(id):  
    print("HOLAAAAAAAAA SOC WORKER")
    task = redisS.blpop(["op",0])
    print(id)
    print(task)


def create_worker():
    global WORKERS
    global WORKER_ID
    
    proc = Process(target=start_worker, args=(WORKER_ID,))
    proc.start()

    WORKERS[WORKER_ID] = proc
    WORKER_ID += 1

def delete_worker(id):
    global WORKERS
    WORKERS[id].terminate()
    del WORKERS[id]
    print("Worker Borrado")

def numberOfWorkers():
    global WORKERS
    return len(WORKERS)

def list_workers():
    global WORKERS
    return WORKERS
    

def do_tasks(func, param):
    print("Tasca pujada")
    dades = {
        "operacio": func,
        "parametre": param,
    }
    
    redisS.rpush("op", json.dumps(dades))
    print("Completat")
   

server.register_function(create_worker, 'crear')
server.register_function(delete_worker, 'borrar')
server.register_function(numberOfWorkers, 'numero')
server.register_function(list_workers, 'lista')
server.register_function(do_tasks, 'tasca')


try:
    print('Use Control-C to exit')
    server.serve_forever()
except KeyboardInterrupt:
    print('Exiting')