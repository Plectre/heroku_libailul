
import json
import pdfkit
from flask import render_template, url_for, flash, redirect, session, request, abort
from flask_mail import Message, Mail
from werkzeug.security import generate_password_hash, check_password_hash
from libaile.models import Users, RentAvion, PilotLogBook, AircraftPlanning, FicheInfo
from libaile import app
#from libaile import card
from .datas.card import Card as card
#from .card import Card as card
from .meteo import fetchApi

#from libaile.planning import Planning
mail = Mail(app)


@app.route('/')
@app.route('/index')
def index():
    meteo = fetchApi()
    infos = FicheInfo.query.all()
    if "user" in session:
        return render_template('public/index.html', user=session['user'], cards=card.get_card(), infos=infos, meteo=meteo)
    else:
        return render_template('public/index.html', cards=card.get_card(), infos=infos, meteo=meteo)

@app.route('/public/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        usr = request.form['user']
        password = request.form['user_password']
        if usr == "" or password == "":
            flash('Merci de remplir tous les champs !', 'error')
            return render_template('login.html')
        findUser = Users().find_user(usr)
        if findUser is not None:
            is_password_true = Users().check_password(findUser.username, password)
            if is_password_true and findUser.is_admin:
                session['user'] = findUser.username
                #return redirect(url_for('admin'))
                return render_template('admin/admin.html')
            elif is_password_true:
                session['user'] = findUser.username
                #return redirect(url_for('member'))
                return redirect(url_for('member'))
            else:
                flash(
                    "Espece d'andouille, vous n'êtes pas enregistré ... Contactez votre gestionnaire !", "error")
            return render_template('public/login.html')
        else:
            flash(
                "Espece d'andouille, vous n'êtes pas enregistré ... Contactez votre gestionnaire !", "error")
            return render_template('public/login.html')
    return render_template('public/login.html')


@app.route('/addUser', methods=['POST', 'GET'])
def addUser():
    if request.method == "POST":
        usr = request.form['user']
        password = request.form['user_password']
        email = request.form['user_email']
        is_admin = 0
        if request.form.get('is_admin', False) == "on":
            is_admin = 1
        else:
            is_admin = 0
        findUser = Users().find_user(usr)

        if not findUser:
            Users().addUser(usr, password, email, is_admin)
            flash("Le membre a été ajouté avec succés !", "success")
            return redirect(url_for('add_member'))
        else:
            flash("le membre existe déjà !", "error")
            return redirect(url_for('add_member'))

# Form du panneau d'administration pour ajouter un utilisateur
@app.route('/add_member')
def add_member():
    val = Users().view_all()
    is_admin = False
    for usr in range(len(val)):             # Test de l'adequation username <=> is_admin
        if val[usr].is_admin and val[usr].username == session['user']:
            is_admin = True
    if 'user' in session and is_admin:
        for i in range(len(val)):           # remplacer le True renvoyè par la base de donnée
            if val[i].is_admin == True:     # par Oui
                val[i].is_admin = "Oui"
            else:
                val[i].is_admin = "Non"
        return render_template('admin/add_member.html', val=val)
    else:
        return render_template("public/login.html")
    return render_template('public/login.html')

#View du planning des appareils
@app.route('/public/view')
def view():
    if 'user' in session:
        aircraftPlanning = AircraftPlanning()
        rents = aircraftPlanning.getPlanning()
        return render_template('public/view.html', events=rents)
    return redirect(url_for('index'))

@app.route('/public/add_rent', methods=["POST"])
def planning_add_rent():
    json = request.get_json()
    json['user'] = session['user']
    if 'user' in session:
        add_rent = AircraftPlanning.addAircraftResa(json["user"], json['start'])
    return redirect(url_for('view'))

@app.route('/public/remove_rent', methods=['POST'])
def planning_remove_rent():
    json = request.get_json()
    print(json['user'])
    #on teste les droits de l'utilisateur
    if 'user' in session and json['user'] == session['user'] or session['user'] == 'admin':
        AircraftPlanning.removeAircraftResa(json["user"], json['start'])
        return redirect(url_for('view'))
    else:
        flash(f"vous ne pouver pas supprimer la rèservation de {json['user']} !", "error")
        return redirect(url_for('view'))
    return redirect(url_for('view'))

## =========================================================##
# Formulaire de location d'appareil
# @app.route('/public/rent_avion', methods=['POST', 'GET'])
# def rent_avion():
#     rentAvion = RentAvion()
#     if request.method == "POST":
#         pilote = session['user']
#         appareil = request.form['appareil']
#         date = request.form['date']
#         heure = request.form['heure']
#         duree = request.form['duree']
#         if pilote != "" and appareil != "" and date != "" and heure != "":
#             rentAvion.add_rent(pilote, appareil, date, heure, duree)
#             ##Planning().add_avion(pilote, appareil, date, heure)
#             flash("Réservation enregistrée ! Bon vol !", "success")
#         else:
#             flash("Tous les champs doivent être remplis !", "error")
#     return redirect(url_for('planning'))


# @app.route('/public/planning', methods=['POST', 'GET'])
# def planning():
#     if 'user' in session:
#         rent_avion = RentAvion().view_all()
#         return render_template('public/planning.html', val=rent_avion)
#     return redirect(url_for('index'))


# @app.route('/public/delete_rent/<int:id>/<string:user>')
# def del_planning(id, user):
#     rentAvion = RentAvion()
#     if 'user' in session and user == session['user'] or session['user'] == 'admin':
#         ## DETERMINER SI LE USER A LES DROITS DE SUPPRESSION ##########
#         rentAvion.delete_rent(id)
#         flash("Réservation supprimée !", "success")
#         return redirect(url_for('planning'))
#     else:
#         flash("Vous ne pouvez pas supprimer ce vol !", "error")
#         return redirect(url_for('planning'))


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))


@app.route('/admin')
def admin():
    if 'user' == 'admin':
        info = FicheInfo().query.filter_by(id=1)
        if info[0].is_publish == True:
            is_publish = True
            return render_template('admin/admin.html', info=info)
        else:
            return render_template('public/index.html')
    return render_template('public/login.html')

## ================ FICHE INFO LIBAILE =====================
@app.route('/admin/fiche_info')
def infos():
    return render_template('admin/fiche_info.html')

@app.route('/admin/publish_info', methods=['POST'])
def publishInfo():
    if request.method == "POST":
        title = request.form['title']
        message = request.form['message']
        is_publish = request.form.get('is_publish', False)
        if is_publish == "on":
            is_publish = 1
        else:
            is_publish = 0
        FicheInfo().updateInfo(title, message, is_publish)
        return render_template('admin/fiche_info.html')
    return render_template('admin/fiche_info.html')
##==========================================================

@app.route('/admin/del/<string:username>')
def admindel(username):
    Users().delete_user(username)
    return redirect(url_for('add_member'))


@app.route('/public/member')
def member():
    infos = FicheInfo().query.filter_by(id=1)
    if "user" in session:
        #usr = session["user"]
        if session['user'] == "admin":
            return render_template('admin/admin.html', infos=infos)
    else:
        return render_template('public/login.html')
    return render_template('public/member.html')

# LOGBOOK ==========================================================

@app.route('/public/logbook')
def logBook():
    log = PilotLogBook().view_logBook(session['user'])
    return render_template('public/logbook.html', val=log)

# Nouvelle entrée dans le logbook
@app.route('/public/add_logbook', methods=['GET', 'POST'])
def add_logBook():
    if request.method == 'POST':
        username = session['user']
        date = request.form['date']
        aircraft = request.form['aircraft']
        ident = request.form['ident']
        to = request.form['to']
        fro = request.form['from']
        horoStart = request.form['horoStart']
        horoStop = request.form['horoStop']
        duration = request.form['duration']
        pilotLogBook = PilotLogBook()
        pilotLogBook.add_log(username, date, aircraft,
                             ident, fro, to, horoStart, horoStop, duration)
    return redirect(url_for('logBook'))


@app.route('/public/contact')
def contact():
    return render_template('public/contact.html', title="Contact")


@app.route('/public/send_email', methods=['POST', 'GET'])
def send_email():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form["email"]
        message = request.form["message"]
        msg = Message(f"Subject: {name}", sender=email,
                      recipients=app.config['MAIL_USERNAME'])
        msg.body = message
        mail.send(msg)
    return redirect(url_for("public/contact"))


@app.route('/public/member_profil')
def member_profil():
    if session['user'] is not "admin":
        find_user = session["user"]
        user_profil = Users().find_profil(find_user)
        return render_template('public/member_profil.html', user_profil=user_profil)
    return render_template('public/login.html')

# Mise à jour du mot de passe par l'utilisateur


@app.route('/public/password-update', methods=['POST'])
def password_update():
    if request.method == "POST":
        password_1 = request.form["email-1"]
        password_2 = request.form["email-2"]
        if password_1 == password_2:
            # Appel base de donnée Users
            user = session['user']
            Users().update_password(user, password_1)
            return redirect(url_for("member_profil"))
        else:
            flash('Les deux mots de passe ne sont pas identiques !', 'error')
            return redirect(url_for("member_profil"))
