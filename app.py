from flask import Flask, render_template, Markup
from json2html import *
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client['5e-database']


@app.route("/")
def index():
    data = Markup(fetch_categories())
    return render_template('index.html', content=data)


@app.route("/ability-scores")
def ability_scores():
    return fetch_collection("ability-scores")


@app.route('/ability/<ability>')
def ability(ability):
    collection = db['ability-scores']
    data = collection.find({'index': ability})
    data = next(data, None)
    return render_template('ability.html', data=data)


@app.route('/skill/<skill>')
def skill(skill):
    collection = db['skills']
    data = collection.find({'index': skill})
    data = next(data, None)
    return render_template('skill.html', data=data)


def fetch_categories():
    filter = {"name": {"$regex": r"^(?!system\.)"}}
    data = db.list_collection_names(filter=filter)
    return render_template("categories.html", categories=data)


def fetch_collection(query: str):
    collection = db[query]
    data = list(collection.find())

    return render_template(f"{query}.html", data=data)
