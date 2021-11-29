#!/usr/bin/env python3
# -*- coding: utf-8 -

from sys import argv
import socket
import asyncio
import random

players = []
tables = [] #liste des tables
listeNbRounds = [] #permet d'avoir tous les nbrounds

#def nextPlayer(player):
    #for playerIT in players:
        #if playerIT != player:
            #return playerIT

async def code200(writer,message):
    msg = "200: " + message
    writer.write(msg.encode() + b"\r\n")

async def jouerUnePartie(reader,writer,nbrounds):
    scoreJ = 0
    scoreIA = 0
    while nbrounds > 0:
        msg = 300 + nbrounds
        score = str(scoreJ) + "-" + str(scoreIA)
        codeEntree = str(msg) + ":" + score
        writer.write(codeEntree.encode() + b"\r\n")
        coupj1 = await reader.readline()
        coupj1 = coupj1.decode()
        coupIA = random.randint(0, 2)
        print("L'IA joue :" + str(coupIA))
        print("J1 joue : " + str(coupj1))
        if coupj1[6] == "0":
            if coupIA == 0 :
                print("Egalité")
            elif coupIA == 1:
                scoreIA += 1
                print("J1 perd")
            elif coupIA == 2:
                scoreJ += 1
                print("J1 gagne")
        elif coupj1[6] == "1":
            if coupIA == 0:
                scoreJ += 1
                print("J1 gagne")
            elif coupIA == 1:
                print("Egalité")
            elif coupIA == 2:
                scoreIA += 1
                print("J1 perd")
        elif coupj1[6] == "2":
            if coupIA == 0:
                scoreIA += 1
                print("J1 perd")
            elif coupIA == 1:
                scoreJ += 1
                print("J1 gagne")
            elif coupIA == 2:
                print("Egalité")

        nbrounds -= 1

    score = str(scoreJ) + "-" + str(scoreIA)
    if scoreJ < scoreIA :
        gagnant = " L'IA a gagné !"
        codeSortie = "300: " + score + gagnant
        writer.write(codeSortie.encode())
    elif scoreJ > scoreIA:
        gagnant = " Vous avez gagné !"
        codeSortie = "300: " + score + gagnant
        writer.write(codeSortie.encode())
    elif scoreJ == scoreIA:
        gagnant = " Match nul !"
        codeSortie = "300: " + score + gagnant
        writer.write(codeSortie.encode())

    writer.close()

async def jouerPartie1vs1(player1,player2,k,i):
    scoreJ1 = 0
    scoreJ2 = 0
    while k > 0:
        msg = 300 + k
        score = str(scoreJ1) + "-" + str(scoreJ2)
        code = str(msg) + ":" + score
        player1[0].write(code.encode() + b"\r\n")
        player2[0].write(code.encode() + b"\r\n")
        coupJ1 = await player1[1].readline()
        coupJ1 = coupJ1.decode()
        coupJ2 = await player2[1].readline()
        coupJ2 = coupJ2.decode()
        print("J1 JOUE :", coupJ1)
        print("J2 JOUE :", coupJ2)
        if (coupJ1[6] == "0"):
            if coupJ2[6] == "0" :
                print("Egalité")
            elif coupJ2[6] == "1":
                scoreJ2 += 1
                print("J2 gagne")
            elif coupJ2[6] == "2":
                scoreJ1 += 1
                print("J1 gagne")
        elif coupJ1[6] == "1":
            if coupJ2[6] == "0":
                scoreJ1 += 1
                print("J1 gagne")
            elif coupJ2[6] == "1":
                print("Egalité")
            elif coupJ2[6] == "2":
                scoreJ2 += 1
                print("J2 gagne")
        elif coupJ1[6] == "2":
            if coupJ2[6] == "0":
                scoreJ2 += 1
                print("J2 gagne")
            elif coupJ2[6] == "1":
                scoreJ1 += 1
                print("J1 gagne")
            elif coupJ2[6] == "2":
                print("Egalité")
        k -= 1

    score = str(scoreJ1) + "-" + str(scoreJ2)
    if scoreJ1 < scoreJ2 :
        gagnant = " J2 a gagné !"
        codeSortie = "300: " + score + gagnant
        player1[0].write(codeSortie.encode())
        player2[0].write(codeSortie.encode())
    elif scoreJ1 > scoreJ2:
        gagnant = " J1 a gagné !"
        codeSortie = "300: " + score + gagnant
        player1[0].write(codeSortie.encode())
        player2[0].write(codeSortie.encode())
    elif scoreJ1 == scoreJ2:
        gagnant = " Match nul !"
        codeSortie = "300: " + score + gagnant
        player1[0].write(codeSortie.encode())
        player2[0].write(codeSortie.encode())


    player1[0].close()
    player2[0].close()
    tables.pop(i)



async def configPartie(reader,writer):
    message=""
    await code200(writer,message)
    data = await reader.readline()
    data = data.decode().strip()
    if data[6] == "0":
        print("mode 0")
        await partieIA(reader,writer)
    elif data[6] == "1":
        print("mode 1")
        player=[writer,reader]
        players.append(player)
        await tableSansNom(player)
    elif data[6] == "2":
        print("mode 2")
        player=[writer,reader]
        players.append(player)
        await creerTable(player)
    elif data[6] == "3":
        print("mode 3")
        player=[writer,reader]
        players.append(player)
        await joindreTable(player)
    else :
        print("format du message incorrect")

async def creerTable(player):
    message = "nom de la table :"
    await code200(player[0],message)
    data = await player[1].readline()
    data = data.decode()
    nomTable = data[7:-2]
    tableExistante = False
    for tableIT in tables :
        if tableIT[0] == nomTable:
            tableExistante = True

    while nomTable == "" or tableExistante == True :
        tableExistante = False
        player[0].write(b'400\n')
        data = await player[1].readline()
        data = data.decode()
        nomTable = data[7:-2]
        for tableIT in tables :
            if tableIT[0] == nomTable:
                tableExistante = True
                break

    message = ""
    await code200(player[0],message)
    data = await player[1].readline()
    data = data.decode()
    nbrounds = int(data[10:-2])

    while nbrounds == 0 or not(data[10:-2].isdigit()):
        player[0].write(b'400\n')
        data = await player[1].readline()
        data = data.decode()
        nbrounds = int(data[10:-2])

    listeNbRounds.append(nbrounds)
    table = [nomTable,nbrounds,player]
    tables.append(table)
    player[0].write(b'202\n')


async def joindreTable(player):
    message = "nom de la table :"
    await code200(player[0],message)
    data = await player[1].readline()
    data = data.decode()
    nomTable = data[7:-2]
    tableExistante = False
    i = 0

    for tableIT in tables :
        if tableIT[0] == nomTable:
            tableExistante = True
            table = tableIT
            break
        i += 1

    if tableExistante == False:
        player[0].write(b'500\n')
        player[0].close()

    player[0].write(b'201\n')
    table.append(player)
    await jouerPartie1vs1(table[2],table[3],table[1],i)




async def tableSansNom(player):

    message = "nombre de coups :"
    await code200(player[0],message)
    data = await player[1].readline()
    data = data.decode()
    nbrounds = int(data[10:-2])

    while nbrounds == 0 or not(data[10:-2].isdigit()):
        player[0].write(b'400\n')
        data = await player[1].readline()
        data = data.decode()
        nbrounds = int(data[10:-2])

    await code200(player[0],message)

    listeNbRounds.append(nbrounds)
    creerTable = False #variable permettant de vérifier si on a mis un joueur seul dans une table

    if len(tables) < 1:
        table = ["table1",nbrounds,player]
        tables.append(table)
        player[0].write(b'202\n')
    else :
        for i in range(len(tables)):
            if listeNbRounds[i] == nbrounds:
                tables[i].append(player)
                table = tables[i]
                creerTable = True
                player[0].write(b'201\n')
                await jouerPartie1vs1(table[2],table[3],nbrounds,i)

        if creerTable == False:
            num_table = str(i) #le nom de la table = le nb d'itération i
            table = ["table2" + num_table,nbrounds,player]
            player[0].write(b'202\n')


async def partieIA(reader,writer):
    message = "nombre de coups :"
    await code200(writer,message)
    data = await reader.readline()
    data = data.decode()
    nbrounds = int(data[10:-2])
    while nbrounds == 0 or not(data[10:-2].isdigit()):
        writer.write(b'400\n')
        data = await reader.readline()
        data = data.decode()
        nbrounds = int(data[10:-2])

    message = "La partie commence"
    await code200(writer,message)
    await jouerUnePartie(reader,writer,nbrounds)

async def servershifumi():
    myHostName = socket.gethostname()
    myIP = socket.gethostbyname(myHostName)
    server = await asyncio.start_server(configPartie,myIP,9999)
    addr = server.sockets[0].getsockname()
    print(f'Servin on {addr}')
    async with server:
        await server.serve_forever()

if __name__ == '__main__' :
    asyncio.run(servershifumi())
