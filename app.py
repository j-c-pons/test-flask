import os
from flask import Flask, request, json
from flask_sqlalchemy import SQLAlchemy, asc
import datetime

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Personne(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    prenom = db.Column(db.String(100))
    date_naisse = db.Column(db.Date)        

app = Flask(__name__)

@app.route('/create/', methods=('POST'))
def create():
    _nom = request.form['nom']
    _prenom = request.form['prenom']
    _date_naissance = request.form['date_naissance']

    if getAge(_date_naissance) >=150:
        return "L'âge fourni pour "+_prenom+" "+_nom+" est trop élevé: "+_date_naissance, 400
    else:
        newPerson = Personne(nom=_nom,
                            prenom=_prenom,
                            date_naissance=_date_naissance)
        db.session.add(newPerson)
        db.session.commit()
        return "Nouvelle personne ajoutée: "+_nom+" "+_prenom, 201


@app.route('/display_all/', methodes=('GET'))
def display_all():
    personnes = Personne.query.all().order_by(asc(Personne.nom))
    personnes_list=[]
    
    for personne in personnes:
        personnes_list.append({"nom":personne.nom, "prenom":personne.prenom, "date_naissance":personne.date_naissance, "age":getAge(personne.date_naissance)})
    
    response = app.response_class(
        response=json.dumps(personnes_list),
        status=200,
    )
    return response


def getAge(date):
        today = datetime.date.today()
        difference_dates = today - date
        age = difference_dates.days // 365
        return age