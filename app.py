import os
from flask import Flask, request, json
from flask_sqlalchemy import SQLAlchemy
import datetime

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
db = SQLAlchemy()

class Personne(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    prenom = db.Column(db.String(100))
    date_naissance = db.Column(db.Date)        

@app.route('/create/', methods=['POST'])
def create():
    _nom = request.form['nom']
    _prenom = request.form['prenom']
    _date_naissance = request.form['date_naissance']
    responseMsg=""
    _status=None
    if getAge(_date_naissance) >=150:
        responseMsg= f"L'âge fourni pour {_prenom} {_nom} est trop élevé: {_date_naissance}"
        _status= 400
    else:
        newPerson = Personne(nom=_nom,
                            prenom=_prenom,
                            date_naissance=_date_naissance)
        db.session.add(newPerson)
        db.session.commit()
        #return f"Nouvelle personne ajoutée: {_nom} {_prenom}", 201
        responseMsg= f"Nouvelle personne ajoutée: {_nom} {_prenom}"
        _status= 200
        
    response = app.response_class(
        response=responseMsg,
        status=_status,
    )
    return response

@app.route('/display_all/', methods=['GET'])
def display_all():
    personnes = Personne.query.order_by(Personne.nom).all()
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

if __name__ == '__main__':
    app.config['SQLALCHEMY_DATABASE_URI'] =\
            'sqlite:///' + os.path.join(basedir, 'database.db')
    db.init_app(app)
    '''
    with app.app_context():
        db.drop_all()
        db.create_all()
    '''
    app.run(debug = True)
   