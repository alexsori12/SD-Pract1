def start_worker(id, redisS):  
    print("HOLAAAAAAAAA SOC WORKER")
    task = redisS.blpop(["op",0])
    print('id '+str(id))
    print(task)
