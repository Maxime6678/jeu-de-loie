from tkinter import Tk, Label, IntVar, Radiobutton, PhotoImage, Canvas, Button, CENTER, NW
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk
import sys
from random import randint
import time
from pygame import mixer

""" Position des cases """
casex = [44,124,207,290,373,456,540,621,703,789,789,789,709,621,540,456,377,294,207,130,43,43,43,125,202,291,371,454,538,618,704,787,787,787,705,622,541,459,376,294,211,125,43,43,43,126,207,291,370,456,539,617,705,788] 
""" coordonées en x des cases"""
casey = [560,560,560,560,560,560,560,560,560,560,494,425,425,425,425,425,425,425,425,425,425,362,293,293,293,293,293,293,293,293,293,293,232,162,162,162,162,162,162,162,162,162,162,97,30,30,30,30,30,30,30,30,30,30] 
"""coordonées en y des cases"""

""" Position des echelles """
echellex = [540,207,703,621]
echelley = [494,359,227,96]

""" Multiplayer variable """
playerCount = 0
currentPlayer = 0
lastPlayer = 0
playersPos = [0, 0, 0, 0]
playerCanevas = [[0, 0], [0, 0], [0, 0], [0, 0]]
colorPion = ['yellow', 'red', 'blue', 'black']
deCanevas = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
labelPlayer = [0, 0, 0, 0]
pastNext = [0, 0, 0, 0]
playWithComputer = 0

""" Musique """
mixer.init()  # initialisation 
mixer.music.load('music/craberave.mp3')
mixer.music.play(-1) # jouer la musique en boucle 

""" Start window """

lw = Tk()
lw.title('Chasles Game')
lw.geometry('600x310')
lw.resizable(0, 0)
lw.protocol("WM_DELETE_WINDOW", sys.exit)

lw.rowconfigure(1, pad=10) # Ajoute un padding de 10px

img_Welcome = ImageTk.PhotoImage(
    Image.open('images/bienvenue.jpg').resize((600, 100)))
lab_welcome = Label(lw, image=img_Welcome)
lab_welcome.grid(row=0, column=0, columnspan=3)

lab_playerCount = Label(lw, text='Selection des joueurs:')
lab_playerCount.grid(row=1, column=1)

var_playerCount = IntVar()
var_playerCount.set(1)
Radiobutton(lw, text='1 joueur avec 1 ordinateur',
            variable=var_playerCount, value=1).grid(row=2, column=1)
Radiobutton(lw, text='2 joueurs', variable=var_playerCount,
            value=2).grid(row=3, column=1)
Radiobutton(lw, text='3 joueurs', variable=var_playerCount,
            value=3).grid(row=4, column=1)
Radiobutton(lw, text='4 joueurs', variable=var_playerCount,
            value=4).grid(row=5, column=1)
 
def launchGame(): # Lance la partie
    global playerCount, playWithComputer

    lw.destroy()
    playerCount = var_playerCount.get()
    if playerCount == 1: # Si on joue avec l'ordinateur
        playWithComputer = 1
        playerCount += 1

btn_launch = Button(lw, text='Lancer la partie', command=launchGame)
btn_launch.grid(row=6, column=0)

btn_quit = Button(lw, text='Quitter la partie', command=sys.exit)
btn_quit.grid(row=6, column=2)

lw.mainloop()

""" Game window """

gw = Tk()
gw.title('Chasles Game')
gw.geometry('855x700')
gw.resizable(0, 0)
gw.protocol("WM_DELETE_WINDOW", sys.exit)
 
back = PhotoImage(file='images/board.gif')

canevas = Canvas(gw, width=855, height=600)
canevas.create_image(0, 0, anchor=NW, image=back)
for i in range(0, playerCount): # Crée l'image des pions pour tout les joueurs
    playerCanevas[i][0] = PhotoImage(file='images/pion_' + colorPion[i] + '.png')
    playerCanevas[i][1] = canevas.create_image(casex[0] + i * 5, casey[0] + i * 5, anchor=CENTER, image=playerCanevas[i][0])
for i in range(0, 6): # Crée l'image des 6 faces du dé
    url = 'images/D' + str(i + 1) + '.png'
    deCanevas[i] = [0, 0]
    deCanevas[i][0] = ImageTk.PhotoImage(
        Image.open(url).resize((64, 64)))
    deCanevas[i][1] = canevas.create_image(-100, -100, anchor=CENTER, image=deCanevas[i][0])
canevas.grid(row=0, column=0, columnspan=3)

"""fonction qui fait bouger les pions quand ils tombent sur une echelle """
def moveEchelle(player): 
    global playersPos, canevas
    echellePos = 0
 
    """case départ echelle 1"""
    if playersPos[player] == 14:
        echellePos = 0
        playersPos[player] = 6 
        """case arrivée echelle 1"""
    elif playersPos[player] == 18:
        echellePos = 1
        playersPos[player] = 24
    elif playersPos[player] == 30:
        echellePos = 2
        playersPos[player] = 34
    elif playersPos[player] == 51:
        echellePos = 3
        playersPos[player] = 35
    """ on déplace le pion aux coordonées echellex et echelley """
    canevas.coords(playerCanevas[player][1], echellex[echellePos], echelley[echellePos]) 
    """met a jour le canevas"""
    canevas.update()
    """delais"""
    time.sleep(0.3)
    """on déplace le joueur aux coordonées de la case arrivée de l'echelle"""
    canevas.coords(playerCanevas[player][1], casex[playersPos[player]], casey[playersPos[player]])
    canevas.update()


def launchDe():
    global currentPlayer, deCanevas, labelPlayer, lastPlayer
    """ désactive le bouton dé apres avoir appuyé dessus"""
    btn.config(state='disabled')
 
    """Ne peux pas relancer le dé"""
    canRelaunch = 0
    """chiffre aléatoire entre 1 et 6"""
    rand = randint(1, 6)
 
    """ Animation """
    """ fait apparaitre deux fois les faces du dé de 1 à 6"""
    for i in range(0, 2):
        """Met l'image du dé 1 dans le canevas"""
        canevas.coords(deCanevas[0][1], 428, 300)
        canevas.update()
        time.sleep(0.04)
        """Remet l'image du dé 1 hors du canevas"""
        canevas.coords(deCanevas[0][1], -100, -100)
        """Met l'image du dé 2 dans le canevas"""
        canevas.coords(deCanevas[1][1], 428, 300)
        canevas.update()
        time.sleep(0.04)
        canevas.coords(deCanevas[1][1], -100, -100)
        canevas.coords(deCanevas[2][1], 428, 300)
        canevas.update()
        time.sleep(0.04)
        canevas.coords(deCanevas[2][1], -100, -100)
        canevas.coords(deCanevas[3][1], 428, 300)
        canevas.update()
        time.sleep(0.04)
        canevas.coords(deCanevas[3][1], -100, -100)
        canevas.coords(deCanevas[4][1], 428, 300)
        canevas.update()
        time.sleep(0.04)
        canevas.coords(deCanevas[4][1], -100, -100)
        canevas.coords(deCanevas[5][1], 428, 300)
        canevas.update()
        time.sleep(0.04)
        canevas.coords(deCanevas[5][1], -100, -100)
        canevas.update()
    
    """affiche le dé que l'on a tiré"""
    canevas.coords(deCanevas[rand - 1][1], 428, 300)
    canevas.update()
    time.sleep(0.3)
    """enleve du canevas le dé que l'on a tiré"""
    canevas.coords(deCanevas[rand - 1][1], -100, -100)
    canevas.update()

    if playersPos[currentPlayer] + rand > 53:
        memo = 53 - playersPos[currentPlayer]
        movePlayer(currentPlayer, memo)
        movePlayer(currentPlayer, memo - rand)
    else:
        movePlayer(currentPlayer, rand)

    if playersPos[currentPlayer] == 1:
        if currentPlayer == 1 and playWithComputer:
            showinfo(title="Notification", message="L'ordinateur avance jusqu'à la prochaine case rouge")
        else:
            """afficher un message"""
            showinfo(title="Notification", message="Vous avancez jusqu'à la prochaine case rouge")
        """Si le joueur actuel est sur la case 1alors il avance de 8 cases"""
        movePlayer(currentPlayer, 8)
    elif playersPos[currentPlayer] == 2 or playersPos[currentPlayer] == 7 or playersPos[currentPlayer] == 13 or playersPos[currentPlayer] == 25 or playersPos[currentPlayer] == 36 or playersPos[currentPlayer] == 43 or playersPos[currentPlayer] == 47:
        showinfo(title="Notification", message="Carte Chance") # pop-up " carte chance"
        Chance = randint(0, 9) # tirage aléatoire de la carte chance
 
        if Chance == 0:
            if currentPlayer == 1 and playWithComputer: # S'il s'agit de l'ordinateur 
                showinfo(title="carte chance", message="L'ordinateur fait reculer ses adversaires de 3 cases") # pop-up 
            else:
                showinfo(title="carte chance", message="Vous faites reculer vos adversaires de 3 cases") # pop-up
            for i in range(0, playerCount):
                if i != currentPlayer:
                    movePlayer(i, -3)
        elif Chance == 1:
            if currentPlayer == 1 and playWithComputer:
                showinfo(title="carte chance", message="M RADONDE vient de dire que l'ordinateur est une MACHINE! Il peut avancer de 3 cases supplémentaires")
            else:
                showinfo(title="carte chance", message="M RADONDE vient de dire que vous êtes une MACHINE! Vous pouvez avancer de 3 cases supplémentaires")
            movePlayer(currentPlayer, 3)
        elif Chance == 2:
            if currentPlayer == 1 and playWithComputer:
                showinfo(title="carte chance", message="MME DELBREIL trouve l'ordinateur très futé, elle lui offre un jet de dé supplémentaire")
            else:
                showinfo(title="carte chance", message="MME DELBREIL vous trouve très futé, elle vous offre un jet de dé supplémentaire")
            canRelaunch = 1 # relancer le dé
        elif Chance == 3:
            if currentPlayer == 1 and playWithComputer:
                showinfo(title="carte chance", message="M LOPEZ oblige l'ordinateur à faire 10 pompes, il doit passer son prochain tour")
            else:
                showinfo(title="carte chance", message="M LOPEZ vous oblige à faire 10 pompes, vous devez passer votre prochain tour")
            pastNext[currentPlayer] = 1 # passer le tour 
        elif Chance == 4:
            if currentPlayer == 1 and playWithComputer:
                showinfo(title="carte chance", message="M IGLESIAS oblige l'ordinateur à faire 2 tours de terrain, il doit passer son prochain tour")
            else:
                showinfo(title="carte chance", message="M IGLESIAS vous oblige à faire 2 tours de terrain, vous devez passer votre prochain tour")
            pastNext[currentPlayer] = 1
        elif Chance == 5:
            if currentPlayer == 1 and playWithComputer:
                showinfo(title="carte chance", message="M COSTA reprend l'ordinateur à l’ordre, il doit reculer d’une case")
            else:
                showinfo(title="carte chance", message="M COSTA vous reprend à l’ordre, vous devez reculer d’une case")
            movePlayer(currentPlayer, -1)
        elif Chance == 6:
            if currentPlayer == 1 and playWithComputer:
                showinfo(title="carte chance", message="Un dé tombe du ciel, Quelle chance! L'ordinateur à un jeu de dé supplémentaire")
            else:
                showinfo(title="carte chance", message="Un dé tombe du ciel, Quelle chance! Vous avez un jeu de dé supplémentaire")
            canRelaunch = 1
        elif Chance == 7:
            if currentPlayer == 1 and playWithComputer:
                showinfo(title="carte chance", message="L'ordinateur vient de déclencher un tremblement de terre… Chaque joueur recule d’une case, les effets des cases sont neutralisés pour tous les joueurs pour ce tour")
            else:
                showinfo(title="carte chance", message="Vous venez de déclencher un tremblement de terre… Chaque joueur recule d’une case, les effets des cases sont neutralisés pour tous les joueurs pour ce tour")
            for i in range(0, playerCount):
                if i != currentPlayer:
                    movePlayer(i, -1)
        elif Chance == 8:
            if currentPlayer == 1 and playWithComputer:
                showinfo(title="carte chance", message="MME PEREZ a un oeil de lynx, elle a chopé l'ordinateur avec son téléphone. Il va à la case colle")
            else:
                showinfo(title="carte chance", message="MME PEREZ a un oeil de lynx, elle vous a chopé avec votre téléphone. Vous allez à la case colle")
            movePlayer(currentPlayer, ( 11 - playersPos[currentPlayer])) # allez a la case colle
        elif Chance == 9:
            if currentPlayer == 1 and playWithComputer:
                showinfo(title="carte chance", message="L'ordinateur avance de 3 cases")
            else:
                showinfo(title="carte chance", message="Vous avancez de 3 cases")
            movePlayer(currentPlayer, 3)
    elif playersPos[currentPlayer] == 4 or playersPos[currentPlayer] == 10 or playersPos[currentPlayer] == 20 or playersPos[currentPlayer] == 27 or playersPos[currentPlayer] == 31 or playersPos[currentPlayer] == 37 or playersPos[currentPlayer] == 40 or playersPos[currentPlayer] == 45:
        if currentPlayer == 1 and playWithComputer:
            showinfo(title="Notification", message="Le dé de l'ordinateur est doublé")
        else:
            showinfo(title="Notification", message="Votre dé est doublé")
        movePlayer(currentPlayer, rand)
    elif playersPos[currentPlayer] == 8:
        if currentPlayer == 1 and playWithComputer:
            showinfo(title="Notification", message="L'ordinateur recule jusqu'à la dernière case noire")
        else:
            showinfo(title="Notification", message="Vous reculez jusqu'à la dernière case noire")
        movePlayer(currentPlayer, -3)
    elif playersPos[currentPlayer] == 9:
        if currentPlayer == 1 and playWithComputer:
            showinfo(title="Notification", message="L'ordinateur avance jusqu'à la prochaine case rouge")
        else:
            showinfo(title="Notification", message="Vous avancez jusqu'à la prochaine case rouge")
        movePlayer(currentPlayer, 6)
    elif playersPos[currentPlayer] == 14:
        if currentPlayer == 1 and playWithComputer:
            showinfo(title="Notification", message="L'ordinateur descend l'échelle")
        else:  
            showinfo(title="Notification", message="Vous descendez à l'échelle")
        moveEchelle(currentPlayer)
    elif playersPos[currentPlayer] == 15:
        if currentPlayer == 1 and playWithComputer:
            showinfo(title="Notification", message="L'ordinateur avance jusqu'à la prochaine case rouge")
        else:
            showinfo(title="Notification", message="Vous avancez jusqu'à la prochaine case rouge")
        movePlayer(currentPlayer, 4)
    elif playersPos[currentPlayer] == 17:
        if currentPlayer == 1 and playWithComputer:
            showinfo(title="Notification", message="L'ordinateur recule jusqu'à la dernière case noire")
        else:
            showinfo(title="Notification", message="Vous reculez jusqu'à la dernière case noire")
        movePlayer(currentPlayer, -9)
    elif playersPos[currentPlayer] == 18:
        if currentPlayer == 1 and playWithComputer:
            showinfo(title="Notification", message="L'ordinateur monte à l'échelle")
        else:  
            showinfo(title="Notification", message="Vous montez à l'échelle")
        moveEchelle(currentPlayer)
    elif playersPos[currentPlayer] == 19:
        if currentPlayer == 1 and playWithComputer:
            showinfo(title="Notification", message="L'ordinateur avance jusqu'à la prochaine case rouge")
        else:
            showinfo(title="Notification", message="Vous avancez jusqu'à la prochaine case rouge")
        movePlayer(currentPlayer, 7)
    elif playersPos[currentPlayer] == 22:
        if currentPlayer == 1 and playWithComputer:
            showinfo(title="Notification", message="L'ordinateur recule jusqu'à la dernière case noire")
        else:
            showinfo(title="Notification", message="Vous reculez jusqu'à la dernière case noire")
        movePlayer(currentPlayer, -5)
    elif playersPos[currentPlayer] == 26:
        if currentPlayer == 1 and playWithComputer:
            showinfo(title="Notification", message="L'ordinateur avance jusqu'à la prochaine case rouge")
        else:
            showinfo(title="Notification", message="Vous avancez jusqu'à la prochaine case rouge")
        movePlayer(currentPlayer, 9)
    elif playersPos[currentPlayer] == 29:
        if currentPlayer == 1 and playWithComputer:
            showinfo(title="Notification", message="L'ordinateur recule jusqu'à la dernière case noire")
        else:
            showinfo(title="Notification", message="Vous reculez jusqu'à la dernière case noire")
        movePlayer(currentPlayer, -7)
    elif playersPos[currentPlayer] == 30:
        if currentPlayer == 1 and playWithComputer:
            showinfo(title="Notification", message="L'ordinateur monte à l'échelle")
        else:  
            showinfo(title="Notification", message="Vous montez à l'échelle")
        moveEchelle(currentPlayer)
    elif playersPos[currentPlayer] == 35:
        if currentPlayer == 1 and playWithComputer:
            showinfo(title="Notification", message="L'ordinateur avance jusqu'à la prochaine case rouge")
        else:
            showinfo(title="Notification", message="Vous avancez jusqu'à la prochaine case rouge")
        movePlayer(currentPlayer, 11)
    elif playersPos[currentPlayer] == 41:
        if currentPlayer == 1 and playWithComputer:
            showinfo(title="Notification", message="L'ordinateur recule jusqu'à la dernière case noire")
        else:
            showinfo(title="Notification", message="Vous reculez jusqu'à la dernière case noire")
        movePlayer(currentPlayer, -12)
    elif playersPos[currentPlayer] == 46:
        if currentPlayer == 1 and playWithComputer:
            showinfo(title="Notification", message="L'ordinateur avance jusqu'à la prochaine case rouge")
        else:
            showinfo(title="Notification", message="Vous avancez jusqu'à la prochaine case rouge")
        movePlayer(currentPlayer, 2)
    elif playersPos[currentPlayer] == 49:
        if currentPlayer == 1 and playWithComputer:
            showinfo(title="Notification", message="L'ordinateur recule jusqu'à la dernière case noire")
        else:
            showinfo(title="Notification", message="Vous reculez jusqu'à la dernière case noire")
        movePlayer(currentPlayer, -8)
    elif playersPos[currentPlayer] == 51:
        if currentPlayer == 1 and playWithComputer:
            showinfo(title="Notification", message="L'ordinateur descend l'échelle")
        else:  
            showinfo(title="Notification", message="Vous descendez à l'échelle")
        moveEchelle(currentPlayer)
    elif playersPos[currentPlayer] == 53:
        gw.destroy()
        return

    for i in range (0, playerCount):
        """Vérifie pour chaque joueur si il est sur la même case qu'un autre"""
        for j in range(0, playerCount):
            """ si le joueur j et le joueur j sont différents et que leur position sont identique, alors :"""
            if i != j and playersPos[i] == playersPos[j]:
                """On déplace le joueur j de 5pixels en x et en y multiplié par son numéro de joueur auquel on soustrait 1"""
                canevas.coords(playerCanevas[j][1], casex[playersPos[j]] + j * 5, casey[playersPos[j]] + j * 5)
                canevas.update()

    if not canRelaunch : # Permet de changer le joueur si on relance pas le dé
        lastPlayer = currentPlayer
        currentPlayer += 1
        if currentPlayer > playerCount - 1: # Passe du joueur max a 0
            currentPlayer = 0
        if pastNext[currentPlayer]: # Saute le tour
            pastNext[currentPlayer] = 0
            currentPlayer += 1

    labelPlayer[lastPlayer].config(font='Helvetica 9 normal', fg=colorPion[lastPlayer]) # Change le gras sur les labels
    labelPlayer[currentPlayer].config(font='Helvetica 11 bold', fg=colorPion[currentPlayer])

    if currentPlayer == 1 and playWithComputer: # Gestion ordinateur
        time.sleep(0.3)
        launchDe()

    btn.config(state='normal')


def movePlayer(player, deplacement): # définition de la fonction movePlayer
    global playersPos, canevas # on importe des variables qui sont en dehors de movePlayer
 
    for _i in range(0, abs(deplacement)): # boucle for pour l’avancement d’un joueur
        time.sleep(0.09)
        if deplacement > 0:
            playersPos[player] = playersPos[player] + 1
        elif deplacement < 0:
            playersPos[player] = playersPos[player] - 1
        if (playersPos[player] < 0): playersPos[player] = 0
        canevas.coords(playerCanevas[player][1], casex[playersPos[player]], casey[playersPos[player]]) # modifier les coordonnées du pion 
        canevas.update()


"""Bouton lancer le dé"""
btn = Button(gw, text="Lancer le dé", command=launchDe)
"""Le place à la premiere ligne et premiere colone d'un tableau invisible divisant la fenetre"""
btn.grid(row=1, column=1)

for i in range(0, playerCount):
    if i == 1 and playWithComputer:
        playerStr = "Ordinateur"
    else:
        playerStr = "Joueur " + str(i + 1)
    font = 'Helvetica 9 normal'
    labelPlayer[i] = Label(gw, text=playerStr, font=font, fg=colorPion[i])
    if i == 0:
        font = 'Helvetica 11 bold'
        labelPlayer[i].config(font=font)
    if i < 2:
        labelPlayer[i].grid(row=i+1, column=0)
    else:
        labelPlayer[i].grid(row=i-1, column=2)

gw.mainloop()

""" Finish window """
fw = Tk()
fw.title('Chasles Game')
fw.geometry('600x300')
fw.resizable(0, 0)
fw.protocol("WM_DELETE_WINDOW", sys.exit)

fw.rowconfigure(1, pad=24)

img_Finish = ImageTk.PhotoImage(
    Image.open('images/over.png').resize((600, 200)))

lab_finish = Label(fw, image=img_Finish)
lab_finish.grid(row=0, column=0, columnspan=3)

labText = ''
if currentPlayer == 1 and playWithComputer:
    labText = 'Perdu ! L\'ordinateur a gagné !'
elif playWithComputer:
    labText = 'Bravo, tu as gagné contre l\'ordinateur !'
else:
    labText = 'Bravo Joueur ' + str(currentPlayer + 1) + ' ! Tu as gagné la partie !'

lab_playerWin = Label(fw, text=labText)
lab_playerWin.grid(row=1, column=1)

btn_quit = Button(fw, text='Quitter la partie', command=sys.exit)
btn_quit.grid(row=2, column=2)

fw.mainloop()