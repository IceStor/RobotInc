import random
from game_state import EffetTemporaire

def evenement_mensuel(entreprise):
    print("\n📅 Événement mensuel en cours...")

    # Mise à jour des effets temporaires
    entreprise.mise_a_jour_effets()

    evenements_possibles = [
        {"type":
            "prix_temp",
            "texte": f"📈 Hausse temporaire du coût des matières premières : " f"{entreprise.prix_mp_base} => {entreprise.prix_mp_base + (entreprise.prix_mp_base * 4)}!",
            "valeur": entreprise.prix_mp_base * 4, "duree": 4},
        {"type":
            "prix_def",
            "texte": "📈 Inflation permanente du coût des matières premières : " f"{entreprise.prix_mp_base} => {entreprise.prix_mp_base * 2}!",
            "valeur": entreprise.prix_mp_base * 2},
        # {"type":
        #     "bonus",
        #     "texte": "💼 Subvention gouvernementale ! +500€",
        #     "gain": 500},
        {"type":
            "neutre",
            "texte": "🌤️ Mois calme, aucun changement."},
    ]

    evenement = random.choice(evenements_possibles)
    print(evenement["texte"])

    if evenement["type"] == "prix_temp":
        # Ajout d'un effet temporaire qui dure plusieurs semaines
        effet = EffetTemporaire("Hausse prix MP", "hausse_prix_mp", evenement["valeur"], evenement["duree"])
        entreprise.effets_temporaire.append(effet)


    elif evenement["type"] == "prix_def":
        entreprise.prix_mp_base = evenement["valeur"]


    elif evenement["type"] == "bonus":
        entreprise.argent += evenement["gain"]

    # Pas besoin de reset, la gestion est dans mise_a_jour_effets()
