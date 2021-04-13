from server import redisS

def start_worker():  
    print("HOLAAAAAAAAA SOC WORKER")
    task = redisS.blpop(["op",0])
    print(task)

