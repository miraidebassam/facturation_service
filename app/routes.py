# app/routes.py

from flask import jsonify, request
from app import app, db
from app.database import *

COUT_PAR_MINUTE = 25 #Cout par minute d'appel = 25 FCFA

@app.route('/invoices', methods=['GET'])
def get_invoices():
    invoices = getAllInvoices()
    invoices_list = []
    for invoice in invoices:
        invoices_list = [{'id': invoice.id_invoice, 'customer_name': invoice.customer_name, 'amount': invoice.amount} for invoice in invoices]

    return jsonify({'invoices': invoices_list})

@app.route('/create_invoices', methods=['POST'])
def create_invoice():
    data = request.get_json()
    new_invoice = Invoice(customer_name=data['customer_name'], amount=data['amount'])
    db.session.add(new_invoice)
    db.session.commit()
    return jsonify({'message': 'Invoice created successfully'}), 201



@app.route('/insertAbonne', methods=['POST'])
def insertAbonne():
    data = request.get_json()
    print("InsertAbonneFacturation: \n\n\n", data,"\n\n\n\n")
    new_abonne = Abonne(numero=data['number'], services_utilises=data['servicesToActivate'])
    insererAbonne(new_abonne)
    return jsonify({'message': 'Subscriber created successfully'}), 201



@app.route('/generate_invoice', methods=['POST'])
def generate_invoice():
    cdr_records = request.json.get('cdr_records', [])

    total_cost = 0

    for cdr_data in cdr_records:
        cdr = CDR(
            num_appelant=cdr_data['num_appelant'],
            num_appele=cdr_data['num_appele'],
            imsi=cdr_data['imsi'],
            date=cdr_data['dte'],
            duree=cdr_data['duree'],
            type_abonne=cdr_data['type_abonne']
        )
        #db.session.add(cdr)
        generateInvoice(cdr)

        # Calcul du coût en fonction de la durée de l'appel
        cost_per_call = (cdr_data['duree'] // 60) * COUT_PAR_MINUTE
        total_cost += cost_per_call

        # ... Autres traitements ou enregistrements liés à la facturation ...

    db.session.commit()

    return jsonify({'message': 'Invoice generated successfully', 'total_cost': total_cost})

@app.route('/test', methods=['GET'])
def test():
    try:
        # Votre logique de test ici
        message = "Test successful"
        # Retourner une réponse JSON avec un message
        return jsonify({"message": message})

    except Exception as e:
        # Gérer les erreurs et renvoyer une réponse d'erreur si nécessaire
        return jsonify({"error": str(e)}), 500  # Renvoie une réponse d'erreur HTTP 500


@app.route('/get_services/<string:service>', methods=['GET'])
def get_services(service):
    service = getService(service)
    # services_list = []
    # for service in services:
    #     services_list = [{'id': service.id, 'nom': service.nom, 'tarif': service.tarif} for service in services]

    return jsonify({'invoices': service})




@app.route('/generer_facture_abonne/<string:abonne>', methods=['GET','POST'])
def generer_facture_abonne(abonne):
    # Chercher l'abonne à travers son numéro
    info_abonne = get_abonne_by_number(abonne)

    if info_abonne:
        # Générer la facture pour l'abonné
        facture_genere = generer_facture(info_abonne)

        # Retourner la facture générée au format JSON
        return jsonify(facture_genere)
    else:
        # Si aucun abonné correspondant n'est trouvé, retourner un message d'erreur
        return jsonify({'error': 'Aucun abonné trouvé avec ce numéro.'}), 404


