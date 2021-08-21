from flask import render_template, url_for, flash, redirect
from webapp import app
from webapp.utils import load_changelog_json, load_datacard_json

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/datacards")
def datacards():
    datacards_data = load_datacard_json()
    return render_template('datacards.html', datacards = datacards_data)

@app.route("/rules")
def rules():
    return render_template('rules.html')

@app.route("/army_builder")
def army_builder():
    return render_template('army_builder.html')

@app.route("/changelog")
def changelog():
    changelog_data = load_changelog_json()
    return render_template('changelog.html', changelog = changelog_data)