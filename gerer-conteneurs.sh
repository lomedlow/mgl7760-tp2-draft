#!/bin/bash

# 1. Fonction pour créer l'environnement de développement avec tous les conteneurs à partir du dépôt de code source et d'une base de données initiale
creer_environnement() {
    echo "Création de l'environnement de développement..."

    
    echo killing old docker processes
    docker-compose rm -fs

    #Construire les images des démarer les contenaires
    docker-compose up --build -d

    #Construire l'image de Jenkins
    bash ./jenkins/install-jenkins.sh


    #Execution du build privee avec make
    #make all

    exit;
}

# 2. Fonction pour supprimer l'environnement de développement avec tous les conteneurs
supprimer_environnement() {
    echo "Suppression de l'environnement de développement... Etre dans le répertoire du projet"
    # Commande pour supprimer tous les conteneurs
    docker-compose down

    #Arreter et supprimer le conteneur et l'image de jenkins
    #docker stop $(docker ps -aq)
    docker stop jenkins_biblio
    docker rm jenkins_biblio

    exit;
}

# 3. Insertion dans la BD
inserer_dans_bd() {
    echo "Insertion dans la Base de données"
    #cd flask_app
    docker exec -it biblio python importer.py
    #cd ..
    exit;
}

# 4. Fonction pour démarrer des conteneurs
demarrer_conteneurs() {
    echo "Démarrage des conteneurs..."
    docker-compose start

    exit;
}

# 5. Fonction pour arrêter des conteneurs
arreter_conteneurs() {
    echo "Arrêt des conteneurs..."
    docker-compose stop

    exit;
}

# 6. Fonction pour executer le build prive
executer_build() {
    #Execution du build privee avec make
    make all

    exit;
}

# Afficher le menu
afficher_menu() {
    echo "Menu :"
    echo "1. Créer l'environnement de développement avec tous les conteneurs"
    echo "2. Supprimer l'environnement de développement avec tous les conteneurs"
    echo "3. Insertion dans le MySql"
    echo "4. Démarrer des conteneurs"
    echo "5. Arrêter des conteneurs"
    echo "6. Executer build prive"
    echo "7. Quitter"
}

# Boucle principale du script
while true; do
    afficher_menu
    read -p "Choisissez une option : " choix
    clear
    case $choix in
        1) creer_environnement ;;
        2) supprimer_environnement ;;
        3) inserer_dans_bd ;;
        4) demarrer_conteneurs ;;
        5) arreter_conteneurs ;;
        6) executer_build ;;
        7) echo "Merci d'avoir utilisé le script. Au revoir !"; exit ;;
        *) echo "Option invalide. Veuillez saisir un nombre entre 1 et 5." ;;
    esac
    echo "-----------------------------------------"
    sleep 1
done
