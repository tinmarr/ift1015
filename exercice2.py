# exercice2.py
# auteur: Martin Chaperot
# date: 30 janvier 2023
# Python: 3.11.1

def calcul_accel(vf: float | int, vi: float | int, tf: float | int, ti: float | int):
    """
    Calcul l'accélération a partir d'un changement de vitesse.

    Args:
        vf: La vitesse finale
        vi: La vitesse initiale
        tf: Le temps final
        ti: Le temp initial
    """
    accel = (vf - vi) / (tf - ti) # L'accélération calculer

    if accel > 0:
        print(f"Accélération de: {accel}")
    elif accel < 0:
        print(f"Décélération de: {accel}")
    else:
        print("Aucune accélération")

if __name__ == "__main__":
    print("Test 1:")
    calcul_accel(36.1, 24.7, 2.47, 0)
    print("Test 2:")
    calcul_accel(0, 12.4, 2.55, 0)
