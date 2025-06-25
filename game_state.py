import random
import math

from contracts import generer_contrats_mensuels, NOMBRE_MAX_CONTRATS


class Entreprise:
    def __init__(self):
        self.semaine = 1
        self.argent = 10000
        self.stock_max = 100
        self.stock = {
            "matiere_premiere": 10,
            "robots": 0,
        }
        self.ouvriers = 2
        self.ingenieurs = 1
        self.salaire_ouvrier = 100
        self.salaire_ingenieur = 200

        self.recherches = []
        self.recherches_en_cours = []
        self.contrats = []
        self.effets_temporaire = []

        # 🔄 Prix dynamique des matières premières
        self.prix_mp_base = 100
        self.decouvert_max = -5000
        self.sauvetage_effectue = False

        self.sauvetages_restant = 3
        self.sauvetage_seuil = self.decouvert_max * 0.25  # Exemple : -1250 si max = -5000
        self.sauvetage_montant = 1000
        self.en_danger = False  # Indique qu'on a dépassé le découvert max ce tour-ci
        self.sauvetages_actionnaires_restants = 3


        #Contrat
        self.contrats_disponibles = generer_contrats_mensuels(NOMBRE_MAX_CONTRATS)
        self.contrats_actifs = []
        self.contrats_a_livrer = []


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


    def payer_salaires(self):
        total = self.ouvriers * self.salaire_ouvrier + self.ingenieurs * self.salaire_ingenieur
        self.argent -= total
        print(f"💸 Paiement des salaires : -{total}€ ({self.ouvriers} ouvriers, {self.ingenieurs} ingénieurs)")

        # Vérifie si plan de licenciement requis
        semaines = self.semaines_solvables()
        if semaines <= 2 and self.ouvriers + self.ingenieurs > 0:
            self.proposer_licenciement()


    def semaines_solvables(self):
        salaire_total = self.ouvriers * self.salaire_ouvrier + self.ingenieurs * self.salaire_ingenieur
        if salaire_total == 0:
            return float("inf")  # aucun salarié, donc solvable indéfiniment
        return self.argent // salaire_total


    def proposer_licenciement(self):
        total_employes = self.ouvriers + self.ingenieurs
        if total_employes == 0:
            return

        print("\n🚨 Situation critique : vous ne pourrez plus payer vos employés !")
        print("💼 Vous pouvez mettre en place un **plan de licenciement** pour éviter la faillite.")
        reponse = input("Souhaitez-vous licencier 25% du personnel ? (o/n) : ").lower()

        if reponse == "o":
            a_licencier = max(1, math.ceil(total_employes * 0.25))
            ouvriers_a_licencier = 0
            ingenieurs_a_licencier = 0

            for _ in range(a_licencier):
                if self.ouvriers > 0 and (self.ingenieurs == 0 or random.random() < 0.5):
                    self.ouvriers -= 1
                    ouvriers_a_licencier += 1
                elif self.ingenieurs > 0:
                    self.ingenieurs -= 1
                    ingenieurs_a_licencier += 1

            print(f"\n❌ {a_licencier} employés licenciés ({ouvriers_a_licencier} ouvriers, {ingenieurs_a_licencier} ingénieurs).")
            self.tours_en_danger = 0
        else:
            print("⏳ Aucun licenciement effectué. Attention au risque de faillite.")


    def verifier_sauvetage_ou_fail(self):
        if self.argent <= self.sauvetage_seuil and self.sauvetages_restant > 0:
            self.sauvetages_restant -= 1
            self.argent += self.sauvetage_montant
            print(
                f"🛟 Les actionnaires vous sauvent ! +{self.sauvetage_montant}€ (sauvetages restants : {self.sauvetages_restant})")

        if self.argent < self.decouvert_max:
            if self.en_danger:
                print("\n💥 Vous êtes resté trop longtemps en dessous du découvert autorisé.")
                print("❌ GAME OVER : Votre entreprise fait faillite.")
                exit()
            else:
                self.en_danger = True
                print(
                    "⚠️ Dépassement du découvert autorisé ! Vous devez remonter la trésorerie avant la fin du prochain tour.")
        else:
            self.en_danger = False  # On est remonté au-dessus, on réinitialise le risque



    def selectionner_contrat(self, index):
        contrat = self.contrats_disponibles[index]
        if not contrat.selectionne:
            contrat.selectionne = True
            self.contrats_actifs.append(contrat)
            acompte = int(contrat.prix * 0.25)
            self.argent += acompte
            contrat.acompte_verse = True
            print(f"✅ Contrat sélectionné. Acompte de {acompte}€ versé.")
        else:
            print("⚠️ Contrat déjà sélectionné.")


    def mise_a_jour_contrats(self):
        # ✅ Gérer les contrats sélectionnés
        contrats_restants = []
        for contrat in self.contrats_actifs:
            if contrat.livre:
                self.argent += contrat.prix - int(contrat.prix * 0.25)
                print(f"📦 Livraison terminée ! Contrat {contrat.nom_client} complété pour {contrat.prix}€.")
            elif contrat.delai_restant <= 0:
                print(f"⏳ Contrat expiré : {contrat.nom_client}")
                if contrat.acompte_verse:
                    retrait = int(contrat.prix * 0.25)
                    self.argent -= retrait
                    print(f"💸 Acompte remboursé : -{retrait}€")
                contrat.expire = True
            else:
                contrat.delai_restant -= 1
                contrats_restants.append(contrat)

        self.contrats_actifs = contrats_restants

        # ✅ Mise à jour mensuelle des contrats disponibles
        if self.semaine % 4 == 0:
            print("🔁 Rafraîchissement des contrats disponibles.")
            nb_actifs = len(self.contrats_actifs)
            nb_a_generer = NOMBRE_MAX_CONTRATS - nb_actifs
            self.contrats_disponibles = generer_contrats_mensuels(nb_a_generer)





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


