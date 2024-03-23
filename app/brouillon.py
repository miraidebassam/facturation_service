    # Parcourir tous les services utilisés par l'abonné
    for service, consommation in info_abonne.services_utilises.items():
        # Récupérer le tarif du service depuis la base de données
        service_info = Session.query(Services).filter(nom=service).first()
        if service_info:
            tarif_service = service_info.tarif
            # Calculer le montant facturé pour ce service
            montant_service = tarif_service * consommation
            montant_total += montant_service
            print(f"Service: {service}, Consommation: {consommation}, Montant: {montant_service}")
        else:
            print(f"Service {service} non trouvé dans la base de données")
