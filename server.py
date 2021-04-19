from xmlrpc.server import SimpleXMLRPCServer
from multiprocessing import Process
import worker as wk
import threading
from redis import Redis
import json


server = SimpleXMLRPCServer(('localhost', 9000), allow_none=True)
server.register_introspection_functions()


WORKERS={}
WORKER_ID=0
REQUEST_ID=0

redisS = Redis()

def create_worker():
    global WORKERS
    global WORKER_ID
    
    proc = Process(target=wk.start_worker, args=(WORKER_ID,redisS))
    proc.start()

    WORKERS[str(WORKER_ID)] = proc
    WORKER_ID += 1

def delete_worker(id):
    global WORKERS

    WORKERS[str(id)].terminate()
    del WORKERS[str(id)]

def numberOfWorkers():
    global WORKERS

    return len(WORKERS)

def list_workers():
    global WORKERS

    workers_list = {}
  
    for worker in WORKERS.keys():
        workers_list[worker] = str(WORKERS[worker])
    
    return workers_list
    

def do_tasks(func, params):
    global REQUEST_ID
    request_id = REQUEST_ID
    REQUEST_ID += 1

    dades = {
        "operacio": func,
        "parametros": 'X',
        "request_id": request_id,
        'end': "False",
    }

    semafor = str(request_id) + 'semafor'
    redisS.rpush(semafor, '1' )

    for i in range(0, len(params)-1):
        dades['parametros'] = params[i]
        redisS.rpush("op", json.dumps(dades))

    dades['parametros'] = params[len(params)-1]
    dades['end'] = "True"
    redisS.rpush("op", json.dumps(dades))

    cua = str(request_id) + 'resposta'
    result = redisS.blpop(cua, timeout=0)
    
    redisS.delete(str(request_id))
    
    return result[1]


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