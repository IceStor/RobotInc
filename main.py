# main.py

from game_state import Entreprise
from contracts import generer_contrats_mensuels
from actions import acheter_matieres_premieres, production_hebdomadaire
from events import evenement_mensuel
from utils import afficher_etat, afficher_contrats


def afficher_menu():
    print("\n🧭 Que voulez-vous faire ?")
    print("1. Acheter matières premières")
    print("2. Finir la semaine")
    print("3. Voir contrats disponibles")
    print("4. Livrer un contrat")
    return input("Votre choix : ")

def main():
    entreprise = Entreprise()
    jeu_actif = True

    while jeu_actif:
        print("="*71)
        entreprise.verifier_sauvetage_ou_fail()
        afficher_etat(entreprise)  # affichage initial de la semaine
        semaine_active = True

        while semaine_active:
            choix = afficher_menu()

            if choix == "1":
                prix_unitaire = entreprise.prix_actuel_mp()
                print(f"\n💡 Prix actuel d’une matière première : {prix_unitaire}€")
                print("📦 Chaque unité prend 5 places de stockage.")

                max_par_espace = entreprise.espace_disponible() // 5
                max_par_argent = entreprise.argent // prix_unitaire
                max_possible = min(max_par_espace, max_par_argent)

                print(f"🔢 Vous pouvez acheter au maximum {max_possible} unité(s).")

                try:
                    quantite = int(input("📥 Quantité à acheter : "))
                    ancien_mp = entreprise.stock["matiere_premiere"]
                    acheter_matieres_premieres(entreprise, quantite)
                    if entreprise.stock["matiere_premiere"] != ancien_mp:
                        afficher_etat(entreprise)
                except ValueError:
                    print("⛔ Entrée invalide.")

            elif choix == "2":
                print('\n\n\n')
                production_hebdomadaire(entreprise)
                entreprise.semaine += 1
                entreprise.payer_salaires()
                if entreprise.semaine % 4 == 0:
                    entreprise.mise_a_jour_contrats()
                    evenement_mensuel(entreprise)

                semaine_active = False  # on sort de la boucle interne

                entreprise.mise_a_jour_effets()  # <-- Important : ici

            elif choix == "3":
                print('\n\n\n')
                afficher_contrats(entreprise)

                contrats_dispo = [
                    c for c in entreprise.contrats_disponibles if not c.selectionne
                ]
                if contrats_dispo:
                    reponse = input("📌 Souhaitez-vous sélectionner un contrat ? (o/n) : ").lower()
                    if reponse == "o":
                        try:
                            index = int(input(f"🔢 Numéro du contrat à sélectionner (1 à {len(contrats_dispo)}) : ")) - 1
                            index_reel = [
                                i for i, c in enumerate(entreprise.contrats_disponibles) if not c.selectionne
                            ][index]
                            entreprise.selectionner_contrat(index_reel)
                        except (ValueError, IndexError):
                            print("⛔ Numéro invalide.")
                else:
                    print("📭 Aucun contrat disponible à sélectionner.")


            else:
                print("⛔ Choix invalide.")


if __name__ == "__main__":
    main()
