import random
from tkinter import *
from functools import partial
from tkinter import messagebox
from copy import deepcopy
from tkinter.messagebox import askyesno

global grille
grille = [[" " for x in range(3)] for y in range(3)]

v = 0
joueur = 0
ordi = 0
ordiIA = 0
moves = []
global ayt 
global essaie


def a_gagner(b, l):
    return ((b[0][0] == l and b[0][1] == l and b[0][2] == l) or
            (b[1][0] == l and b[1][1] == l and b[1][2] == l) or
            (b[2][0] == l and b[2][1] == l and b[2][2] == l) or
            (b[0][0] == l and b[1][0] == l and b[2][0] == l) or
            (b[0][1] == l and b[1][1] == l and b[2][1] == l) or
            (b[0][2] == l and b[1][2] == l and b[2][2] == l) or
            (b[0][0] == l and b[1][1] == l and b[2][2] == l) or
            (b[0][2] == l and b[1][1] == l and b[2][0] == l))


def whoStarts():
    global joueur
    if (grille.count(' ') == 0):
        test = askyesno(title="qui commence", message="Voulez-vous commencer ?")
        if test is True:
            joueur = 0
        else:
            joueur = -1
        print(joueur)


def set_choix(i, j, gb, l1, l2):
    global joueur

    if grille[i][j] == ' ':
        if joueur % 2 == 0:
            l1.config(state=DISABLED)
            l2.config(state=ACTIVE)
            grille[i][j] = "X"
        else:
            button[i][j].config(state=ACTIVE)
            l2.config(state=DISABLED)
            l1.config(state=ACTIVE)
            grille[i][j] = "O"

        joueur += 1
        button[i][j].config(text=grille[i][j])

    x = True

    if a_gagner(grille, "X"):
        for i in range(len(grille)):
            for j in range(len(grille[i])):
                if grille[i][j] == ' ':
                    button[i][j].config(state=DISABLED)
        x = False
        box = messagebox.showinfo("Winner", "Player won the match")

    elif a_gagner(grille, "O"):
        for i in range(len(grille)):
            for j in range(len(grille[i])):
                if grille[i][j] == ' ':
                    button[i][j].config(state=DISABLED)
        x = False
        box = messagebox.showinfo("Winner", "Computer won the match")

    elif (choix_valide()):
        x = False
        box = messagebox.showinfo("Tie Game", "Tie Game")

    if (x):
        if joueur % 2 != 0:
            move = get_ordi_choix()
            print(move)
            button[move[0]][move[1]].config(state=DISABLED)
            set_choix(move[0], move[1], gb, l1, l2)


def event_reset():
    for i in range(len(grille)):
        for j in range(len(grille[i])):
            button[i][j].config(text=" ")
            button[i][j].config(state=ACTIVE)
            grille[i][j] = " "
    whoStarts()


def choix_valide():
    flag = True
    for i in grille:
        if (i.count(' ') > 0):
            flag = False
    return flag


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


def hasard():
    lesChoix = []
    choix = 0
    choix2 = 0

    while not grille[choix][choix2] == ' ':
        choix = random.randint(0, 2)
        choix2 = random.randint(0, 2)
        lesChoix.append(choix)
        lesChoix.append(choix2)
        return lesChoix


def get_possible_moves():
    possibleMoves = []
    for x in range(0, 3):
        for y in range(0, 3):
            if grille[x][y] == " ":
                possibleMoves.append((x, y))
    return possibleMoves


def make_move(coordinates):
    global moves
    x = coordinates[0]
    y = coordinates[1]

    if (grille[x][y] == " "):
        moves.append(coordinates)


def minimax(isMaxTurn, maximizerMark):
    global moves
    scores = []

    for move in get_possible_moves():
        make_move(move)
        scores.append(minimax(not isMaxTurn, maximizerMark))
        lastMove = moves.pop()
        if lastMove:
            grille[lastMove[0]][lastMove[1]] = " "
        if (isMaxTurn and max(scores) == 1) or (not isMaxTurn and min(scores) == -1):
            break
    return max(scores) if isMaxTurn else min(scores)


def gameboard_pc(game_board, l1, l2):
    global button
    global reponse
    button = []

    for i in range(3):
        m = 3 + i
        button.append(i)
        button[i] = []

        for j in range(3):
            n = j
            button[i].append(j)
            get_t = partial(set_choix, i, j, game_board, l1, l2)
            button[i][j] = Button(game_board, command=get_t, bd=5, height=5, width=10)
            button[i][j].grid(row=m, column=n)

    game_board.mainloop()


def play():
    global ordiIA
    game_board = Tk()

    game_board.title("Tic Tac Toe")
    l1 = Button(game_board, text="Player : X", width=10)
    l1.grid(row=2, column=0)
    l2 = Button(game_board, text="Computer : O",
                width=10, state=DISABLED)

    l2.grid(row=2, column=1)
    play_again_button = Button(game_board, text='Nouvelle partie', font=('Arial', 10), command=event_reset)
    play_again_button.grid(row=2, column=2)

    global v
    v = IntVar()
    v.set(2)  # valeur par default

    r1 = Radiobutton(game_board, text="heuristoque", variable=v, value=1)
    r2 = Radiobutton(game_board, text="hasard", variable=v, value=2)
    r3 = Radiobutton(game_board, text="minimax", variable=v, value=3)

    r1.grid(row=0, column=0)
    r2.grid(row=0, column=1)
    r3.grid(row=0, column=2)

    whoStarts()
    gameboard_pc(game_board, l1, l2)


# Call main function
if __name__ == '__main__':
    play()
