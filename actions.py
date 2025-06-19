# actions.py

def acheter_matieres_premieres(entreprise, quantite, prix_unitaire=10):
    cout_total = quantite * prix_unitaire
    espace_requis = quantite * 5  # 1 MP = 5 unités de stockage

    if cout_total > entreprise.argent:
        print("💸 Pas assez d'argent.")
        return
    if entreprise.espace_disponible() < espace_requis:
        print("📦 Pas assez d’espace dans le stock.")
        return

    entreprise.argent -= cout_total
    entreprise.stock["matiere_premiere"] += quantite
    print(f"✅ Acheté {quantite} MP pour {cout_total}€, utilisé {espace_requis} de stockage.")

def production_hebdomadaire(entreprise):
    capacite = entreprise.capacite_production()
    matieres_dispo = entreprise.stock["matiere_premiere"]
    robots_max = matieres_dispo * 10  # chaque MP permet de produire 10 robots
    production_possible = min(capacite, robots_max)

    matieres_necessaires = (production_possible + 9) // 10  # arrondi haut
    espace_necessaire = production_possible  # 1 robot = 1 espace

    if entreprise.espace_disponible() < espace_necessaire:
        production_possible = entreprise.espace_disponible()
        matieres_necessaires = (production_possible + 9) // 10

    if production_possible > 0 and entreprise.stock["matiere_premiere"] >= matieres_necessaires:
        entreprise.stock["matiere_premiere"] -= matieres_necessaires
        entreprise.stock["robots"] += production_possible
        print(f"🤖 Production automatique : {production_possible} robots produits.")
    else:
        print("⚠️ Pas assez de MP ou d’espace pour produire.")
