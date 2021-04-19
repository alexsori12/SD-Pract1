import json
import re
import string

def start_worker(id, redisS):
    #FALTA UN DO WHILE INFINITO  
    while True:
        task = redisS.blpop('op', timeout=0)
        #print("     Tasca agafadas")
        tasca = json.loads(task[1])
        request_id = tasca["request_id"]
        
        semafor = str(request_id) + 'semafor'
        redisS.blpop(semafor, timeout=0)


        if tasca["operacio"] == "suma":
            suma(request_id, redisS)
        elif tasca["operacio"] == "count":
            countingWords(request_id, redisS, tasca["parametros"])
        elif tasca["operacio"] == "wordcount":
            wordCount(request_id, redisS, tasca["parametros"])
        else:
            #ARREGLAR ESTE APARTAT
            print("operacio no declarada")
        

        if tasca["end"] == "True":
            cua = str(request_id) + 'resposta'
            redisS.rpush(cua, redisS.get(request_id))
        else:
            redisS.rpush(semafor, '1')



def llegirFitxer(archiu):
    #Utilitzar el archiu
    document_text = open(archiu,"r")
    text_string = document_text.read().lower()
    return text_string.split()

def suma(request_id, redisS):
    antic = redisS.get(request_id)
    if antic == None: 
        antic = 0
        
    nou = int(antic) + 1
    redisS.set(request_id, str(nou))
    
def  countingWords(request_id, redisS, archiu):
    
    antic = redisS.get(request_id)
    if antic == None: 
        antic = 0
    
    llistaP = llegirFitxer(archiu)
    cont = len(llistaP)
    nou = int(antic) + cont
    redisS.set(request_id, str(nou))
   

def wordCount(request_id, redisS, archiu):

    antic = redisS.get(request_id)
    if antic != None:
        dicc_general = json.loads(antic)
    else:
        dicc_general = {}
    
    llistaP = llegirFitxer(archiu)
    
    for word in llistaP:
        if word in dicc_general:
            dicc_general[word] += 1
        else:
            dicc_general[word] = 1

    redisS.set(request_id, str(json.dumps(dicc_general)))

    
   
