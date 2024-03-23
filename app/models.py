# app/models.py

from app import db

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100))
    amount = db.Column(db.Float)
    # Ajoutez d'autres champs selon vos besoins


class Abonne(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(100), unique=True, nullable=False)
    services_utilises = db.Column(db.String(100), unique=True, nullable=False)

    def __init__(self, numero, services_utilises):
        self.numero = numero
        self.services_utilises = services_utilises

    def generer_facture(self):
        montant_total = 0
        for service, consommation in self.services_utilises.items():
            tarif_service = obtenir_tarif_service(service)
            montant_service = tarif_service * consommation
            montant_total += montant_service
            print(f"Service: {service}, Consommation: {consommation}, Montant: {montant_service}")
        print(f"Montant Total à Payer: {montant_total}")


class Services(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), unique=True, nullable=False)
    tarif = db.Column(db.Float, nullable=False)

    def __init__(self):
        self.services = {}

    def ajouter_service(self, nom, tarif):
        self.services[nom] = tarif

    def obtenir_tarif_service(self, nom):
        return self.services.get(nom, None)

    def afficher_services(self):
        for service, tarif in self.services.items():
            print(f"Service: {service}, Tarif: {tarif}")

# Exemple d'utilisation
gestion_services = Services()

# Ajout des services avec leurs tarifs
gestion_services.ajouter_service("Voix", 0.1)
gestion_services.ajouter_service("SMS", 0.05)
gestion_services.ajouter_service("Data", 0.2)

# Affichage des services avec leurs tarifs
gestion_services.afficher_services()

# Obtention du tarif d'un service spécifique
tarif_voix = gestion_services.obtenir_tarif_service("Voix")
print(f"Tarif de Voix: {tarif_voix}")


# Fonction fictive pour obtenir le tarif d'un service
def obtenir_tarif_service(service):
    tarifs = {"voix": 0.1, "sms": 0.05, "data": 0.2}
    return tarifs.get(service, 0)

# Exemple d'utilisation
abonne1 = Abonne("123456789", {"voix": 50, "sms": 100, "data": 500})
abonne1.generer_facture()

