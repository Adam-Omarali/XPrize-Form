#Align on header  for each page (link back to learn more, XPrize Info?, Better explanation)

from flask import Flask, render_template, session, request, redirect
from flask_session import Session
from tempfile import mkdtemp
import datetime
import random
import os
import sqlite3
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL') or 'sqlite:///input.db'

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMENANT"] = False
app.config["SESSION_TYPE"] = "filesystem" #now referenced variables using session["name"]
Session(app)

db = SQLAlchemy(app)
#cursor.execute("CREATE TABLE IF NOT EXISTS researchers (id, incentives, purpose, know, sign_up_1, research, mentor, often, seperate_competition, develop_research, thoughts, geography)")
class Researcher(db.Model): 
    id = db.Column("id", db.Integer, primary_key=True)
    user = db.Column(db.String(200))
    incentives = db.Column(db.String(500))
    purpose = db.Column(db.String(500))
    know = db.Column(db.String(100))
    sign_up = db.Column(db.String(100))
    research = db.Column(db.String(100))
    mentor = db.Column(db.String(100))
    often = db.Column(db.String(100))
    seperate_competition = db.Column(db.String(100))
    develop_research = db.Column(db.String(100))
    thoughts = db.Column(db.String(500))
    geography = db.Column(db.String(100))

    def __init__(self, user, incentives, purpose, know, sign_up, research, geography, mentor, often, seperate_competition, develop_research, thoughts):
        self.user = user
        self.incentives = incentives
        self.purpose = purpose
        self.know = know
        self.sign_up = sign_up
        self.research = research
        self.mentor = mentor
        self.often = often
        self.seperate_competition = seperate_competition
        self.develop_research = develop_research
        self.thoughts = thoughts
        self.geography = geography

class General(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    user = db.Column(db.String(200))
    know = db.Column(db.String(200))
    sign_up = db.Column(db.String(200))
    factors = db.Column(db.String(200))
    all_factors = db.Column(db.String(200))
    support_others = db.Column(db.String(200))
    funding = db.Column(db.String(200))
    programs = db.Column(db.String(200))
    person = db.Column(db.String(200))
    thoughts = db.Column(db.String(200))
    geography = db.Column(db.String(200))

    def __init__(self, user, know, sign_up, factors, all_factors, person, support_others, funding, programs, thoughts, geography):
        self.user = user
        self.know = know
        self.sign_up = sign_up
        self.factors = factors
        self.all_factors = all_factors
        self.support_others = support_others
        self.funding = funding
        self.programs = programs
        self.person = person
        self.thoughts = thoughts
        self.geography = geography


class Organizer(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    user = db.Column(db.String(200))
    competitors = db.Column(db.String(200))
    organization = db.Column(db.String(200))
    roadblocks = db.Column(db.String(200))
    ideas = db.Column(db.String(200))

    def __init__(self, user, competitors, organization, roadblocks, ideas):
        self.user = user
        self.competitors = competitors
        self.organization = organization
        self.roadblocks = roadblocks
        self.ideas = ideas



@app.route("/")
def index():
    session.clear()
    session["user"] = (str(datetime.datetime.now()) + str(random.randint(1, 100000))) #maybe math.randomed somewhere?
    return render_template("index.html", test=session)


@app.route("/index2")
def index2():
    return render_template("index2.html")

# @app.route("/<string:name>")
# def hello(name):
#     name = name
#     return f"Hello, {name}"

@app.route("/researcher", methods=['GET', 'POST'])
def researcher():
    if request.method == 'POST':
        values = Researcher(session["user"], str(request.form.getlist("incentives")), str(request.form.getlist("purpose")), request.form.get("know"), request.form.get("sign up"), request.form.get("research"), request.form.get("country"), "", "", "", "", "")
        db.session.add(values)
        db.session.commit()
        return redirect("/researcher2")
    return render_template("researcher.html", test=session)

@app.route("/researcher2", methods=['GET', 'POST'])
def researcher2():
    if request.method == "POST":
        query = Researcher.query.filter_by(user=session['user']).first()
        query.mentor = request.form.get("mentor")
        query.often = request.form.get("often")
        query.seperate_competition = request.form.get("competition")
        query.develop_research = request.form.get("develop_research")
        query.thoughts = request.form.get("barriers")
        db.session.commit()
        return render_template("thank-you.html")
    return render_template("researcher2.html")

@app.route("/technichal", methods=['GET', 'POST'])
def technichal():
    if request.method == "POST":
        person = "technichal"
        values = General(session["user"], request.form.get("know"), request.form.get("sign up"), str(request.form.getlist("factors")), request.form.get("all"), person, request.form.get("help"), "", "", "", "")
        db.session.add(values)
        db.session.commit()
        return redirect("/general2")
    return render_template("technichal.html")

@app.route("/cxo", methods=['GET', 'POST'])
def cxo():
    if request.method == "POST":
        person = "cxo"
        values = General(session["user"], request.form.get("know"), request.form.get("sign up"), str(request.form.getlist("factors")), request.form.get("all"), person, "", request.form.get("funding"), "", "", "")
        db.session.add(values)
        db.session.commit()
        return redirect("/general2")
    return render_template("cxo.html")

@app.route("/general", methods=['GET', 'POST'])
def general():
    if request.method == "POST":
        person = "general"
        values = General(session["user"], request.form.get("know"), request.form.get("sign up"), str(request.form.getlist("factors")), request.form.get("all"), person, "", "", "", "", "")
        db.session.add(values)
        db.session.commit()
        return redirect("/general2")
    return render_template("general.html")

@app.route("/general2", methods=['GET', 'POST'])
def general2():
    if request.method == "POST":
        query = General.query.filter_by(user=session['user']).first()
        query.thoughts = request.form.get("thoughts")
        query.geography = request.form.get("country")
        db.session.commit()
        return render_template("thank-you.html")
    return render_template("general2.html")

@app.route("/highschool", methods=["GET", "POST"])
def highschool():
    if request.method == "POST":
        person = "highschool"
        values = General(session["user"], request.form.get("know"), request.form.get("sign up"), str(request.form.getlist("factors")), request.form.get("all"), person, "", "", request.form.get("programs"), "", "")
        db.session.add(values)
        db.session.commit()
        return redirect("/general2")
    return render_template("student.html")

@app.route("/university", methods=["GET", "POST"])
def university():
    if request.method == "POST":
        person = "university"
        values = General(session["user"], request.form.get("know"), request.form.get("sign up"), str(request.form.getlist("factors")), request.form.get("all"), person, "", "", request.form.get("programs"), "", "")
        db.session.add(values)
        db.session.commit()
        return redirect("/general2")
    return render_template("student.html")

@app.route("/graduate", methods=["GET", "POST"])
def graduate():
    if request.method == "POST":
        person = "graduate"
        values = General(session["user"], request.form.get("know"), request.form.get("sign up"), str(request.form.getlist("factors")), request.form.get("all"), person, "", "", request.form.get("programs"), "", "")
        db.session.add(values)
        db.session.commit()
        return redirect("/general2")
    return render_template("student.html")

@app.route("/competition", methods=["GET", "POST"])
def competition():
    session.clear()
    session["user"] = (str(datetime.datetime.now()) + str(random.randint(1, 100000)))
    if request.method == "POST":
        person = "organizer"
        values = Organizer(session["user"], request.form.get("contestants"), request.form.get("organization"), request.form.get("barriers"), request.form.get("ideas"))
        db.session.add(values)
        db.session.commit()
        return render_template("thank-you.html")
    return render_template("competition.html")

@app.route("/tksxprize-results")
def results():
    return render_template("results.html")

@app.route("/tksxprize-results-general")
def general_results():
    general = General.query.all()
    return render_template("general-results.html", general=general)

@app.route("/tksxprize-results-researchers")
def researcher_results():
    researcher = Researcher.query.all()
    return render_template("researcher-result.html", researcher=researcher)

@app.route("/tksxprize-results-organizers")
def organizer_results():
    organizers = Organizer.query.all()
    return render_template("competition-result.html", organizers=organizers)

if __name__ == "__main__":
    db.create_all()
    app.run()