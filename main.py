# main.py

from game_state import Entreprise
from actions import acheter_matieres_premieres, production_hebdomadaire
from events import evenement_mensuel
from utils import afficher_etat

def afficher_menu():
    print("\n🧭 Que voulez-vous faire ?")
    print("1. Acheter matières premières")
    print("2. Finir la semaine")
    return input("Votre choix : ")

def main():
    entreprise = Entreprise()
    jeu_actif = True

    while jeu_actif:
        print("\n" + "="*40)
        afficher_etat(entreprise)  # affichage initial de la semaine
        semaine_active = True

        while semaine_active:
            choix = afficher_menu()

            if choix == "1":
                try:
                    quantite = int(input("📦 Quantité de MP à acheter : "))
                    ancien_mp = entreprise.stock["matiere_premiere"]
                    acheter_matieres_premieres(entreprise, quantite)
                    if entreprise.stock["matiere_premiere"] != ancien_mp:
                        afficher_etat(entreprise)  # réaffiche seulement si achat effectif
                except ValueError:
                    print("⛔ Entrée invalide.")
            elif choix == "2":
                production_hebdomadaire(entreprise)
                entreprise.semaine += 1
                if entreprise.semaine % 4 == 0:
                    evenement_mensuel(entreprise)
                semaine_active = False  # on sort de la boucle interne
            else:
                print("⛔ Choix invalide.")


if __name__ == "__main__":
    main()
