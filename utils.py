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

    if entreprise.contrats_actifs:
        print("\n📌 Contrats en cours :")
        if entreprise.contrats_actifs:
            for i, contrat in enumerate(entreprise.contrats_actifs):
                print(contrat.afficher(i))


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
    mapping = {}
    display_index = 1
    for i, contrat in enumerate(entreprise.contrats_disponibles):
        if not contrat.selectionne:
            print(f"{display_index}. {contrat.afficher()}")  # sans passer l'index
            mapping[display_index] = i  # mapping affiché → index réel
            display_index += 1

    print("\n📌 Contrats en cours :")
    if not entreprise.contrats_actifs:
        print("⏳ Aucun contrat en cours.")
    else:
        for i, contrat in enumerate(entreprise.contrats_actifs):
             print(contrat.afficher(i))
    return mapping





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

