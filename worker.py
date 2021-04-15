import json

def start_worker(id, redisS):
    #FALTA UN DO WHILE INFINITO  
    while True:
        #print("     HOLAAAAAAAAA SOC WORKER")
        task= redisS.blpop('op', timeout=0)

        #print("     Tasca agafadas")
        tasca  = json.loads(task[1])
        request_id = tasca["request_id"]
        
        semafor =str(request_id) + 'semafor'
        redisS.blpop(semafor, timeout=0)

        antic = redisS.get(request_id)
        print('Valor antic:', antic)
        nou = int(antic) + 1
        print('Valor nou:', nou)
        redisS.set(request_id,str(nou))
        
        
        if tasca["end"] == "True":
            print("     END TRUE")
            cua =str(request_id) + 'resposta'
            redisS.rpush(cua,str(int(antic)+1))
        else:
            redisS.rpush(semafor,'1')
        
        #print("     Adeeeeeeeeeeeeeeeeeeeeeeeeeeu")
        


