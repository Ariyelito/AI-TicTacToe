import random
from tkinter import *
from functools import partial
from tkinter import messagebox
from copy import deepcopy
from tkinter.messagebox import askyesno

global grille
grille = [[" " for x in range(3)] for y in range(3)]

button = []
moves = []
v = 0
joueur = 0
ordi = 0
ordiIA = 0
etat = "INIT"


# vérifie les combinaisons gagnantes
def a_gagner(b, l):
    return ((b[0][0] == l and b[0][1] == l and b[0][2] == l) or
            (b[1][0] == l and b[1][1] == l and b[1][2] == l) or
            (b[2][0] == l and b[2][1] == l and b[2][2] == l) or
            (b[0][0] == l and b[1][0] == l and b[2][0] == l) or
            (b[0][1] == l and b[1][1] == l and b[2][1] == l) or
            (b[0][2] == l and b[1][2] == l and b[2][2] == l) or
            (b[0][0] == l and b[1][1] == l and b[2][2] == l) or
            (b[0][2] == l and b[1][1] == l and b[2][0] == l))


def ordi_tour():
    # actions de l'ordi
    global button
    move = get_ordi_choix()
    print('move' + str(move))
    button[move[0]][move[1]].config(state=DISABLED)
    set_choix(move[0], move[1])


# decide qui sera le premier joueur
def qui_commence():
    global joueur
    global etat
    etat = 'JEU'
    if grille.count(' ') == 0:
        test = askyesno(title="Qui commence?", message="Voulez-vous commencer?  [Oui : Humain, Non : Ordi]")
        if test is True:
            joueur = 0
        else:
            joueur = -1
            ordi_tour()

    print(joueur)


def set_choix(i, j):
    global joueur
    global button
    global etat

    if grille[i][j] == ' ':
        if joueur % 2 == 0:
            grille[i][j] = "X"
        else:
            button[i][j].config(state=ACTIVE)
            grille[i][j] = "O"

        joueur += 1
        button[i][j].config(text=grille[i][j])

    # x = True

    if a_gagner(grille, "X"):
        for i in range(len(grille)):
            for j in range(len(grille[i])):
                if grille[i][j] == ' ':
                    button[i][j].config(state=DISABLED)
        # x = False
        etat = 'FIN'
        box = messagebox.showinfo("Gagnant", "Le joueur a gagné")

    elif a_gagner(grille, "O"):
        for i in range(len(grille)):
            for j in range(len(grille[i])):
                if grille[i][j] == ' ':
                    button[i][j].config(state=DISABLED)
        # x = False
        etat = 'FIN'
        box = messagebox.showinfo("Gagnant", "L'ordinateur a gagné")

    elif (partie_egalite()):
        # x = False
        box = messagebox.showinfo("Match nul", "Match nul")
        etat = 'FIN'

    if etat == 'JEU':
        if joueur % 2 != 0:
            ordi_tour()

    if etat == 'FIN':
        box = messagebox.showinfo(";p", "Merci d'avoir joué!")
        # exit()


# reinitialise les variables globales et tableaux
def raz():
    global joueur
    global etat
    etat = 'INIT'
    joueur = 0
    for i in range(len(grille)):
        for j in range(len(grille[i])):
            button[i][j].config(text=" ")
            button[i][j].config(state=ACTIVE)
            grille[i][j] = " "
    qui_commence()


# verifie si la game est fini en egalite
def partie_egalite():
    egalite = True
    for i in grille:
        if (i.count(' ') > 0):
            egalite = False
    return egalite


# actions de l'ordi selon le IA choisi
def get_ordi_choix():
    global ordiIA
    global joueur
    ordiIA = v.get()

    if ordiIA == 1:
        print("heuristique")
        return heuristique()
    elif ordiIA == 2:
        print("hasard")
        return hasard()
    elif ordiIA == 3:
        print("minimax")
        return minimax(False, 2)
    else:
        messagebox.showinfo("", "selectionner une option")


# AI heuristique
def heuristique():
    possiblemove = []
    for i in range(len(grille)):
        for j in range(len(grille[i])):
            if grille[i][j] == ' ':
                possiblemove.append([i, j])
    move = []
    if possiblemove == []:
        return
    else:
        for let in ['O', 'X']:
            for i in possiblemove:
                grillecopy = deepcopy(grille)
                grillecopy[i[0]][i[1]] = let
                if a_gagner(grillecopy, let):
                    return i
        corner = []
        for i in possiblemove:
            if i in [[0, 0], [0, 2], [2, 0], [2, 2]]:
                corner.append(i)
        if len(corner) > 0:
            move = random.randint(0, len(corner) - 1)
            return corner[move]
        edge = []
        for i in possiblemove:
            if i in [[0, 1], [1, 0], [1, 2], [2, 1]]:
                edge.append(i)
        if len(edge) > 0:
            move = random.randint(0, len(edge) - 1)
            return edge[move]


# AI hasard
def hasard():
    lesChoix = []
    choix = random.randint(0, 2)
    choix2 = random.randint(0, 2)
    lesChoix.append(choix)
    lesChoix.append(choix2)

    while not grille[choix][choix2] == ' ':
        lesChoix = []
        choix = random.randint(0, 2)
        choix2 = random.randint(0, 2)
        lesChoix.append(choix)
        lesChoix.append(choix2)
        # print('Hasard : ' + lesChoix)
    return lesChoix


# obtenir mouvements possibles
def get_possible_moves():
    possibleMoves = []
    for i in range(len(grille)):
        for j in range(len(grille[i])):
            if grille[i][j] == ' ':
                possibleMoves.append([i, j])
                print(possibleMoves)
    return possibleMoves


def make_move(move):
    global moves
    if (grille[move[0]][move[1]] == " "):
        moves.append(move[0])
        moves.append(move[1])


def undo():
    global moves
    lastMove = moves.pop()
    if lastMove:
        grille[lastMove[0]][lastMove[1]] = " "


def minimax(isMaxTurn, maximizerMark):
    scores = []
    print(get_possible_moves())
    for move in get_possible_moves():
        make_move(move)
        scores.append(minimax(not isMaxTurn, maximizerMark))

        undo()

    return max(scores) if isMaxTurn else min(scores)


# genère la grille de jeux
def gameboard_pc(game_board):
    print('Creating Buttons...')
    global button
    for i in range(3):
        m = 3 + i
        button.append(i)
        button[i] = []

        for j in range(3):
            n = j
            button[i].append(j)
            get_t = partial(set_choix, i, j)
            button[i][j] = Button(game_board, command=get_t, bd=5, height=5, width=10)
            button[i][j].grid(row=m, column=n)

    global etat
    if (etat == 'INIT'):
        qui_commence()

    game_board.mainloop()


# commence le jeu
def play():
    global ordiIA
    game_board = Tk()
    global v
    v = IntVar()
    v.set(2)  # valeur par default

    game_board.title("Tic Tac Toe")
    l1 = Button(game_board, text="Player : X", width=10)
    l1.grid(row=2, column=0)
    l2 = Button(game_board, text="Computer : O",
                width=10)

    l2.grid(row=2, column=1)
    play_again_button = Button(game_board, text='Nouvelle partie', font=('Arial', 10), command=raz)
    play_again_button.grid(row=2, column=2)

    r1 = Radiobutton(game_board, text="heuristique", variable=v, value=1)
    r2 = Radiobutton(game_board, text="hasard", variable=v, value=2)
    r3 = Radiobutton(game_board, text="minimax", variable=v, value=3)

    r1.grid(row=0, column=0)
    r2.grid(row=0, column=1)
    r3.grid(row=0, column=2)

    print('Will create buttons...')
    gameboard_pc(game_board)


# methode main
if __name__ == '__main__':
    play()
