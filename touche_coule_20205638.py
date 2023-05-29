###############################################################################
# Le programme fourni est une implémentation du jeu Touché-coulé (aussi connu
# sous le nom de Bataille navale) en Python, en utilisant le module Turtle
# pour afficher les grilles de jeu graphiquement et en prenant les entrées des
# joueurs via la console.
###############################################################################
# Auteur: Martin Chaperot (Matricule: 20205638)
# Date: 04 avril 2023
# Email: martin.chaperot@umontreal.ca
###############################################################################


import random
from turtle import *
import math


def arc(r, angle):
    """Cette fonction permet de tracer un arc de cercle

    Args:
        r (int): Rayon de l'arc
        angle (int): Angle de l'arc
    """
    longueur_arc = 2 * math.pi * r * angle / 360
    n = int(longueur_arc / 3) + 1
    longueur_etape = longueur_arc / n
    angle_etape = float(angle) / n
    for _ in range(n):
        fd(longueur_etape)
        lt(angle_etape)


def cercle(r):
    """Cette fonction permet de dessiner un cercle

    Args:
        r (int): Longueur du rayon
    """
    arc(r, 360)


def carre(cote):
    """Cette fonction permet de dessiner un carré

    Args:
        cote (int): Longueur d'un coté
    """
    for _ in range(4):
        fd(cote)
        lt(90)


def positionner(x, y):
    """Cette fonction permet de positionner la tortue relativement à son 
    emplacement actuel

    Args:
        x (int): Nombre de pas en x
        y (int): Nombre de pas en y
    """
    pu()
    fd(x)
    lt(90)
    fd(y)
    rt(90)
    pd()


def grille(cols, lignes, taille, espace):
    """Cette fonction permet de tracer une grille.

    Args:
        cols (int): Nombre de colonnes
        lignes (int): Nombre de lignes
        taille (int): Taille d'une case
        espace (int): Taille de l'espace entre chaque case
    """
    for x in range(cols):
        for y in range(lignes):
            positionner(x * (taille + espace), y * (taille + espace))
            carre(taille)
            positionner(-x * (taille + espace), -y * (taille + espace))


# Fonction principale du programme
def initialise_grille():
    # g[0] = grille du joueur 1, g[1] = grille du joueur 2
    # Chaque grille est un entier dont les bits de poids faible représentent
    # les cases de la grille. Par exemple, la case 0 est représentée par le
    # bit de poids faible, la case 1 par le bit de poids 2, etc.
    g = [0, 0]
    bateaux1 = []
    bateaux2 = []

    # Generation des positions aléatoires des bateaux
    while len(bateaux1) < 5:
        if (b := random.randint(0, 35)) not in bateaux1:
            bateaux1.append(b)
    while len(bateaux2) < 5:
        if (b := random.randint(0, 35)) not in bateaux2:
            bateaux2.append(b)

    # Stockage des positions des bateaux dans la grille
    for i in range(5):
        g[0] += 2 ** bateaux1[i]
        g[1] += 2 ** bateaux2[i]

    return g


def case_ratee(j, case):
    """Cette fonction permet de dessiner une case ratée

    Args:
        j (int): Le numéro du joueur
        case (int): Case à dessiner
    """
    diag = math.sqrt(2 * 16 ** 2)
    if j == 0:
        positionner(-36-120, 0)

    positionner(case % 6 * 20, 100 - (case // 6 * 20))

    width(2)
    color(0, 1, 0)
    carre(16)
    width(1)
    lt(45)
    fd(diag)
    lt(45+90)
    fd(16)
    lt(90+45)
    fd(diag)
    rt(45+90)
    fd(16)
    rt(180)
    color(0, 0, 0)

    positionner(-(case % 6 * 20), -100 + (case // 6 * 20))

    if j == 0:
        positionner(120+36, 0)


def case_touchee(j, case):
    """Cette fonction permet de dessiner une case touchée

    Args:
        j (int): Le numéro du joueur
        case (int): Case à dessiner
    """
    if j == 0:
        positionner(-36-120, 0)

    positionner(case % 6 * 20, 100 - (case // 6 * 20))

    color(1, 1, 1)
    carre(16)
    color(1, 0, 0)
    width(4)
    positionner(8, 0)
    cercle(8)
    positionner(-8, 0)
    width(1)
    color(0, 0, 0)

    positionner(-(case % 6 * 20), -100 + (case // 6 * 20))

    if j == 0:
        positionner(120+36, 0)


def jouer():
    wn = Screen()
    wn.tracer(0)
    speed(0)

    g = initialise_grille()
    # Grille 1
    grille(6, 6, 16, 4)
    # Line blue vertical
    positionner(120+16, 120+50)
    rt(90)
    color(0, 0, 1)
    width(10)
    fd(120+100)
    color(0, 0, 0)
    width(1)
    lt(90)
    positionner(20, 50)
    # Grille 2
    grille(6, 6, 16, 4)
    wn.update()

    lettre = "ABCDEF"
    print("TOUCHÉ-COULÉ")
    t = 0  # compteur de tours
    while g[0] != 0 and g[1] != 0:
        c = input(f"Joueur {t % 2 + 1}: ")
        if c[0] not in lettre or not c[1].isdigit() or int(c[1]) > 6:
            print("Erreur de saisie")
            continue

        case = lettre.index(c[0]) + ((int(c[1]) - 1) * 6)

        if g[t % 2] & (1 << case):
            print("Touché")
            g[t % 2] -= 1 << case
            case_touchee(t % 2, case)
        else:
            print("Raté")
            case_ratee(t % 2, case)

        wn.update()
        t += 1

    print(f"JOUEUR {(t-1) % 2 + 1} a gagné !")


jouer()
