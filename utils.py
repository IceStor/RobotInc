# utils.py

def afficher_etat(entreprise):
    print(f" " * 30 + f"📅Semaine {entreprise.semaine}")
    print(f"💰 Argent : {entreprise.argent}€")
    print(f"📦 Stock - MP : {entreprise.stock['matiere_premiere']}, Robots : {entreprise.stock['robots']} / Max : {entreprise.stock_max}")
    print(f"🧠 Place utilisée : {entreprise.espace_utilise()} / {entreprise.stock_max} | Place libre : {entreprise.espace_disponible()}")
    print(f"👷 Ouvriers : {entreprise.ouvriers} | 👨‍🔬 Ingénieurs : {entreprise.ingenieurs}")
    print(f"🔮 Production théorique (prochaine semaine) : {production_theorique(entreprise)} robots")
    semaines = entreprise.semaines_solvables()
    if semaines < 4:
        print(f"💥 Trésorerie critique : vous pouvez payer {semaines} semaine(s) de salaire(s).")

    if entreprise.effets_temporaire:
        print("\n🌀 Effets temporaires actifs :")
        for effet in entreprise.effets_temporaire:
            print(f"  - {effet.description(entreprise)}")


def production_theorique(entreprise):
    ouvriers = entreprise.ouvriers
    mp_dispo = entreprise.stock["matiere_premiere"]
    espace_dispo = entreprise.espace_disponible()

    max_ouvriers_utilisables = min(ouvriers, mp_dispo)
    max_robot_possible = max_ouvriers_utilisables * 5
    max_robot_place = min(max_robot_possible, espace_dispo)

    return max_robot_place



def afficher_contrats(entreprise):
    print("📋 Contrats disponibles ce mois-ci :")
    for i, contrat in enumerate(entreprise.contrats_disponibles):
        if not contrat.selectionne:
            print(contrat.afficher(i))
    print("\n📌 Contrats en cours :")
    for contrat in entreprise.contrats_actifs:
        status = f"🕒 Reste {contrat.delai_restant} sem."
        print(f"- {contrat.nom_client} | Robots : {contrat.nb_robots} | {status}")




def tenter_livraison(entreprise):
    livrables = [c for c in entreprise.contrats_actifs if not c.livre and entreprise.stock["robots"] >= c.nb_robots]
    if not livrables:
        print("❌ Aucun contrat livrable.")
        return
    for i, c in enumerate(livrables):
        print(f"{i+1}. {c.nom_client} | Robots : {c.nb_robots}")
    choix = int(input("📦 Choisissez un contrat à livrer : ")) - 1
    contrat = livrables[choix]
    entreprise.stock["robots"] -= contrat.nb_robots
    entreprise.contrats_a_livrer.append(contrat)
    contrat.livre = True
    print(f"🚚 Livraison prévue semaine prochaine pour {contrat.nom_client}.")

