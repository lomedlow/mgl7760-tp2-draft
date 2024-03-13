from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Table d'association pour la relation plusieurs-à-plusieurs entre Livre et Auteur
livres_auteurs = db.Table('livres_auteurs',
    db.Column('livre_id', db.Integer, db.ForeignKey('livre.id'), primary_key=True),
    db.Column('auteur_id', db.Integer, db.ForeignKey('auteur.id'), primary_key=True)
)

# Table d'association pour la relation plusieurs-à-plusieurs entre Livre et Categorie
livre_categorie = db.Table('livre_categorie',
    db.Column('livre_id', db.Integer, db.ForeignKey('livre.id'), primary_key=True),
    db.Column('categorie_id', db.Integer, db.ForeignKey('categorie.id'), primary_key=True)
)

class Livre(db.Model):
    __tablename__ = 'livre'
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    isbn = db.Column(db.String(20), nullable=True)
    annee_apparition = db.Column(db.Integer)
    image = db.Column(db.String(100))
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_modification = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    editeur_id = db.Column(db.Integer, db.ForeignKey('editeur.id'), nullable=False)
    #categorie_id = db.Column(db.Integer, db.ForeignKey('categorie.id'), nullable=False)
    # Relations
    auteurs = db.relationship('Auteur', secondary=livres_auteurs, lazy='subquery',
                              backref=db.backref('livres', lazy=True))
    #categorie = db.relationship('Categorie', backref='livres', lazy=True)
    categories = db.relationship('Categorie', secondary=livre_categorie, lazy='subquery',
                             backref=db.backref('livres', lazy=True))
                            

    editeur = db.relationship('Editeur', backref='livres', lazy=True)

    # Méthodes de recherche
    @classmethod
    def chercher_tous(cls):
        return cls.query.all()

   # @classmethod
   # def chercher_par_categorie(cls, categorie_id):
     #    return cls.query.filter_by(categorie_id=categorie_id).all()

    @classmethod
    def chercher_par_categorie(cls, categorie_id):
        return cls.query.join(livre_categorie, cls.id == livre_categorie.c.livre_id)\
        .join(Categorie, Categorie.id == livre_categorie.c.categorie_id)\
        .filter(Categorie.id == categorie_id).all()

  

    @classmethod
    def chercher_par_titre(cls, titre):
        return cls.query.filter(cls.titre.ilike(f'%{titre}%')).all()


    @classmethod   
    def chercher_par_auteur(cls, auteur_nom):
        return cls.query.join(livres_auteurs).join(Auteur).filter(Auteur.nom.ilike(f'%{auteur_nom}%')).all()


class Auteur(db.Model):
    __tablename__ = 'auteur'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)

class Editeur(db.Model):
    __tablename__ = 'editeur'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)

class Categorie(db.Model):
    __tablename__ = 'categorie'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50))
    nom = db.Column(db.String(100), nullable=False)
    

