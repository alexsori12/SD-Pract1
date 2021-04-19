import json
import re
import string
import urllib.request

def start_worker(id, redisS):

    while True:
        task = redisS.blpop('op', timeout=0)
        tasca = json.loads(task[1])

        if tasca["operacio"] == "suma":
            suma(tasca, redisS)
        elif tasca["operacio"] == "count":
            countingWords(tasca, redisS)
        elif tasca["operacio"] == "wordcount":
            wordCount(tasca, redisS)
        elif tasca["operacio"] == "merge_resultados":
            merge(tasca, redisS)


def merge(tasca, redisS ):
    cont = 0
    if tasca["word_merge"] == "True":
        result = {}
        while cont < tasca["numero_param"]:
            aux = redisS.blpop(tasca["request_id"], timeout=0)
            nou_dicc = json.loads(aux[1])
            print(nou_dicc)
            for word in nou_dicc.keys():
                if word in result:
                    nou = int(result[word]) + int(nou_dicc[word])
                    result[word] = nou
                else:
                    result[word] = int(nou_dicc[word])
            cont += 1    
        result = str(json.dumps(result))
    else:
        result = 0
        while cont < tasca["numero_param"]:
            aux = redisS.blpop(tasca["request_id"], timeout=0)
            result += int(aux[1])
            cont += 1
    
    cua = str(tasca["request_id"]) + 'resposta'
    redisS.rpush(cua, result)

def llegirFitxer(arxiu):                     
 
    document_text = urllib.request.urlopen(arxiu).read().decode('utf-8')
    text_string = document_text.lower()
    return text_string.split()

def suma(tasca, redisS):
    redisS.rpush(tasca["request_id"], 1)
    
def  countingWords(tasca, redisS):
    
    llistaP = llegirFitxer(tasca["parametros"])
    n_palabras = len(llistaP)
    redisS.rpush(tasca["request_id"], n_palabras)
   

def wordCount(tasca, redisS):

    dicc_general = {}
    
    llistaP = llegirFitxer(tasca["parametros"])
    
    for word in llistaP:
        if word in dicc_general:
            dicc_general[word] += 1
        else:
            dicc_general[word] = 1

    redisS.rpush(tasca["request_id"], str(json.dumps(dicc_general)))