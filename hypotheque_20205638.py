# hypotheque_20205638.py
# Martin Chaperot
# 07 Fevrier 2023
# Python 3.11.1
# Ce programme calcul le versement mensuel d'un prêt a partir du montant du prêt, du taux
# d'intérêt, et de la durée du prêt.

def versement(pret: int, taux: float, duree: int) -> float:
    """
    Calcul le versement mensuel.

    Args:
        pret: Le pret initial
        taux: Le taux d'intérêt (pourcentage)
        duree: La durée du prêt (année)
    """
    interet_mensuel = taux / 100 / 12
    versement_mensuel = (pret * interet_mensuel) / (1 - pow(1 + interet_mensuel, -12*duree))
    return round(versement_mensuel, 2)

def affichage(pret: int, taux: float, duree: int):
    """
    Affichage des versement mensuel.

    Args:
        pret: Le pret initial
        taux: Le taux d'intérêt (pourcentage)
        duree: La durée du prêt (année)
    """
    interet_mensuel = taux / 100 / 12
    versement_mensuel = versement(pret, taux, duree)
    balance = pret
    print("Mois\t| Balance\t| Intérêt payé\t| Montant payé")
    for i in range(duree * 12):
        interet_paye = balance * interet_mensuel
        montant_paye = versement_mensuel - interet_paye
        print("{}\t| {:.2f} $\t| {:.2f} $\t| {:.2f} $\t".format(i, balance, interet_paye, montant_paye))
        balance -= montant_paye

def test():
    print(f"Cas 1: {versement(90_000, 7.5, 20)}")
    print(f"Cas 2: {versement(100_000, 5, 15)}")
    print(f"Cas 3: {versement(100_000, 10, 20)}")
    print(f"Cas 4: {versement(60_000, 6.5, 5)}")
    print(f"Cas 5: {versement(65_000, 8, 10)}")


if __name__ == "__main__":
    pret = input("Montant du prêt: $ ") # le montant du pret (non validé)
    taux = input("Taux d'intérêt: (%) ") # le taux (non validé)
    duree = input("Duree du prêt: (an) ") # la durée (non validé)
    
    try:
        pret = int(pret) 
        duree = int(duree)
        taux = float(taux)
        if not (0 <= taux <= 100):
            raise ValueError
        if not (duree > 0):
            raise ValueError
    except ValueError:
        raise ValueError("Une des valeurs rentré n'est pas valide.")
         
    affichage(pret, taux, duree)
