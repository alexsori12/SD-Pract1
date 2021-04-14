import json

def start_worker(id, redisS):
    #FALTA UN DO WHILE INFINITO  
    while True:
        print("     HOLAAAAAAAAA SOC WORKER")
        task= redisS.blpop(["op",0])
        print("     Tasca agafadas")
        tasca  = json.loads(task[1])
        request_id = tasca["request_id"]
        
        antic = redisS.get(request_id)
        redisS.set(request_id,str(int(antic)+1))

            
        if tasca["end"] == "True":
            print("     END TRUE")
            redisS.rpush("ap","3")
        
        print("     Adeeeeeeeeeeeeeeeeeeeeeeeeeeu")
        


