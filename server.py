from xmlrpc.server import SimpleXMLRPCServer
from multiprocessing import Process
import worker as wk
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

    WORKERS[WORKER_ID] = proc
    print(str(proc))
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
    print(type(WORKERS))
    return "hola"
    

def do_tasks(func, params):
    global REQUEST_ID
    request_id = REQUEST_ID
    REQUEST_ID+=1
    
    dades = {
        "operacio": func,
        "parametros": 'X',
        "request_id": request_id,
        'end': "False",
    }
    
    for i in range(0,len(params)-1):
        dades['parametros'] = params[i]
        redisS.rpush("op", json.dumps(dades))

    dades['parametros'] = params[len(params)-1]
    dades['end'] = "True"
    redisS.set(str(request_id),"0")
    redisS.rpush("op", json.dumps(dades))
   
    print("adpegooooooooo")
    result= redisS.blpop("ap 0")[0]

    print("RESULTADO")
    print(str(result[1]))
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