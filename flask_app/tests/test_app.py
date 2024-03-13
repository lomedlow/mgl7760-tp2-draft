import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from flask import url_for
from app import app as flask_app

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()


def test_lister_livres_page(client):
    """Test de la route qui liste tous les livres."""
    response = client.get('/livres')
    assert response.status_code == 200
    

def test_home_page(client):
    """Test de la page d'accueil."""
    response = client.get('/')
    assert response.status_code == 200
    return response.data  

