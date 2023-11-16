import requests
import json
import time

#---IMPUTS--- 
#nombre del invocador
nombre_invocador = "pablo911"

#Key de la Api
key = ""

#región a la que pertenece
region = "euw1"
region2 = "europe"


#---DATOS DE LA CUENTA---
#Peticion para pedir datos de la cuenta dando el nombre invocador
peticion1 = requests.get("https://" + region + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + nombre_invocador + "?api_key=" + key)

#Variable json con datos del player
datos = peticion1.json()

#puuid de cada player
puuid = datos['puuid']


level = datos['summonerLevel']

#---FUNCIONES SECUNDARIAS
#convertir segundos
def epoch(hora):
    epoch_actual = int(time.time() * 1000)  # La función time.time() devuelve segundos, por lo que multiplicamos por 1000
    diferencia_milisegundos = epoch_actual - hora
    segundos = diferencia_milisegundos // 1000
    minutos = segundos // 60
    horas = minutos // 60
    dias = horas // 24
    horas %= 24
    minutos %= 60
    segundos %= 60
    resultado = "días: " + str(dias)+ ", horas: "+ str(horas) + ", minutos:" +str(minutos)
    return resultado



#---FUNCIONES PRINCIPALES---

#Devuelve el nomrbe de invocador y el nivel del jugador
def nombre_y_nivel():
    res = ("{:<20} {:<15}".format(str(nombre_invocador),"Nivel: "+str(level)))

    return res

# Devuelve una lista con los personajes con mas maestria 
def maestria_campeones_all():
    resultado=""

    #Print inicial
    resultado2 =  ""

    #---LISTA DE CHAMPIONS MAESTRIA---
    #Peticion para pedir lista de campeones con maestria
    peticion2 = requests.get("https://" + region + ".api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/"+puuid+"?api_key="+ key)

    #Variable json con lista de campeones y maestria
    datos = peticion2.json()

    #Abrir archivo IdToChamp.json donde estan todos los CHAMPS y sus ID
    with open('Principal/IdToChamp.json', 'r') as archivo_original:
        global listaIdChamp 
        listaIdChamp = json.load(archivo_original)

    suma = 0

    #Por cada champ imprime su nombre, puntos de maestria y ultima vez jugado.
    for i in datos:
        
        idChamp = i['championId']
        puntosmaestria = format(i['championPoints'],",d").replace(",",".")

        lastPlayed = i['lastPlayTime']
        lastPlayed2 = epoch(lastPlayed)
        suma = suma + int(i['championPoints'])
        resultado = resultado + ("{:<20}{:<20} {:<20}".format(str(listaIdChamp[str(idChamp)]['name']),"Maestria: " +  puntosmaestria,"Última vez jugado: " + str(lastPlayed2)))+ "\n"

    t_suma = "{:,}"
    p_suma = t_suma.format(suma).replace(",",".")
    resultado = resultado + ("\n")
    resultado = resultado + ("{:<20} {:<15}".format("Total de puntos: ",p_suma))

    return resultado2 + resultado
          
# Devuelve lista con personajes con mas maestria de cada posicion Valores disponibles -> (top,jungla,mid,adc,support)
def maestria_campeones_rol(rol):
    resultado=""

    #Print inicial 
    resultado2 =  ""

    #---LISTA DE CHAMPIONS MAESTRIA---
    #Peticion para pedir lista de campeones con maestria
    peticion2 = requests.get("https://" + region + ".api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/"+puuid+"?api_key="+ key)

    #Variable json con lista de campeones y maestria
    datos = peticion2.json()

    #Abrir archivo IdToChamp.json donde estan todos los CHAMPS y sus ID
    with open('Principal/IdToChamp.json', 'r') as archivo_original:
        global listaIdChamp 
        listaIdChamp = json.load(archivo_original)

    #Abrir archivo IdToChamp.json donde estan todos los CHAMPS y sus ID
    with open('Principal/ChampToRole.json', 'r') as archivo_original:
        global listaRol
        listaRol = json.load(archivo_original)

    suma = 0

    #Por cada champ imprime su nombre, puntos de maestria y ultima vez jugado.
    for i in datos:
        idChamp = i['championId']
        nombreChamp = listaIdChamp[str(idChamp)]['name']
        roles = listaRol[str(nombreChamp)]['rol']
        if(rol in roles):

            lastPlayed = i['lastPlayTime']
            lastPlayed2 = epoch(lastPlayed)
            puntosmaestria = format(i['championPoints'],",d").replace(",",".")
            suma = suma + int(i['championPoints'])
            resultado = resultado + ("{:<20} {:<20} {:<20}".format(str(listaIdChamp[str(idChamp)]['name']),"Maestria: " +  puntosmaestria,"Última vez jugado: " + str(lastPlayed2)))+ "\n"

    t_suma = "{:,}"
    p_suma = t_suma.format(suma).replace(",",".")
    resultado = resultado + ("\n")
    resultado = resultado + ("{:<20} {:<15}".format("Total de puntos: ",p_suma))

    return resultado2 + resultado

# Devuelve lista con personajes con mas maestria de cada posicion Valores disponibles -> (top,jungla,mid,adc,support) (ORDENADA POR LAST TIME PLAYED)
def maestria_campeones_rol_ordenado_hora(rol):
    resultado=""

    #Print inicial -----LISTA DE MAESTRIAS EN HORAS-----
    resultado2 =  ""

    #---LISTA DE CHAMPIONS MAESTRIA---
    #Peticion para pedir lista de campeones con maestria
    peticion2 = requests.get("https://" + region + ".api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/"+puuid+"?api_key="+ key)

    #Variable json con lista de campeones y maestria
    datos = peticion2.json()

    #Abrir archivo IdToChamp.json donde estan todos los CHAMPS y sus ID
    with open('Principal/IdToChamp.json', 'r') as archivo_original:
        global listaIdChamp 
        listaIdChamp = json.load(archivo_original)

    #Abrir archivo IdToChamp.json donde estan todos los CHAMPS y sus ID
    with open('Principal/ChampToRole.json', 'r') as archivo_original:
        global listaRol
        listaRol = json.load(archivo_original)

    suma = 0
    lista =  []

    #Por cada champ imprime su nombre, puntos de maestria y ultima vez jugado.
    for i in datos:
        idChamp = i['championId']
        nombreChamp = listaIdChamp[str(idChamp)]['name']
        roles = listaRol[str(nombreChamp)]['rol']
        if(rol in roles):

            lastPlayed = i['lastPlayTime']
            lastPlayed2 = epoch(lastPlayed)
            puntosmaestria = format(i['championPoints'],",d").replace(",",".")
            suma = suma + int(i['championPoints'])
            var = (("{:<20} {:<20} {:<20}".format(str(listaIdChamp[str(idChamp)]['name']),"Maestria: " +  puntosmaestria,"Última vez jugado: " + str(lastPlayed2)))+ "\n")
            lista.append((var,lastPlayed))

    mi_lista_ordenada = sorted(lista, key=lambda x: int(x[1]), reverse=True)
    valor_x = ""
    for tupla in mi_lista_ordenada:
        valor_x = valor_x  + str(tupla[0])

    t_suma = "{:,}"
    p_suma = t_suma.format(suma).replace(",",".")
    resultado = resultado + ("\n")
    resultado = resultado + ("{:<20} {:<15}".format("Total de puntos: ",p_suma))

    return resultado2 + valor_x + resultado

# Devuelve una lista con los personajes con mas maestria (ORDENADA POR LAST TIME PLAYED)
def maestria_campeones_all_ordenado_hora():
    resultado=""

    #Print inicial
    resultado2 =  ""

    #---LISTA DE CHAMPIONS MAESTRIA---
    #Peticion para pedir lista de campeones con maestria
    peticion2 = requests.get("https://" + region + ".api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/"+puuid+"?api_key="+ key)

    #Variable json con lista de campeones y maestria
    datos = peticion2.json()

    #Abrir archivo IdToChamp.json donde estan todos los CHAMPS y sus ID
    with open('Principal/IdToChamp.json', 'r') as archivo_original:
        global listaIdChamp 
        listaIdChamp = json.load(archivo_original)

    suma = 0
    lista = []

    #Por cada champ imprime su nombre, puntos de maestria y ultima vez jugado.
    for i in datos:
        
        idChamp = i['championId']
        puntosmaestria = format(i['championPoints'],",d").replace(",",".")

        lastPlayed = i['lastPlayTime']
        lastPlayed2 = epoch(lastPlayed)
        suma = suma + int(i['championPoints'])
        var = (("{:<20} {:<20} {:<20}".format(str(listaIdChamp[str(idChamp)]['name']),"Maestria: " +  puntosmaestria,"Última vez jugado: " + str(lastPlayed2)))+ "\n")
        lista.append((var,lastPlayed))

    mi_lista_ordenada = sorted(lista, key=lambda x: int(x[1]), reverse=True)
    valor_x = ""
    for tupla in mi_lista_ordenada:
        valor_x = valor_x  + str(tupla[0])
    t_suma = "{:,}"
    p_suma = t_suma.format(suma).replace(",",".")
    resultado = resultado + ("\n")
    resultado = resultado + ("{:<20} {:<15}".format("Total de puntos: ",p_suma))

    return resultado2 + valor_x + resultado

#Devuelve una lista de "x" games de un usuario Rango Valido -> (1-100)
def lista_games(total):
    #Print inicial
    resultado2 =  ""

    #Abrir archivo IdToChamp.json donde estan todos los CHAMPS y sus ID
    with open('Principal/IdToQueue.json', 'r') as archivo_queue:
        global archivo_colas
        archivo_colas = json.load(archivo_queue)

    #---LISTA DE CHAMPIONS MAESTRIA---
    #Peticion para pedir lista de campeones con maestria
    peticionLM = requests.get("https://" + region2 + ".api.riotgames.com/lol/match/v5/matches/by-puuid/"+puuid+"/ids?start=0&count="+str(total)+"&api_key="+ key)
    datos = peticionLM.json()
    
    for i in datos:
            print(i)
            peticion = requests.get("https://" + region2 + ".api.riotgames.com/lol/match/v5/matches/" +str(i) + "?api_key="+ key)
            datos_2pet = peticion.json()
            dato_match = datos_2pet['info']['participants']

            cola_nombre = ""
            dato_gamemode = datos_2pet['info']['queueId']
            for k in archivo_colas:
                if k['queueId'] == dato_gamemode: 
                    cola_nombre = k['description']
                    break

            if "games" in cola_nombre:
                cola_nombre = cola_nombre.replace(" games","")
            
            for l in dato_match:
                if(l['summonerName'] == nombre_invocador): datos_jugador = l
            #datos win or loss

            win = "LOSS"
            if(datos_jugador['win']==True):win = "WIN"

            resultado2 += "{:<4} {:<10} {}/{}/{} {:<10}\n".format(win, datos_jugador['championName'], datos_jugador['kills'], datos_jugador['deaths'] ,datos_jugador['assists'],cola_nombre)
    return resultado2

#Devuelve una lista de "x" games de un usuario de una cola especiífica -> (5v5 Ranked Solo, 5v5 ARAM,...)
def lista_games_cola(total,cola): 
    #Print inicial
    resultado2 =  ""

    #Abrir archivo IdToChamp.json donde estan todos los CHAMPS y sus ID
    with open('Principal/IdToQueue.json', 'r') as archivo_queue:
        global archivo_colas
        archivo_colas = json.load(archivo_queue)

    contador = 0
    iteraciones = 0

    while(contador < total):

        #---LISTA DE CHAMPIONS MAESTRIA---
        #Peticion para pedir lista de campeones con maestria
        peticionLM = requests.get("https://" + region2 + ".api.riotgames.com/lol/match/v5/matches/by-puuid/"+puuid+"/ids?start="+str(iteraciones)+"&count="+str(int(total)-contador)+"&api_key="+ key)
        datos = peticionLM.json()
        
        for i in datos:
                iteraciones+=1
                peticion = requests.get("https://" + region2 + ".api.riotgames.com/lol/match/v5/matches/" +str(i) + "?api_key="+ key)
                datos_2pet = peticion.json()
                dato_match = datos_2pet['info']['participants']

                cola_nombre = ""
                dato_gamemode = datos_2pet['info']['queueId']

                for k in archivo_colas:
                    if k['queueId'] == dato_gamemode: 
                        cola_nombre = k['description']
                        break

                if "games" in cola_nombre:
                    cola_nombre = cola_nombre.replace(" games","")
                    
                if(cola_nombre == cola):
                    
                    for l in dato_match:
                        if(l['summonerName'] == nombre_invocador): datos_jugador = l
                    #datos win or loss

                    win = "LOSS"
                    if(datos_jugador['win']==True):win = "WIN"
                    contador+=1
                    resultado2 += "{:<4} {:<10} {}/{}/{} {:<10}\n".format(win, datos_jugador['championName'], datos_jugador['kills'],  datos_jugador['deaths'],datos_jugador['assists'],cola_nombre)
    return resultado2

#-----PRINTS-----#
#print( puuid)
#print(nombre_y_nivel())
#print(maestria_campeones_all())
#print(maestria_campeones_all_ordenado_hora())
#print(maestria_campeones_rol('mid'))
#print(maestria_campeones_rol_ordenado_hora('mid'))
#print(lista_games(2))
#print(lista_games_cola(20,'5v5 Ranked Solo'))