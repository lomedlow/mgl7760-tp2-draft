import csv
from models import db, Livre, Auteur, Editeur, Categorie
from app import app

def importer_donnees(csv_filepath):
    with app.app_context():
        with open(csv_filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                # Gestion de l'éditeur
                editeur_nom = row.get('editeur')
                editeur = Editeur.query.filter_by(nom=editeur_nom).first()
                if not editeur:
                    editeur = Editeur(nom=editeur_nom)
                    db.session.add(editeur)
                
                # Gestion des auteurs
                auteurs = []
                if row.get('auteurs'):
                    for auteur_nom in row['auteurs'].split(','):
                        auteur = Auteur.query.filter_by(nom=auteur_nom.strip()).first()
                        if not auteur:
                            auteur = Auteur(nom=auteur_nom.strip())
                            db.session.add(auteur)
                        auteurs.append(auteur)
                
                # Gestion des catégories
                categories = []
                if row.get('categories'):
                    for categorie_nom in row['categories'].split(','):
                        categorie = Categorie.query.filter_by(nom=categorie_nom.strip()).first()
                        if not categorie:
                            categorie = Categorie(nom=categorie_nom.strip())
                            db.session.add(categorie)
                        categories.append(categorie)
                
                # Création du livre
                livre = Livre(
                    titre=row.get('titre'),
                    description=row.get('description'),
                    isbn=row.get('isbn'),
                    annee_apparition=int(row['annee_apparition']) if row.get('annee_apparition') else None,
                    image=row.get('image'),
                    editeur=editeur
                )
                db.session.add(livre)
                db.session.flush()  # S'assurer que le livre a un ID avant de lier les relations
                
                # Associer les auteurs et les catégories au livre
                livre.auteurs = auteurs
                livre.categories = categories
                
                db.session.commit()

if __name__ == '__main__':
    importer_donnees('./biblio.csv')
