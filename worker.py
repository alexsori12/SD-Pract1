import json
import re
import string

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

        if tasca["operacio"] == "suma":
            suma(request_id,redisS)
        elif tasca["operacio"] == "count":
            countingWords(request_id,redisS,tasca["parametros"])
        elif tasca["operacio"] == "wordcount":
            wordCount(request_id,redisS,tasca["parametros"])
        else:
            #ARREGLAR ESTE APARTAT
            print("operacio no declarada")
        
        if tasca["end"] == "True":
            print("     END TRUE")
            cua =str(request_id) + 'resposta'
            redisS.rpush(cua,str(int(redisS.get(request_id))))
        else:
            redisS.rpush(semafor,'1')
        
        #print("     Adeeeeeeeeeeeeeeeeeeeeeeeeeeu")
        
def suma(request_id, redisS):
    antic = redisS.get(request_id)
    print('Valor antic:', antic)
    nou = int(antic) + 1
    print('Valor nou:', nou)
    redisS.set(request_id,str(nou))
    
def  countingWords(request_id, redisS, archiu):
    llistaP = comu(archiu)

    cont = len(llistaP)
    antic = redisS.get(request_id)
    nou = int(antic) + cont
    redisS.set(request_id,str(nou))

def comu(archiu):
    #Utilitzar el archiu
    document_text = open("/mnt/c/Users/Victor/Documents/GitHub/SD-Pract1/files/Text2.txt","r")
    text_string = document_text.read().lower()
    return text_string.split()
   

def wordCount(request_id, redisS, archiu):
    llistaP = comu(archiu)
    frecuenciaPalab = []
    for word in llistaP:
        frecuenciaPalab.append(llistaP.count(word))

    #Guarda a REDIS, la pregunta es com?
    print("Pares\n" + str(list(zip(llistaP, frecuenciaPalab))))

