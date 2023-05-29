# Martin Chaperot (20205638) et Olivier Simard (20262563)
# Testé avec python 3.10.10
import csv
import json
from datetime import datetime
from typing import Optional, Any


def lire_comptes():
    comptes: list[dict[str, str]] = []
    with open("comptes.csv", "r") as f:
        reader = csv.DictReader(f,
                                fieldnames=(
                                    "matricule", "nom", "prenom", "mdp", "courriel", "role", "actif"
                                ),
                                delimiter="|",
                                )
        for row in reader:
            r = row
            for key, value in row.items():
                r[key] = value.strip()
            comptes.append(r)
    return comptes


def lire_commandes():
    commandes: list[dict[str, str]] = []
    with open("commandes.csv", "r") as f:
        reader = csv.DictReader(f,
                                fieldnames=(
                                    "id", "compte", "items", "date", "total",
                                ),
                                delimiter="|",
                                )
        for row in reader:
            r = row
            for key, value in row.items():
                r[key] = value.strip()
            commandes.append(r)
    return commandes


def ajouter_commande(items: str, total: int):
    global commandes
    with open("commandes.csv", "a", newline="\n") as f:
        s = ""
        if len(commandes) + 1 > 9:
            s = f"{len(commandes) + 1} | "
        else:
            s = f"{len(commandes) + 1}  | "
        date = datetime.now().strftime('%Y-%m-%d')

        s += f"{matricule} | {items} | {date} | {total:.2f}"

        f.write(s)

    commandes = lire_commandes()


def lire_menu() -> dict[str, Any]:
    with open("menu.json", "r") as f:
        menu = json.load(f)
    return menu


def compte_valide(matricule: str, mot_de_passe: str):
    for compte in comptes:
        if compte["matricule"].strip() == matricule and compte["mdp"].strip() == mot_de_passe:
            return compte["actif"].strip() == "1"
    return False


def obtenir_role(matricule: str) -> Optional[str]:
    for compte in comptes:
        if compte["matricule"].strip() == matricule:
            return compte["role"].strip()
    return None


def search_items(search_type, search_value=None):
    results = []

    def traverse(node):
        nonlocal search_type
        if isinstance(node, list):
            for item in node:
                if search_type == "id" and search_value is not None and str(item["id"]) == search_value:
                    results.append(item)
                elif search_type == "all":
                    results.append(item)
        elif isinstance(node, dict):
            for key, value in node.items():
                if search_type == "categorie" and search_value is not None and key == search_value:
                    if (val := value.get("items", None)) is not None:
                        results.extend(val)
                    else:
                        search_type = "all"
                        traverse(value)
                        return
                else:
                    traverse(value)

    traverse(menu)
    return results


def traiter_requetes_public(requete: str):
    if requete == "GET /api/menu/items":
        for item in search_items("all"):
            print(f"{item['id']}\t{item['nom']}")
        return True
    if requete.startswith("GET /api/menu/") and requete.endswith("/items"):
        category = requete[14:-6]
        for item in search_items("categorie", category):
            print(f"{item['id']}\t{item['nom']}")
        return True
    if requete.startswith("GET /api/menu/items/"):
        item_id = requete[20:]
        for item in search_items("id", item_id):
            print(
                f"{item['id']}\t{item['nom']}\t{item['prix']:.2f} $\t{'Disponible' if item['disponible'] else 'Pas Disponible'}")
        return True
    if requete.startswith("POST /api/commandes"):
        items = requete[20:].split(" ")
        total = 0
        for item in items:
            item_id = item.split("x")[0]
            for menu_item in search_items("id", item_id):
                total += int(item.split("x")[1]) * menu_item["prix"]
        ajouter_commande(", ".join(items), total)
        return True
    return False


def traiter_requetes_staff(requete: str):
    if traiter_requetes_public(requete):
        return True

    if requete == "GET /api/commandes":
        for c in commandes:
            print(f"{c['id']}\t{c['date']}\t{float(c['total']):.2f} $")
        return True
    if requete.startswith("GET /api/commandes/"):
        commande_id = requete[19:]
        for c in commandes:
            if c["id"] == commande_id:
                s = f"{c['id']}\t"
                items = c["items"].split(", ")
                for item in items:
                    item_id = item.split("x")[0]
                    for menu_item in search_items("id", item_id):
                        s += f"{item.split('x')[1]}x{menu_item['nom']}, "
                s = s[:-2]
                print(s + f"\t{c['date']}\t{float(c['total']):.2f} $")
                return True
        print("Commande introuvable.")
        return True
    if requete.startswith("PUT /api/menu/items/"):
        args = requete[20:]
        item_id = args.split(" ")[0]
        dispo = args.split(" ")[1]
        if dispo.startswith("disponible="):
            dispo = dispo.split("=")[1]
        else:
            print("Paramètre invalide.")
            return True

        for item in search_items("id", item_id):
            item["disponible"] = bool(int(dispo))
            with open("menu.json", "w") as f:
                json.dump(menu, f, indent=4)
            return True
        print("Item introuvable.")
        return True

    return False


def test():
    """
    This test function assumes that menu.json and comptes.csv contain at least
    the data given in the assignment description.
    """
    global menu, comptes

    # Test 1.1: lire_menu() returns a dictionary
    menu = lire_menu()
    assert isinstance(menu, dict), "lire_menu() should return a dictionary"

    # Test 1.2: Check if the menu contains at least one category
    assert len(menu) > 0, "Menu should contain at least one category"

    # Test 1.3: Check if each category in the menu contains items or subcategories
    for category, items in menu.items():
        assert "items" in items or any(isinstance(val, dict) for val in items.values(
        )), f"Category {category} should contain items or subcategories"

    def check_items(menu):
        for key, value in menu.items():
            if "items" in value:
                for item in value["items"]:
                    # Test 1.4: Check if each item has an 'id', 'nom', 'prix', and 'disponible' field
                    assert 'id' in item, f"Item {item} should have an 'id' field"
                    assert 'nom' in item, f"Item {item} should have a 'nom' field"
                    assert 'prix' in item, f"Item {item} should have a 'prix' field"
                    assert 'disponible' in item, f"Item {item} should have a 'disponible' field"

                    # Test 1.5: Check if each item's 'prix' is a positive number
                    assert item['prix'] > 0, f"Item {item} should have a positive 'prix' value"
            else:
                check_items(value)

    check_items(menu)

    comptes = lire_comptes()
    # Test 2.1: compte_valide() returns False for invalid credentials
    assert not compte_valide(
        "20140722", "sdPass_01"), "compte_valide() should return False for invalid credentials"

    # Test 2.2: compte_valide() returns True for valid credentials
    assert compte_valide(
        "20140721", "sdPass_03"), "compte_valide() should return True for valid credentials"

    # Test 2.3: compte_valide() returns False for an inactive account
    assert not compte_valide(
        "inactive_matricule", "inactive_password"), "compte_valide() should return False for an inactive account"

    # Test 2.4: compte_valide() returns False for a valid matricule but invalid password
    assert not compte_valide(
        "20140721", "sdPass_01"), "compte_valide() should return False for a valid matricule but invalid password"

    # Test 2.5: compte_valide() returns False for an invalid matricule but valid password
    assert not compte_valide(
        "20140722", "sdPass_03"), "compte_valide() should return False for an invalid matricule but valid password"

    def count_items(menu):
        item_count = 0
        for _, value in menu.items():
            if "items" in value:
                item_count += len(value["items"])
            else:
                item_count += count_items(value)
        return item_count

    # Test 3.1: search_items('all') returns all items in the menu
    all_items = search_items("all")
    total_items = count_items(menu)
    assert len(
        all_items) == total_items, "search_items('all') should return all items in the menu"

    # Test 3.2: search_items("categorie", "valid_category") returns all items in the specified category
    valid_category = "cafe"
    category_items = search_items("categorie", valid_category)
    expected_items_count = len(
        menu["boisson"]["boisson_chaude"][valid_category]["items"])
    assert len(
        category_items) == expected_items_count, f"search_items('categorie', '{valid_category}') should return all items in the specified category"

    # Test 3.3: search_items("categorie", "invalid_category") returns an empty list
    invalid_category = "eau"
    empty_items = search_items("categorie", invalid_category)
    assert len(
        empty_items) == 0, f"search_items('categorie', '{invalid_category}') should return an empty list"

    # Test 3.4: search_items("id", "valid_item_id") returns the item with the specified id
    valid_item_id = "1"
    item_search = search_items("id", valid_item_id)
    assert len(
        item_search) == 1, f"search_items('id', '{valid_item_id}') should return one item"
    assert item_search[0]['id'] == int(
        valid_item_id), f"search_items('id', '{valid_item_id}') should return the item with the specified id"

    # Test 3.5: search_items("id", "invalid_item_id") returns an empty list
    invalid_item_id = "0"
    empty_item_search = search_items("id", invalid_item_id)
    assert len(
        empty_item_search) == 0, f"search_items('id', '{invalid_item_id}') should return an empty list"


# test()


comptes = lire_comptes()
commandes = lire_commandes()
menu = lire_menu()

essaie = 0
while True:
    matricule = input("Entrez votre matricule : ")
    mot_de_passe = input("Entrez votre mot de passe : ")

    if compte_valide(matricule, mot_de_passe):
        print("Connexion réussie.")
        break
    else:
        essaie += 1
        print("Erreur d'authentification. Veuillez réessayer.")
    if essaie == 3:
        print("Trop d'erreurs d'authentification.")
        exit()

role = obtenir_role(matricule)

while True:
    requete = input("> ")

    if requete == "FIN":
        break

    if role == "public":
        if not traiter_requetes_public(requete):
            print("Requête invalide.")
    elif role == "staff":
        if not traiter_requetes_staff(requete):
            print("Requête invalide.")
