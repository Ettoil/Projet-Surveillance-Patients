import random
import uuid
from datetime import datetime,timedelta
import csv
import mysql.connector

host = "localhost"
user = "chefmed"
password = "1234"
database = "ssdp"

def generer_num_secu(sexe):
    if sexe == 'Masculin':
        sexe_digit = '1'
    elif sexe == 'Féminin':
        sexe_digit = '2'

    age_minimal = 18
    age_maximal = 100
    annee_actuelle = datetime.now().year

    annee_naissance = random.randint(annee_actuelle - age_maximal, annee_actuelle - age_minimal)
    mois_naissance = random.randint(1, 12)  # Mois de naissance
    
    num_secu = f"{sexe_digit}{annee_naissance % 100:02d}{mois_naissance:02d}{random.randint(10, 99):02d}{random.randint(100, 999):03d}{random.randint(10, 99):02d}"

    return num_secu

def generer_medecins(nb_medecins):
    medecins = []
    for _ in range(nb_medecins):
        identifiant = str(uuid.uuid4())[:5]
        mot_de_passe = str(uuid.uuid4())[:8]
        numero_telephone = f"06{''.join([str(random.randint(0, 9)) for _ in range(8)])}"
        nom = "Nom_" + str(random.randint(1, 100))
        prenom = "Prenom_" + str(random.randint(1, 100))
        medecins.append((identifiant, mot_de_passe, numero_telephone, nom, prenom, 0))  
        # Ajouter un compteur de patients initialisé à 0
    return medecins

def generer_patient(medecins):
    sexe = random.choice(['Masculin', 'Féminin'])
    num_secu = generer_num_secu(sexe)
    nom = "Nom_" + str(random.randint(1, 100))
    prenom = "Prenom_" + str(random.randint(1, 100))
    age = random.randint(18, 80)
    taille = round(random.uniform(150, 190), 1)  # Taille en cm
    poids = round(random.uniform(50, 100), 1)  # Poids en kg
    groupe_sanguin = random.choice(["A+", "B-", "AB+", "O-", "A-", "B+", "AB-", "O+"])
    telephone = f"06{''.join([str(random.randint(0, 9)) for _ in range(8)])}"
    email_provider = random.choice(['gmail.com', 'hotmail.com'])
    email = f"{prenom.lower()}.{nom.lower()}@{email_provider}"
    medecin = random.choice(medecins)
    id_medecin = medecin[0]  # Sélectionner aléatoirement un médecin et récupérer son identifiant

    return num_secu, sexe, nom, prenom, age, taille, poids, groupe_sanguin, telephone, email, id_medecin

def generer_mesure_medicale(itm,cpt):
    temperature = round(random.uniform(35, 41), 1)
    freq_cardiaque = random.randint(60, 120)
    tension = f"{random.randint(90, 140)}/{random.randint(60, 90)}"
    pouls = random.randint(50, 100)
    taux_o2_sang = round(random.uniform(95, 100), 1)
    cond_nerv = round(random.uniform(50, 120), 1)
    heure_mesure = datetime.now().replace(second=0, microsecond=0) #Avoir que l'heure et les minutes
    heure_mesure += timedelta(minutes=(itm*cpt)) #Intervalle Minute et Compteur
    return temperature, freq_cardiaque, tension, pouls, taux_o2_sang, cond_nerv, heure_mesure

def generer_capteurs(n):
    capteurs = [
        ("", "Tensiomètre", "Tension", "", ""),
        ("", "Oxymètre1", "Pouls", "", ""),
        ("", "Oxymètre2", "TauxO2Sang", "", ""),
        ("", "Électromyographe", "ConductionNerveuse", "", ""),
        ("", "Capteur de Fréquence cardiaque", "FreqCardiaque", "", ""),
        ("", "Capteur Thermique", "Temperature", "", "")
    ]
    ldl_capteurs = []
    for numsecu, nom, typemesure, mesure, heure in capteurs:
        ldl_capteurs.append((numsecu, (nom + "_" + n ), typemesure, mesure, heure))
    return ldl_capteurs


def generer_listes(nb_patients, medecins):
    patients = []
    mesures_patients = []
    ldl_capteurs = []
    
    for patient_index in range(nb_patients):
        while True:
            d_patient = list(generer_patient(medecins))
            id_medecin = d_patient[10]  # Récupérer l'identifiant du médecin généré pour ce patient
            if id_medecin in [medecin[0] for medecin in medecins]:  # Vérifier si l'identifiant existe dans la liste des médecins
                break  # Si l'identifiant existe, sortir de la boucle
        
        # Générer les capteurs pour ce patient
        n = str(random.randint(1, 100))
        d_capteurs = generer_capteurs(n)  
        d_capteurs = [(d_patient[0],) + capteur[1:] for capteur in d_capteurs]  # Associer le numéro de sécu du patient à chaque capteur
        
        patients.append(d_patient)

        # Incrémenter le compteur de patients du médecin associé
        index_medecin = [medecin[0] for medecin in medecins].index(id_medecin)  # Rechercher l'index du médecin dans la liste
        medecins[index_medecin] = medecins[index_medecin][:5] + (medecins[index_medecin][5] + 1,)

        # Générer les mesures médicales pour ce patient et les associer aux capteurs
        for mesure_index in range(10):  # 10 mesures pour chaque patient
            d_mesures = list(generer_mesure_medicale(1, mesure_index))
            mesures_patients.append([d_patient[0], *d_mesures])
            for capteur in d_capteurs:
                capteur_type = capteur[2]  # Récupérer le type de capteur actuel
                # Utiliser un dictionnaire pour mapper le type de capteur à l'indice approprié dans mesures_patients
                index_mesure = {"Tension": 3, "Pouls": 4, "TauxO2Sang": 5, "ConductionNerveuse": 6, "FreqCardiaque": 2, "Temperature": 1, "HeureMesure": 7}
                if capteur_type in index_mesure:  # Vérifier si le type de capteur est dans le dictionnaire
                    x = index_mesure[capteur_type]  # Obtenir l'indice correspondant dans mesures_patients
                    liste_capteur = list(capteur)
                    liste_capteur[3] = str(mesures_patients[-1][x])
                    liste_capteur[4] = mesures_patients[-1][7] 
                    ldl_capteurs.append(tuple(liste_capteur))

    return patients, mesures_patients, ldl_capteurs

def creer_base_utilisateur():
    try:
        # Établir une connexion avec le serveur MySQL en utilisant l'utilisateur root
        connexion = mysql.connector.connect(host=host, user="root", password="")
        curseur = connexion.cursor()

        # Vérifier si la base de données existe déjà
        curseur.execute("SHOW DATABASES;")
        databases = curseur.fetchall()
        db_exists = False
        for db in databases:
            if database in db:
                db_exists = True
                break

        if not db_exists:
            # Créer la base de données
            curseur.execute(f"CREATE DATABASE {database};")

            # Créer l'utilisateur avec tous les privilèges sur la base de données
            curseur.execute(f"CREATE USER IF NOT EXISTS '{user}'@'{host}' IDENTIFIED BY '{password}';")
            curseur.execute(f"GRANT ALL PRIVILEGES ON {database}.* TO '{user}'@'{host}';")
            curseur.execute("FLUSH PRIVILEGES;")

            print("Base de données et utilisateur créés avec succès.")
        else:
            print("La base de données et l'utilisateur existent déjà.")

    except Exception as e:
        print(f"Erreur lors de la création de la base de données et de l'utilisateur : {e}")

    finally:
        # Fermer la connexion
        if connexion is not None and connexion.is_connected():
            curseur.close()
            connexion.close()

def inserer_dans_base_de_donnees(data_medecins, data_patients, data_mesures, data_capteurs, hote, utilisateur, mot_de_passe, base_de_donnees):
    connexion = None  # Définir la variable connexion en dehors du bloc try pour qu'elle soit accessible dans le bloc finally

    try:
        # Établir une connexion avec le serveur MySQL
        connexion = mysql.connector.connect(host=hote, user=utilisateur, password=mot_de_passe, database=base_de_donnees)
        curseur = connexion.cursor()
        
        # Créer la table des médecins
        create_medecins= """
        CREATE TABLE IF NOT EXISTS Medecins (
            Identifiant VARCHAR(10) PRIMARY KEY,
            MotDePasse VARCHAR(10),
            NumeroTelephone CHAR(10),
            Nom VARCHAR(50),
            Prenom VARCHAR(50),
            NombrePatients INT
        );
        """
        curseur.execute(create_medecins)
        
        # Insérer les données des médecins dans la table
        insert_medecins = """
        INSERT INTO Medecins (Identifiant, MotDePasse, NumeroTelephone, Nom, Prenom, NombrePatients)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        curseur.executemany(insert_medecins, data_medecins)

        # Créer la table des patients
        create_patients = """
        CREATE TABLE IF NOT EXISTS Patients (
            NumSecu CHAR(15) PRIMARY KEY,
            Sexe VARCHAR(10),
            Nom VARCHAR(50),
            Prenom VARCHAR(50),
            Age INT,
            Taille FLOAT,
            Poids FLOAT,
            GroupeSanguin VARCHAR(5),
            Telephone CHAR(10),
            Email VARCHAR(100),
            IdMedecin VARCHAR(10),
            FOREIGN KEY (IdMedecin) REFERENCES Medecins(Identifiant)
        );
        """
        curseur.execute(create_patients)

        # Insérer les données des patients dans la table 
        insert_patients = """
        INSERT INTO Patients (
            NumSecu, Sexe, Nom, Prenom, Age, Taille, Poids, GroupeSanguin, Telephone, Email, IdMedecin
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        curseur.executemany(insert_patients, data_patients)
        
        # Créer la table des mesures des patients
        create_mesures_patient = """
        CREATE TABLE IF NOT EXISTS Mesures_Patient (
            Id INT AUTO_INCREMENT PRIMARY KEY,
            NumSecu CHAR(15),
            Temperature FLOAT,
            FreqCardiaque INT,
            Tension VARCHAR(10),
            Pouls INT,
            TauxO2Sang FLOAT,
            ConductionNerveuse FLOAT,
            HeureMesure DATETIME,
            FOREIGN KEY (NumSecu) REFERENCES Patients(NumSecu)
            );
            """
        curseur.execute(create_mesures_patient)

        # Insérer les données des mesures des patients dans la table
        insert_mesures_patient = """
        INSERT INTO Mesures_Patient(
            NumSecu, Temperature, FreqCardiaque, Tension, Pouls, TauxO2Sang, ConductionNerveuse, HeureMesure
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        curseur.executemany(insert_mesures_patient, data_mesures)
        
        # Créer la table des capteurs
        create_capteurs= """
        CREATE TABLE IF NOT EXISTS Capteurs (
            IdCapteur INT AUTO_INCREMENT PRIMARY KEY,
            NumSecu CHAR(15),
            NomCapteur VARCHAR(50),
            TypeMesure VARCHAR(50),
            Mesure VARCHAR(10),
            HeureMesure DATETIME,
            FOREIGN KEY (NumSecu) REFERENCES Patients(NumSecu)
        );
        """
        curseur.execute(create_capteurs)
        
        # Insérer les données des capteurs dans la table
        insert_capteurs = """
        INSERT INTO Capteurs (NumSecu, NomCapteur, TypeMesure, Mesure, HeureMesure)
        VALUES (%s, %s, %s, %s, %s);
        """
        curseur.executemany(insert_capteurs, data_capteurs)
        
        # Valider les changements et fermer la connexion
        connexion.commit()
        print("Données insérées dans la base de données avec succès !")

    except Exception as e:
        print(f"Erreur : {e}")

    finally:
        # Fermer la connexion
        if connexion is not None and connexion.is_connected():
            curseur.close()
            connexion.close()

def sauvegarder_fiches_patients_csv(hote, utilisateur, mot_de_passe, base_de_donnees, fichier_csv):
    try:
        # Établir une connexion avec le serveur MySQL
        connexion = mysql.connector.connect(host=hote, user=utilisateur, password=mot_de_passe, database=base_de_donnees)
        curseur = connexion.cursor()

        # Exécuter la requête SQL
        requete_sql = """
        SELECT Patients.NumSecu, Patients.Nom, Patients.Prenom, Patients.Telephone, Medecins.Nom, Medecins.Prenom, Medecins.NumeroTelephone
        FROM Patients
        JOIN Medecins ON Patients.IdMedecin = Medecins.Identifiant;
        """
        curseur.execute(requete_sql)

        # Écrire les résultats dans un fichier CSV
        with open(fichier_csv, mode='w', newline='') as fichier:
            writer = csv.writer(fichier)
            writer.writerow(['NumSecu', 'Nom_Patient', 'Prenom_Patient','Tel_Patient','Nom_Medecin','Prenom_Medecin','Tel_Medecin'])
            for row in curseur.fetchall():
                writer.writerow(row)

    finally:
        # Fermer la connexion
        if connexion.is_connected():
            curseur.close()
            connexion.close()

def sauvegarder_donnees_medicales_csv(hote, utilisateur, mot_de_passe, base_de_donnees, fichier_csv):
    try:
        # Établir une connexion avec le serveur MySQL
        connexion = mysql.connector.connect(host=hote, user=utilisateur, password=mot_de_passe, database=base_de_donnees)
        curseur = connexion.cursor()

        # Exécuter la requête SQL
        requete_sql = """
        SELECT Patients.NumSecu, Patients.Nom, Patients.Prenom, Mesures_Patient.Temperature, Mesures_Patient.FreqCardiaque, Mesures_Patient.Tension, Mesures_Patient.Pouls, Mesures_Patient.TauxO2Sang, Mesures_Patient.ConductionNerveuse, Mesures_Patient.HeureMesure
        FROM Patients
        JOIN Mesures_Patient ON Patients.NumSecu = Mesures_Patient.NumSecu;
        """
        curseur.execute(requete_sql)

        # Écrire les résultats dans un fichier CSV
        with open(fichier_csv, mode='w', newline='') as fichier:
            writer = csv.writer(fichier)
            writer.writerow(['NumSecu', 'Nom', 'Prenom', 'Temperature', 'FreqCardiaque', 'Tension', 'Pouls', 'TauxO2Sang', 'ConductionNerveuse', 'HeureMesure'])
            for row in curseur.fetchall():
                writer.writerow(row)

    finally:
        # Fermer la connexion
        if connexion.is_connected():
            curseur.close()
            connexion.close()
            
def sauvegarder_donnees_capteurs_csv(hote, utilisateur, mot_de_passe, base_de_donnees, fichier_csv):
    try:
        # Établir une connexion avec le serveur MySQL
        connexion = mysql.connector.connect(host=hote, user=utilisateur, password=mot_de_passe, database=base_de_donnees)
        curseur = connexion.cursor()

        # Exécuter la requête SQL pour récupérer les données des capteurs
        requete_sql = """
        SELECT DISTINCT Capteurs.NumSecu, Capteurs.NomCapteur, Patients.Nom, Patients.Prenom, Capteurs.TypeMesure
        FROM Capteurs
        JOIN Patients ON Capteurs.NumSecu = Patients.NumSecu;
        """
        curseur.execute(requete_sql)

        # Écrire les résultats dans un fichier CSV
        with open(fichier_csv, mode='w', newline='') as fichier:
            writer = csv.writer(fichier)
            writer.writerow(['NumSecu', 'NomCapteur', 'NomPatient', 'PrenomPatient', 'TypeMesure'])
            for row in curseur.fetchall():
                writer.writerow(row)

    finally:
        # Fermer la connexion
        if connexion.is_connected():
            curseur.close()
            connexion.close()


def sauvegarder_csv_medecins(data, fichier):
    with open(fichier, mode='w', newline='') as fichier_csv:
        writer = csv.writer(fichier_csv)
        writer.writerow(["Identifiant", "MotDePasse", "NumeroTelephone", "Nom", "Prenom", "NombrePatients"])
        writer.writerows(data)

def sauvegarder_csv_patients(data, fichier):
    with open(fichier, mode='w', newline='') as fichier_csv:
        ecrivain = csv.writer(fichier_csv)
        ecrivain.writerow(["NumSecu", "Sexe", "Nom", "Prenom", "Age", "Taille", "Poids","GroupeSanguin", "Telephone", "Email","IdMedecin"])
        ecrivain.writerows(data)

def sauvegarder_csv_mesures(data, fichier):
    with open(fichier, mode='w', newline='') as fichier_csv:
        ecrivain = csv.writer(fichier_csv)
        ecrivain.writerow(["NumSecu", "Temperature", "FreqCardiaque", "Tension", "Pouls", "TauxO2Sang", "ConductionNerveuse", "HeureMesure"])
        ecrivain.writerows(data)
        
def sauvegarder_csv_capteurs(data, fichier):
    with open(fichier, mode='w', newline='') as fichier_csv:
        writer = csv.writer(fichier_csv)
        writer.writerow(["NumSecu", "NomCapteur", "TypeMesure", "Mesure", "HeureMesure"])
        writer.writerows(data)

        
def sauvegarder_sql_medecins(data, fichier):
    with open(fichier, mode='w') as fichier_sql:
        fichier_sql.write("INSERT INTO Medecins (Identifiant, MotDePasse, NumeroTelephone, Nom, Prenom, NombrePatients) VALUES\n")
        for index, row in enumerate(data):
            values = f"('{row[0]}', '{row[1]}', '{row[2]}', '{row[3]}', '{row[4]}', {row[5]})"
            fichier_sql.write(f"{values}")
            if index < len(data) - 1:  # Vérifier si ce n'est pas la dernière ligne
                fichier_sql.write(",\n")  # Ajouter une virgule pour toutes les lignes sauf la dernière
        fichier_sql.write(";")

def sauvegarder_sql_patients(data, fichier):
    with open(fichier, mode='w') as fichier_sql:
        fichier_sql.write(f"USE {database};\n")
        fichier_sql.write("INSERT INTO Patients (NumSecu, Sexe, Nom, Prenom, Age, Taille, Poids, GroupeSanguin, Telephone, Email, IdMedecin) VALUES\n")
        for index, row in enumerate(data):
            values = f"('{row[0]}', '{row[1]}', '{row[2]}', '{row[3]}', {row[4]}, {row[5]}, {row[6]}, '{row[7]}', '{row[8]}', '{row[9]}', '{row[10]}')"
            fichier_sql.write(f"{values}")
            if index < len(data) - 1:  # Vérifier si ce n'est pas la dernière ligne
                fichier_sql.write(",\n")  # Ajouter une virgule pour toutes les lignes sauf la dernière
        fichier_sql.write(";")

def sauvegarder_sql_mesures(data, fichier):
    with open(fichier, mode='w') as fichier_sql:
        fichier_sql.write(f"USE {database};\n")
        fichier_sql.write("INSERT INTO Mesures_patient (NumSecu, Temperature, FreqCardiaque, Tension, Pouls, TauxO2Sang, ConductionNerveuse, HeureMesure) VALUES\n")
        for index, row in enumerate(data):
            values = f"('{row[0]}', {row[1]}, {row[2]}, '{row[3]}', {row[4]}, {row[5]}, {row[6]}, '{row[7]}')"
            fichier_sql.write(f"{values}")
            if index < len(data) - 1:  # Vérifier si ce n'est pas la dernière ligne
                fichier_sql.write(",\n")  # Ajouter une virgule pour toutes les lignes sauf la dernière
        fichier_sql.write(";")
        
def sauvegarder_sql_capteurs(data, fichier):
    with open(fichier, mode='w') as fichier_sql:
        fichier_sql.write("INSERT INTO Capteurs (NumSecu, NomCapteur, TypeMesure, Mesure, HeureMesure) VALUES\n")
        for index, row in enumerate(data):
            values = f"('{row[0]}', '{row[1]}', '{row[2]}', '{row[3]}', '{row[4]}')"
            fichier_sql.write(f"{values}")
            if index < len(data) - 1:
                fichier_sql.write(",\n")
        fichier_sql.write(";")
        
        

# Appeler la fonction pour créer la base de données et l'utilisateur
creer_base_utilisateur()

# Générer les attributs
medecins = generer_medecins(10)
patients, mesures, capteurs = generer_listes(10, medecins)


#Insérer les données dans la base de données
inserer_dans_base_de_donnees(medecins, patients, mesures, capteurs, host, user, password, database)

# Sauvegarder les données dans un fichier SQL
sauvegarder_sql_medecins(medecins, 'insert_medecins.sql')
sauvegarder_sql_patients(patients, 'insert_patients.sql')
sauvegarder_sql_mesures(mesures, 'insert_mesures_patient.sql')
sauvegarder_sql_capteurs(capteurs, 'insert_capteurs.sql')

# Sauvegarder les données dans un fichier CSV
sauvegarder_csv_medecins(medecins, 'Medecins.csv')
sauvegarder_csv_patients(patients, 'Patients.csv')
sauvegarder_csv_mesures(mesures, 'Mesures_patient.csv')
sauvegarder_csv_capteurs(capteurs, 'Capteurs.csv')

# Sauvegardes Estéthiques
sauvegarder_fiches_patients_csv(host, user, password, database, 'fiches_patients.csv')
sauvegarder_donnees_medicales_csv(host, user, password, database, 'donnees_medicales.csv')
sauvegarder_donnees_capteurs_csv(host, user, password, database, 'donnees_capteurs.csv')


