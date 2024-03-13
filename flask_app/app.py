import time
import redis
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from models import db, Livre, Auteur, Editeur, Categorie

app = Flask(__name__)

#Verification redis
cache = redis.Redis(host='redis', port=6379)
def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:motpass@dbmysql/bibliodb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)



with app.app_context():
    db.create_all()

# Page d'accueil qui pourrait afficher les livres ou avoir des liens vers d'autres fonctionnalités
@app.route('/')
def index():
    categories = Categorie.query.all()  # Récupère toutes les catégories de la base de données
    count = get_hit_count()
    return render_template('index.html', categories=categories, count=count)


# Route pour afficher tous les livres
@app.route('/livres')
def lister_livres():
    livres = Livre.chercher_tous()
    return render_template('liste_livres.html', livres=livres)

# Route pour afficher les détails d'un livre spécifique
@app.route('/livres/<int:id>')
def livre_details(id):
    livre = Livre.query.get_or_404(id)
    return render_template('details_livre.html', livre=livre)

# Route pour filtrer les livres par catégorie
@app.route('/categories/<int:categorie_id>')
def livres_par_categorie(categorie_id):
    categorie = Categorie.query.get_or_404(categorie_id)
    livres = Livre.chercher_par_categorie(categorie_id)
    return render_template('liste_livres.html', livres=livres, categorie=categorie)



# Route pour rechercher des livres par titre
@app.route('/recherche/titre', methods=['GET'])
def recherche_par_titre():
    titre = request.args.get('titre')  # Récupère le titre du formulaire de recherche
    livres = Livre.chercher_par_titre(titre)
    return render_template('liste_livres.html', livres=livres)


# Route pour rechercher des livres par auteur
@app.route('/recherche/auteur', methods=['GET'])
def recherche_par_auteur():
    auteur_nom = request.args.get('auteur')
    livres = Livre.chercher_par_auteur(auteur_nom)
    return render_template('liste_livres.html', livres=livres)



@app.route('/associations')
def voir_associations():
    # Cette requête va récupérer tous les livres avec leurs auteurs associés
    livres = Livre.query.all()
    return render_template('associations.html', livres=livres)



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)