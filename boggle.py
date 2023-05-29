# Martin Chaperot (20205638) et Olivier Simard (20262563)
# Testé avec python 3.10.10
from math import floor
from random import choice


def generer_grille(taille: int) -> list[list[str]] | None:
    quatre = [
        ["E", "T", "U", "K", "N", "O"],
        ["E", "V", "G", "T", "I", "N"],
        ["D", "E", "C", "A", "M", "P"],
        ["I", "E", "L", "R", "U", "W"],
        ["E", "H", "I", "F", "S", "E"],
        ["R", "E", "C", "A", "L", "S"],
        ["E", "N", "T", "D", "O", "S"],
        ["O", "F", "X", "R", "I", "A"],
        ["N", "A", "V", "E", "D", "Z"],
        ["E", "I", "O", "A", "T", "A"],
        ["G", "L", "E", "N", "Y", "U"],
        ["B", "M", "A", "Q", "J", "O"],
        ["T", "L", "I", "B", "R", "A"],
        ["S", "P", "U", "L", "T", "E"],
        ["A", "I", "M", "S", "O", "R"],
        ["E", "N", "H", "R", "I", "S"]
    ]
    cinq = [
        ["A", "T", "S", "I", "O", "U"],
        ["W", "I", "R", "E", "B", "C"],
        ["Q", "D", "A", "H", "A", "U"],
        ["A", "C", "F", "L", "N", "E"],
        ["P", "R", "S", "T", "U", "G"],
        ["J", "P", "R", "X", "E", "Z"],
        ["E", "K", "V", "Y", "B", "E"],
        ["A", "L", "C", "H", "E", "M"],
        ["E", "D", "U", "F", "H", "K"],
    ]
    if taille not in (4, 5):
        return None

    grille: list[list[str]] = []
    utiliser = [i for i in range(taille * taille)]
    for _ in range(taille):
        temp = []
        for _ in range(taille):
            de = choice(utiliser)
            utiliser.remove(de)
            if de < 16:
                choix = choice(quatre[de])
            else:
                choix = choice(cinq[de - 16])
            temp.append(choix)
        grille.append(temp)

    return grille


def est_valide(grille: list[list[str]], mot: str) -> bool:
    if len(mot) < 3:
        return False

    def cherche_mot(x: int, y: int, mot: str, direction: tuple[int, int]) -> bool:
        """
        Trouve un mot dans une direction étant donné la position
        initiale (x, y) et la direction.
        """
        while 0 <= x < len(grille[0]) and 0 <= y < len(grille):
            if mot == "":
                return True
            elif grille[y][x] == mot[0]:
                mot = mot[1:]
                x += direction[0]
                y += direction[1]
            else:
                return False
        return mot == ""

    resultat = False
    for i in range(len(grille)):
        for j in range(len(grille[i])):
            if grille[i][j] == mot[0]:
                resultat |= cherche_mot(j, i, mot, (1, 0)) or \
                    cherche_mot(j, i, mot, (0, 1)) or \
                    cherche_mot(j, i, mot, (-1, 0)) or \
                    cherche_mot(j, i, mot, (0, -1))
    return resultat


def calcul_point(mots: list[str]) -> int:
    """
    J'assume que tout les mots sont validés avant et que la liste mots contient
    seulement les mots legals et non rejeté.

    Donc le parametre "grille" n'est pas necessaire.
    """
    total_point = 0
    for mot in mots:
        if len(mot) == 3:
            total_point += 1
        elif len(mot) == 4:
            total_point += 2
    return total_point


def jouer():
    while True:
        taille = 0
        while True:
            taille = input("Taille de la grille ? [4 ou 5] ")
            try:
                taille = int(taille)
            except ValueError:
                print("La taille donné n'est pas un nombre valide")
                continue
            if taille in (4, 5):
                break
            else:
                print("La taille donné n'est pas 4 ou 5")

        j1 = input("Nom du joueur 1? ")
        j2 = input("Nom du joueur 2? ")

        grille = generer_grille(taille)
        if grille is None:
            # ne peux jamais arriver normalement car valide la taille avant
            return
        for i in range(taille):
            print("-"*((4*taille)+1))
            print("|", end="")
            for j in range(taille):
                print(f" {grille[i][j]} |", end="")
            print("")
        print("-"*((4*taille)+1))

        # mots = [[mot, legal?, accepté?],...]
        mots = []
        finie = False
        for i in range(20):
            mot = input(f"{j2 if i%2 else j1} mot {floor(i/2)+1}: ")
            mot = mot.upper()
            if mot == "":
                if finie:
                    break
                finie = True
                continue
            else:
                finie = False
            accepte = True
            if not (valide := est_valide(grille, mot)):
                print("Mot illégal")
            else:
                rejete_q = input(f"{j1 if i%2 else j2} rejete le mot ? [o/N] ")
                if rejete_q.strip() in ("o", "O"):
                    accepte = False
            mots.append([mot, valide, accepte])

        j1_mots = [m for m in mots if mots.index(m) % 2 == 0]
        j1_point = calcul_point([m[0] for m in j1_mots if all(m[1:])])
        j2_mots = [m for m in mots if mots.index(m) % 2 == 1]
        j2_point = calcul_point([m[0] for m in j2_mots if all(m[1:])])

        print("")
        print(j1)
        print("-"*40)
        for mot in j1_mots:
            print(f"- {mot[0]}", end="\t\t")
            if not all([mot[1], mot[2]]):
                print("(x) --", end=" ")
                if not mot[1]:
                    print("ILLEGAL")
                else:
                    print("REJECTE")
            else:
                if len(mot[0]) == 3:
                    print("(1)")
                elif len(mot[0]) == 4:
                    print("(2)")
        print("="*40)
        print(f"Total: {j1_point}")

        print("")
        print(j2)
        print("-"*40)
        for mot in j2_mots:
            print(f"- {mot[0]}", end="\t\t")
            if not all([mot[1], mot[2]]):
                print("(x) --", end=" ")
                if not mot[1]:
                    print("ILLEGAL")
                else:
                    print("REJECTE")
            else:
                if len(mot[0]) == 3:
                    print("(1)")
                elif len(mot[0]) == 4:
                    print("(2)")
        print("="*40)
        print(f"Total: {j2_point}")

        print(f"\n{j1 if j1_point > j2_point else j2} a remporté la partie!\n")

        encore = input("Voulez-vous jouer une nouvelle partie? [o/N] ")
        if encore.strip() in ("o", "O"):
            continue
        else:
            break


def test():
    assert generer_grille(4) is not None
    assert generer_grille(5) is not None
    assert generer_grille(3) is None
    assert generer_grille(6) is None
    assert len(generer_grille(4)) == 4

    grille_test = [["A", "B", "C", "D"], ["E", "F", "G", "H"],
                   ["I", "J", "K", "L"], ["M", "N", "O", "P"]]
    assert est_valide(grille_test, "ABCD") == True
    assert est_valide(grille_test, "AEI") == True
    assert est_valide(grille_test, "AB") == False
    assert est_valide(grille_test, "ABCDH") == False
    assert est_valide(grille_test, "abcd") == False  # majuscule seulement

    assert calcul_point(["ABCD", "EFGH", "IJKL", "MNOP"]) == 8
    assert calcul_point(["ABCD", "EFGH", "IJKL", "MNOP", "ABCD"]) == 10
    assert calcul_point(["ABCD", "EFGH", "IJKL", "MNOP", "ABC", "EFG"]) == 10
    assert calcul_point(["ABCD", "ABC", "EFG", "ABA"]) == 5
    assert calcul_point([]) == 0


# jouer()
test()
