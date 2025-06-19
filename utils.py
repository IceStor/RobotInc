# utils.py

def afficher_etat(entreprise):
    print(f"\n📅 Semaine {entreprise.semaine}")
    print(f"💰 Argent : {entreprise.argent}€")
    print(f"📦 Stock - MP : {entreprise.stock['matiere_premiere']}, Robots : {entreprise.stock['robots']} / Max : {entreprise.stock_max}")
    print(f"🧠 Place utilisée : {entreprise.espace_utilise()} / {entreprise.stock_max} | Place libre : {entreprise.espace_disponible()}")
    print(f"👷 Ouvriers : {entreprise.ouvriers} | 👨‍🔬 Ingénieurs : {entreprise.ingenieurs}")
    print(f"🔮 Production théorique (prochaine semaine) : {production_theorique(entreprise)} robots")

def production_theorique(entreprise):
    capacite = entreprise.capacite_production()
    matieres_dispo = entreprise.stock["matiere_premiere"]
    robots_max = matieres_dispo * 10
    production_possible = min(capacite, robots_max, entreprise.espace_disponible())
    return production_possible
