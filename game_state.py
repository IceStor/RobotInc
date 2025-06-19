# game_state.py

class Entreprise:
    def __init__(self):
        self.semaine = 1
        self.argent = 1000
        self.stock_max = 100
        self.stock = {
            "matiere_premiere": 10,
            "robots": 0,
        }
        self.ouvriers = 2
        self.ingenieurs = 1
        self.recherches = []
        self.recherches_en_cours = []
        self.contrats = []
        self.effets_temporaire = []

        # 🔄 Prix dynamique des matières premières
        self.prix_mp_base = 100


    def capacite_production(self):
        return self.ouvriers * 5

    def capacite_recherche(self):
        return self.ingenieurs * 2

    def espace_utilise(self):
        return self.stock["matiere_premiere"] * 5 + self.stock["robots"]

    def espace_disponible(self):
        return self.stock_max - self.espace_utilise()


    def prix_actuel_mp(self):
        prix = self.prix_mp_base
        for effet in self.effets_temporaire:
            if effet.type_effet == "hausse_prix_mp":
                prix += effet.valeur
        return max(prix, 1)  # prix minimum à 1€

    def mise_a_jour_effets(self):
        effets_fin = []
        for effet in self.effets_temporaire:
            effet.duree -= 1
            if effet.duree <= 0:
                effets_fin.append(effet)
        for effet in effets_fin:
            print(f"🛑 Fin de l'effet temporaire : {effet.nom}")
            self.effets_temporaire.remove(effet)


class EffetTemporaire:
    def __init__(self, nom, type_effet, valeur, duree):
        self.nom = nom
        self.type_effet = type_effet
        self.valeur = valeur
        self.duree = duree  # en semaines

    def semaine_passee(self):
        self.duree -= 1
        return self.duree <= 0  # True si expiré

    def description(self, entreprise):
        if self.type_effet == "hausse_prix_mp":
            prix_base = entreprise.prix_mp_base
            prix_modifie = prix_base + self.valeur
            return f"{self.nom} : +{self.valeur}€ MP ({prix_base}€ ➝ {prix_modifie}€), reste {self.duree} sem."
        return f"{self.nom} ({self.duree} sem. restantes)"


