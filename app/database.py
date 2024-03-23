import random
from sqlalchemy import JSON, Column,Integer,String,Float
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base 
from sqlalchemy.orm import sessionmaker

engine= create_engine("sqlite:///invoice.sqlite3",echo=True)

Session = sessionmaker(bind=engine)
Session = Session()

base=declarative_base()

def sessionsThread():
    try:
    # Commit the Session to persist the data
        Session.commit()
    except Exception as e:
        # Rollback the Session in case of an error
        Session.rollback()

    finally:
        # Close the Session
        Session.close()

###############################
#Shema
###############################

class Invoice(base):
    __tablename__ = 'invoice'

    id_invoice = Column(Integer,primary_key=True, autoincrement=True)
    customer_name=Column(String,nullable=True)
    amount=Column(Float,nullable=True)    
    
    # @property
    def __init__(self,customer_name, amount):
        """Creer une instance de calibrage pour un agent"""
        self.customer_name=customer_name
        self.amount=amount


class CDR(base):
    __tablename__ = 't_cdr'

    id = Column(Integer,primary_key=True, autoincrement=True)
    num_appelant = Column(String(15))
    num_appele = Column(String(15))
    imsi = Column(String(15))
    date = Column(String(15))
    duree = Column(Integer)
    type_abonne = Column(String(10)) 
    
    # @property
    

class Abonne(base):
    __tablename__ = 't_abonne'
    id = Column(Integer, primary_key=True)
    numero = Column(String(100), unique=True, nullable=False)
    services_utilises = Column(JSON, nullable=False)


class Services(base):
    __tablename__ = 't_service'
    id = Column(Integer, primary_key=True)
    nom = Column(String(100), unique=True, nullable=False)
    tarif = Column(Float, nullable=False)

    def __init__(self, nom, tarif):
        self.nom = nom
        self.tarif = tarif
        self.services = {}

    def ajouter_service(self, nom, tarif):
        self.services[nom] = tarif

    def obtenir_tarif_service(self, nom):
        return self.services.get(nom, None)

    def afficher_services(self):
        for service, tarif in self.services.items():
            print(f"Service: {service}, Tarif: {tarif}")

















base.metadata.create_all(engine)


def getAllInvoices():
    invoices = Session.query(Invoice).all()
    return invoices

def getAllServices():
    services = Session.query(Services).all()
    return services


def insererInvoiceInto(new_object):    
    Session.add(new_object)
    try:
        # Commit the Session to persist the data
        Session.commit()
        id = new_object.id_invoice

    except Exception as e:
        # Rollback the Session in case of an error
        Session.rollback()
        print(f"Failed to insert data. Error: {str(e)}")
    finally:
        # Close the Session
        Session.close()
    return id

def insererAbonne(new_object):    
    Session.add(new_object)
    try:
        # Commit the Session to persist the data
        Session.commit()
        # id = new_object.id_invoice

    except Exception as e:
        # Rollback the Session in case of an error
        Session.rollback()
        print(f"Failed to insert data. Error: {str(e)}")
    finally:
        # Close the Session
        Session.close()
    


def get_abonne_by_number(number):  
    try:
        # Effectuez la requête pour récupérer l'abonné en fonction de son numéro
        abonne = Session.query(Abonne).filter(Abonne.numero == number).first()

        if abonne:
            # print("Abonné trouvé :")
            # print(f"Numéro : {abonne.numero}")
            # print(f"Services utilisés : {abonne.services_utilises}")
            return abonne
        else:
            print("Abonné non trouvé.")
            return None
        

    except Exception as e:
        print(f"Erreur lors de la récupération de l'abonné. Erreur : {str(e)}")
        return None


def generateInvoice(new_object):
    Session.add(new_object)
    try:
        # Commit the Session to persist the data
        Session.commit()
        #id = new_object.id_invoice

    except Exception as e:
        # Rollback the Session in case of an error
        Session.rollback()
        print(f"Failed to insert data. Error: {str(e)}")
    finally:
        # Close the Session
        Session.close()
    

    print("\n----------------Fin----------------\n")


def insertFacture(new_object):
    Session.add(new_object)
    try:
        # Commit the Session to persist the data
        Session.commit()
        #id = new_object.id_invoice

    except Exception as e:
        # Rollback the Session in case of an error
        Session.rollback()
        print(f"Failed to insert data. Error: {str(e)}")
    finally:
        # Close the Session
        Session.close()
    


def generer_consommation_fictive(services):
    # stocker la consommation de chaque service
    consommation = {}

    # Générer une consommation aléatoire pour chaque service
    for service in services:
        # Générer une consommation aléatoire entre 0 et 1000 (par exemple)
        consommation[service] = random.randint(0, 1000)

    return consommation


# Fonction pour générer la facture d'un abonné
def generer_facture(info_abonne):
    montant_total = 0
    
    services_utilises = info_abonne.services_utilises
    # print("\n\nServices utilisés de l'abonné:", services_utilises, "\n\n")

    # Générer une consommation fictive aleatoire pour chaque service de l'abonné
    consommation = generer_consommation_fictive(services_utilises)

    # Parcourir tous les services utilisés par l'abonné
    for service in services_utilises:
        # Récupérer le tarif du service depuis la base de données
        print("\n\n", service, "\n\n")
        service_info = Session.query(Services).filter(Services.nom ==service).first()

        if service_info:
            tarif_service = service_info.tarif
            # Récupérer la consommation pour ce service
            consommation_service = consommation.get(service, 0)
            # Calculer le montant facturé pour ce service
            montant_service = tarif_service * consommation_service
            montant_total += montant_service

            # Créer une nouvelle facture dans la base de données
            nouvelle_facture = Invoice(customer_name=info_abonne.numero, amount=montant_service)
            Session.add(nouvelle_facture)
            Session.commit()

            print(f"Service: {service}, Tarif: {service_info.tarif}, Montant Service: {montant_service}")


        else:
            print(f"Service {service} non trouvé dans la base de données")
    
    # Afficher le montant total à payer
    print(f"Montant Total: {montant_total}")






# services_to_add = [
#     {"nom": "SERV_VOLTE", "tarif": 0.1},
#     {"nom": "SERV_ROAMING", "tarif": 0.15},
#     {"nom": "SERV_5G", "tarif": 0.2},
#     {"nom": "SERV_LTE", "tarif": 0.5},
#     {"nom": "SERV_3G", "tarif": 0.3},
#     {"nom": "SERV_VOICE", "tarif": 0.7},
#     {"nom": "SERV_SMS", "tarif": 0.2},
#     {"nom": "SERV_CFWNOREPLY", "tarif": 0.5},
#     {"nom": "SERV_CFWNOREACH", "tarif": 0.8},
#     {"nom": "SERV_CRBT", "tarif": 0.1},
# ]
    
# for service_data in services_to_add:
#     new_service = Services(nom=service_data["nom"], tarif=service_data["tarif"])
#     Session.add(new_service)

# Session.commit()
    

# get_abonne_by_number("Miraide")
    

# Supprimez les lignes de la table Invoice
Session.query(Invoice).delete()

# Confirmez les modifications
Session.commit()

# Fermez la session
Session.close()