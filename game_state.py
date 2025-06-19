# game_state.py

class Entreprise:
    def __init__(self):
        self.semaine = 1
        self.argent = 1000
        self.stock_max = 100  # capacité totale
        self.stock = {
            "matiere_premiere": 10,  # 10 MP * 5 = 50 de place
            "robots": 0,             # 0 robots * 1 = 0 de place
        }
        self.ouvriers = 2
        self.ingenieurs = 1
        self.recherches = []
        self.recherches_en_cours = []
        self.contrats = []

    def capacite_production(self):
        return self.ouvriers * 5  # robots/semaine

    def capacite_recherche(self):
        return self.ingenieurs * 2

    def espace_utilise(self):
        return self.stock["matiere_premiere"] * 5 + self.stock["robots"]

    def espace_disponible(self):
        return self.stock_max - self.espace_utilise()
