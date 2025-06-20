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

