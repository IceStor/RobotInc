# events.py

import random

def evenement_mensuel(entreprise):
    evenements = [
        ("Subvention gouvernementale", lambda e: setattr(e, 'argent', e.argent + 500)),
        ("Vol de stock", lambda e: e.stock.update({"matiere_premiere": max(0, e.stock["matiere_premiere"] - 20)})),
        ("Panne d'outils", lambda e: setattr(e, 'ouvriers', max(0, e.ouvriers - 1))),
        ("Prime innovation", lambda e: setattr(e, 'ingenieurs', e.ingenieurs + 1)),
    ]
    event = random.choice(evenements)
    print(f"💥 Événement aléatoire : {event[0]}")
    event[1](entreprise)
