# actions.py

def acheter_matieres_premieres(entreprise, quantite):
    prix_unitaire = entreprise.prix_actuel_mp()
    cout_total = quantite * prix_unitaire
    espace_requis = quantite * 5

    if cout_total > entreprise.argent:
        print("💸 Pas assez d'argent.")
        return
    if entreprise.espace_disponible() < espace_requis:
        print("📦 Pas assez d’espace dans le stock.")
        return

    entreprise.argent -= cout_total
    entreprise.stock["matiere_premiere"] += quantite
    print(f"✅ Acheté {quantite} MP pour {cout_total}€ ({prix_unitaire}€/u), utilisé {espace_requis} d’espace.")


# actions.py

def production_hebdomadaire(entreprise):
    ouvriers = entreprise.ouvriers
    mp_dispo = entreprise.stock["matiere_premiere"]
    espace_dispo = entreprise.espace_disponible()

    max_ouvriers_utilisables = min(ouvriers, mp_dispo)
    max_robot_possible = max_ouvriers_utilisables * 5
    max_robot_place = min(max_robot_possible, espace_dispo)

    robot_produits = max_robot_place
    mp_consomme = (robot_produits // 5)

    entreprise.stock["robots"] += robot_produits
    entreprise.stock["matiere_premiere"] -= mp_consomme

    print(f"🤖 Production automatique : {robot_produits} robots produits.")


