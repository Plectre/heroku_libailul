import datetime
import json
from libaile import convert
from libaile import db

from flask import Flask, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, update
from werkzeug.security import generate_password_hash, check_password_hash

#app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite"
#db = SQLAlchemy(app)

# TABLE MEMBRES
class Users(db.Model):
    id = db.Column("id_user", db.Integer, primary_key=True)
    username = db.Column("name", db.String(100))
    password = db.Column("password", db.String(20))
    email = db.Column("email", db.String(50))
    is_admin = db.Column('is_admin', db.Boolean())

    def addUser(self, username, password, email=email, is_admin=False):
        hash_password = generate_password_hash(password) # hash du mot de passe
        usr = Users(username=username, password=hash_password, email=email, is_admin=is_admin)
        db.session.add(usr)
        db.session.commit()
        flash("le membre enregisté !", "sucess")
    def view_all(self):
        return Users.query.all()

## Update password by user
    def update_password(self, user, pw): # hash du mot de passe
        password = generate_password_hash(pw)
        Users.query.filter_by(username=user).update({Users.password : password})
        flash("Youpi !, dansons la carioca !", "success")
        db.session.commit()
        return

        
    def check_password(self, user, pw):
        user = Users.query.filter_by(username=user).first()
        if check_password_hash(user.password, pw): # un_hash du mot de passe
            return True
        else:
            return False

    def find_user(self, user):
        user = Users.query.filter_by(username=user).first()
        return user

    def find_profil(self, user):
        user = Users.query.filter_by(username=user).first()
        return user

    def delete_user(self, username):
        delete_user = Users.query.filter_by(username=username).first()
        db.session.delete(delete_user)
        db.session.commit()
        flash('Le membre à été supprimé avec succés !', "success")

# TABLE AIRCRAFT RENT ==========================================================
class RentAvion(db.Model):
    id = db.Column("id", db.Integer, primary_key=True, nullable=False)
    date = db.Column("date", db.String, nullable=False)
    pilote = db.Column("pilote", db.String, nullable=False)
    appareil = db.Column("appareil", db.String, nullable=False)
    heure = db.Column("heure", db.String, nullable=False)
    duree = db.Column("duree", db.Integer, nullable=False)

    def view_all(self):
        return RentAvion.query.all()

    def add_rent(self, pilote, appareil, date, heure, duree):
        str_date = cast_date_to_date_time(date)
        new_entrie = RentAvion(pilote=pilote,appareil=appareil, date=str_date, heure=heure, duree=duree)
        db.session.add(new_entrie)
        db.session.commit()

    def delete_rent(self, id):
        delete_rent = RentAvion.query.get(id)
        db.session.delete(delete_rent)
        db.session.commit()

    def find_user(self, user, id):
        whoIs = db.session.query(RentAvion.pilote).all()
        print(str(whoIs[3]) +":"+ str(id))
        if user == whoIs:
            return True
        else:
            return False

# TABLE PLANNING APPREILS ====================================================
class AircraftPlanning(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(20), nullable=False)
    start = db.Column(db.String(30))
    end = db.Column(db.String(30))

    def addAircraftResa(username, start, end=""):
        resa=AircraftPlanning(username=username, start=start, end=end)
        db.session.add(resa)
        db.session.commit()

    def removeAircraftResa (username, start):
        removeResa = AircraftPlanning.query.filter_by(username=username).all()
        for obj in removeResa:
            print(f'{obj.start} , {start}')
            if obj.start == start:
                db.session.delete(obj)
                db.session.commit()
                db.session.close()
                print('egal !')
            else:
                print('pas egal')


    def getPlanning(self):
        rents = AircraftPlanning.query.all()
        events = []
        rent = {}
        for i in rents:
            rent["username"] = i.username
            rent["start"] = i.start
            rent["end"] = i.end
            events.append(dict(rent))
        return events

# TABLE PILOT'S LOGBOOK ===============================================
class PilotLogBook(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    aircraft = db.Column(db.String(20), nullable=False)
    ident = db.Column(db.String(20), nullable=False)
    fro = db.Column(db.String(20), nullable=False)
    to = db.Column(db.String(20), nullable=False)
    start = db.Column(db.Integer, nullable=True)
    stop = db.Column(db.Integer, nullable=True)
    duration = db.Column(db.Integer, nullable=False)



    def add_log(self, username, date, aircraft, ident, fro, to, start, stop, duration):
        ##duration = convert.Convert().add(start, stop)
        if aircraft != "" and date != "" and ident != "" and fro != "" and to != "" and duration != "":
            str_date = cast_date_to_date_time(date)
            new_log = PilotLogBook(username=username, date=str_date, 
                            aircraft=aircraft.upper(), ident=ident.upper(), 
                            fro=fro.upper(), to=to.upper(), start=start, stop=stop, duration=duration)
            db.session.add(new_log)
            db.session.commit()
            flash("Le vol a été ajouté avec succés !", "success")
            return
        else:
            flash("Tous les champs doivent être remplis !", "error")
            return

    def view_logBook(self, user):
        return PilotLogBook.query.filter_by(username=user)

# TABLE FICHE INFO =======================================================

class FicheInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(20), nullable=False)
    content = db.Column(db.String(800), nullable=False)
    is_publish = db.Column(db.Boolean, nullable=True)

    # def __init__(self, id, title, content, is_publish):
    #     self.id = id
    #     self.title = title
    #     self.content = content
    #     self.is_publish = is_publish

    def updateInfo(self, title, content, is_publish):
        FicheInfo.query.filter_by(id=1).update({FicheInfo.title: title, 
                                                FicheInfo.content: content,
                                                FicheInfo.is_publish: is_publish})
        #newInfo = FicheInfo(title=title, content=content, is_publish=is_publish)
        #db.session.add(newInfo)
        db.session.commit()
        flash('... Ok cool ...' , 'success')
        return

def cast_date_to_date_time(date):
    date_time_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
    str_date = date_time_obj.strftime("%d/%m/%Y")
    return str_date