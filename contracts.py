import random

NOMS_CLIENTS = ["Robotech", "MecaCorp", "InnovaBot", "CyberDyn", "AlphaSystems", "TheCombine"]
# Dictionnaire des sites possibles par client
SITES_PAR_CLIENT = {
    "Robotech": ["Paris", "Lyon", "Marseille", "Toulouse", "Nice", "Nantes", "Strasbourg", "Montpellier", "Lille", "Bordeaux"],
    "MecaCorp": ["Berlin", "Munich", "Hambourg", "Francfort", "Stuttgart", "Düsseldorf", "Dortmund", "Essen", "Brême", "Leipzig"],
    "InnovaBot": ["London", "Manchester", "Birmingham", "Liverpool", "Leeds", "Sheffield", "Bristol", "Newcastle", "Nottingham", "Cambridge"],
    "CyberDyn": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"],
    "AlphaSystems": ["Toronto", "Mexico City", "Vancouver", "Montreal", "Tokyo", "Seoul", "Bangkok", "Jakarta", "Delhi", "Shanghai", "Manila"],
    "Combine": ["Sydney", "Melbourne", "Auckland", "São Paulo", "Buenos Aires", "Lima", "Kuala Lumpur", "Hanoi", "Taipei"]
}

GAMMES_DISPONIBLES = ["V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9", "V10"]
SEMAINE_TRANSITION_MARCHE = 20  # semaine à laquelle la transition commence
DUREE_TRANSITION_MARCHE = 10    # durée pendant laquelle la transition a lieu
NOMBRE_MAX_CONTRATS = 3


class Contrat:
    def __init__(self, nom_client, nb_robots, delai, budget, prix):
        self.nom_client = nom_client
        self.nb_robots = nb_robots
        self.delai = delai
        self.delai_restant = delai
        self.budget = budget
        self.prix = prix
        self.selectionne = False
        self.acompte_verse = False
        self.livre = False
        self.expire = False


    def afficher(self, index=None):
        prefix = f"{index + 1}. " if index is not None else ""

        # Déterminer le statut du contrat
        if self.expire:
            statut = "❌ Expiré"
        elif self.livre:
            statut = "📦 En livraison"
        elif self.selectionne and self.acompte_verse:
            statut = "💰 Acompte versé"
        elif self.selectionne:
            statut = "✅ Sélectionné"
        else:
            statut = "🆕 Disponible"

        return (
            f"{prefix}📦 Client : {self.nom_client} | Robots : {self.nb_robots} | "
            f"Délais : {self.delai} sem. | Prix : {self.prix}€ / Budget : {self.budget}€ [{statut}]"
        )


def generer_contrats_mensuels(nombre):
    contrats = []
    for _ in range(nombre):
        nom = random.choice(NOMS_CLIENTS)
        # Robots demandés : multiple de 5 entre 20 et 50
        nb_robots = random.choice([i for i in range(20, 51, 5)])

        # Valeur "marché" par robot : entre 60€ et 120€, par palier de 10
        valeur_par_robot = random.choice([i for i in range(60, 121, 10)])

        # Calcul du budget avec une variation de ±10% aléatoire
        base_budget = nb_robots * valeur_par_robot
        fluctuation = random.uniform(0.9, 1.1)
        budget = int(base_budget * fluctuation)

        # Arrondi au multiple de 100 supérieur
        budget = int(round(budget / 100.0)) * 100

        # Générer un prix dans [70%, 100%] du budget, multiple de 100
        prix_min = int(budget * 0.7)
        prix = random.choice([i for i in range(prix_min, budget + 1, 100)])
        prix = int(round(prix / 100.0)) * 100  # Arrondi à la centaine la plus proche

        # Délai de livraison
        delai = random.randint(3, 6)

        # Créer le contrat
        contrats.append(Contrat(nom, nb_robots, delai, budget, prix))

    return contrats


