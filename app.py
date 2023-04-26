from flask import Flask
import mysql.connector


class Personne:
    def __init__(self, nom, prenom, date_naissance):
        self.nom = nom
        self.prenom = prenom
        self.date_naissance = date_naissance



app = Flask(__name__)

'''
@app.route("/")
def hello():
    return "hello"
'''

@app.route('/newPerson', methods=['POST'])
def create_personne():