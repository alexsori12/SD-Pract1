CLIENT

Llibreries:
xmlrpc

Definició:
Arxiu python que donarà peticions de feina al servidor

Peticions:
create() -> crea worker
number()-> nº de workers
lista() -> llista de workers
delete(id) -> borra worker segons paràmetre
suma(urls) -> conta el nº de paràmetres
count(urls)
wordcount(urls)




SERVER

Llibreries:
xmlrpc
multiprocessing
redis
json
threading

Definició:
Arxiu python que gestiona els workers i tracta les peticions delegant-les als workers

Funcions:
create_worker() -> crea worker
delete_worker(id) -> borra worker segons paràmetre
numberOfWorkers() -> nº de workers
list_workers() -> llista de workers
do_tasks(func, params) -> envia la funció a una cua que tracten els workers, indicada per primer paràmetre i els paràmetres en el segon

Observacions:
Al final del arxiu, es pot observar com registrem la informació enviada desde el client al servidor.
El servidor es capaç de gestionar invocacions simples i múltiples.




WORKER

Llibreries:
json
re
urllib.request

Definició:
Arxiu python que tracta les peticions desde una cua i envia el resultat al SERVER

Funcions:
start_worker() -> Cicle infinit del worker, on tracta les peticions
merge() -> funció que ajunta els resultats d'una tasca i ho retorna al SERVER
llegirFitxer() -> obra un fitxer i retorna el text d'una web
suma() -> suma 1 a la cua
countingWords() -> conta les paraules d'un fitxer
wordCount() -> crea un diccionari amb els cops que apareix cada paraula



PER EXECUTAR

Primer iniciem el servidor de redis fent un redis-server, fem un flushall per tal de borrar contingut de la BD, llavors obrim el servidor amb un (python3 ./server.py), i ja podem iniciar el client.

Si fem un (python3 ./client.py "opció" ) sense opció ens sortiran una llista de totes les opcions que pot fer el client. (Hem de executar el client.py per cada opcio que es vulgui executar)

Per realitzar les funcions de count i wordcount, hem de fer un servidor http on estiguen els fitxers:
cd /directori/fitxers
python3 -m http.server

I ja podrem executar 
python3 ./client.py count http://localhost:8000/Text1.txt http://localhost:8000/Text2.txt 
