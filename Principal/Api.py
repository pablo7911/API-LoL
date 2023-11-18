import requests
import json
import time

#---IMPUTS--- 
#nombre del invocador
nombre_invocador = "pablo911"

#Key de la Api
key = "RGAPI-5897f2b0-cd0d-4375-88ee-cd4ef48cadd1"

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

def total_carreo(datos): #[kills, asistencias, daño, oro, daño_torres, control_ward, wards, wards_quitados,muertes]
    pesos = [1.65, 1.5, 1.1, 0.8, 0.8, 0.4, 0.7, 0.6, -1.55]

    def calcular_rendimiento_jugador(jugador):
        return sum(jugador[i] * pesos[i] for i in range(9)) / 9

    def calcular_equipo_rendimiento(equipo):
        return [calcular_rendimiento_jugador(jugador) for jugador in equipo]

    equipo_1 = datos[0]
    equipo_2 = datos[1]

    rendimientos_equipo_1 = calcular_equipo_rendimiento(equipo_1)
    rendimientos_equipo_2 = calcular_equipo_rendimiento(equipo_2)

    return [rendimientos_equipo_1, rendimientos_equipo_2]



def carreo_partida(id): #lineas->(TOP,JUNGLE,MIDDLE,BOTTOM,UTILITY)
    peticion = requests.get("https://" + region2 + ".api.riotgames.com/lol/match/v5/matches/" +str(id)+ "?api_key="+ key)
    players = peticion.json()['info']['participants']

    equipo1_win = False
    top1 = []
    top1n = []
    top2 = []
    top2n = []
    jungle1 = []
    jungle1n = []
    jungle2 = []
    jungle2n = []
    mid1 = []
    mid1n = []
    mid2 = []
    mid2n = []
    adc1 = []
    adc1n = []
    adc2 = []
    adc2n = []
    supp1 = []
    supp1n = []
    supp2 = []
    supp2n = []

    for i in players:

        datos = [i['kills'],i['assists'],i['totalDamageDealtToChampions'],i['goldEarned'],i['damageDealtToTurrets'],i['visionWardsBoughtInGame'],i['wardsPlaced'],i['wardsKilled'],i['deaths']]
        posicion = i['teamPosition']
        print(posicion)
        print(datos)
        print(i['teamId'])
        if(str(i['teamId']) == "100" ):
            equipo1_win = i['win']
            if(str(posicion) == "TOP"):
                top1 = datos
                top1n = i['championName']
            elif(str(posicion) == "JUNGLE"):
                jungle1 = datos
                jungle1n = i['championName']
            elif(str(posicion) == "MIDDLE"):
                mid1 = datos                
                mid1n = i['championName']                
            elif(str(posicion) == "BOTTOM"):
                adc1 = datos
                adc1n = i['championName']
            elif(str(posicion) == "UTILITY"):
                supp1 = datos                
                supp1n = i['championName']               
        elif (str(i['teamId']) == "200"):
            if(str(posicion) == "TOP"):
                top2 = datos
                top2n = i['championName']
            elif(str(posicion) == "JUNGLE"):
                jungle2 = datos
                jungle2n = i['championName']
            elif(str(posicion) == "MIDDLE"):
                mid2 = datos
                mid2n = i['championName']
            elif(str(posicion) == "BOTTOM"):
                adc2 = datos
                adc2n = i['championName']
            elif(str(posicion) == "UTILITY"):
                supp2 = datos
                supp2n = i['championName']

    conjunto_datos = [[top1,jungle1,mid1,adc1,supp1],[top2,jungle2,mid2,adc2,supp2]]
    carreos = total_carreo(conjunto_datos)
    porcentajes_redondeados = []
    print(carreos)
    for subconjunto in carreos:
        # Calcula la suma total del subconjunto
        total_subconjunto = sum(subconjunto)

        # Calcula el porcentaje para cada número del subconjunto y redondea a 2 cifras decimales
        porcentajes = [(numero / total_subconjunto) * 100 for numero in subconjunto]
        porcentajes_redondeados.append([round(porcentaje, 2) for porcentaje in porcentajes])
    print(porcentajes_redondeados)
    print("///")



    if(equipo1_win == True):
        dato_win_o_loss = "WIN"
        dato_win_o_loss2 = "LOSS"
    else:
        dato_win_o_loss = "LOSS"
        dato_win_o_loss2 = "WIN"

    resultado = "Equipo 1: ("+dato_win_o_loss+"):\n" 
    resultado += str(top1n) + " -> " + str(top1[0]) + " / " + str(top1[8]) + " / " + str(top1[1]) + " puntuación carreo -> " + str(porcentajes_redondeados[0][0]) + "%\n"        
    resultado += str(jungle1n) + " -> " + str(jungle1[0]) + " / " + str(jungle1[8]) + " / " + str(jungle1[1]) + " puntuación carreo -> " + str(porcentajes_redondeados[0][1]) + "%\n"      
    resultado += str(mid1n) + " -> " + str(mid1[0]) + " / " + str(mid1[8]) + " / " + str(mid1[1]) + " puntuación carreo -> " + str(porcentajes_redondeados[0][2]) + "%\n"       
    resultado += str(adc1n) + " -> " + str(adc1[0]) + " / " + str(adc1[8]) + " / " + str(adc1[1]) + " puntuación carreo -> " + str(porcentajes_redondeados[0][3]) + "%\n"        
    resultado += str(supp1n) + " -> " + str(supp1[0]) + " / " + str(supp1[8]) + " / " + str(supp1[1]) + " puntuación carreo -> " + str(porcentajes_redondeados[0][4]) + "%\n" 
    resultado +=  "\n"  
    resultado += "Equipo 2: ("+dato_win_o_loss2+"):\n" 
    resultado += str(top2n) + " -> " + str(top2[0]) + " / " + str(top2[8]) + " / " + str(top2[1]) + " puntuación carreo -> " + str(porcentajes_redondeados[1][0]) + "%\n"        
    resultado += str(jungle2n) + " -> " + str(jungle2[0]) + " / " + str(jungle2[8]) + " / " + str(jungle2[1]) + " puntuación carreo -> " + str(porcentajes_redondeados[1][1]) + "%\n"      
    resultado += str(mid2n) + " -> " + str(mid2[0]) + " / " + str(mid2[8]) + " / " + str(mid2[1]) + " puntuación carreo -> " + str(porcentajes_redondeados[1][2]) + "%\n"       
    resultado += str(adc2n) + " -> " + str(adc2[0]) + " / " + str(adc2[8]) + " / " + str(adc2[1]) + " puntuación carreo -> " + str(porcentajes_redondeados[1][3]) + "%\n"        
    resultado += str(supp2n) + " -> " + str(supp2[0]) + " / " + str(supp2[8]) + " / " + str(supp2[1]) + " puntuación carreo -> " + str(porcentajes_redondeados[1][4]) + "%\n" 

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
                print(i)
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
#print(lista_games(15))
#print(lista_games_cola(20,'5v5 Ranked Solo'))
print(carreo_partida('EUW1_6679852408'))