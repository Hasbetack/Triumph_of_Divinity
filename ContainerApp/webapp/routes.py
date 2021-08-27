from flask import render_template, url_for, flash, redirect, request
from webapp import app
from webapp.utils import load_changelog_json, filter_datacards_by_faction, filter_datacards_by_keyword, load_datacards_from_files


@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')


@app.route("/datacards", methods=['GET', 'POST'])
def datacards():
    datacards_data, all_factions, all_keywords = load_datacards_from_files()

    if request.method == 'POST':
        faction_list = request.form.getlist('faction-checkbox')
        keyword_list = request.form.getlist('keyword-checkbox')
        datacards_data = filter_datacards_by_faction(datacards_data, faction_list)
        datacards_data = filter_datacards_by_keyword(datacards_data, keyword_list, False)

    return render_template('datacards.html', datacards=datacards_data, all_factions=all_factions, all_keywords=all_keywords)


@app.route("/rules")
def rules():
    return render_template('rules.html')


@app.route("/army_builder")
def army_builder():
    return render_template('army_builder.html')


@app.route("/changelog")
def changelog():
    changelog_data = load_changelog_json()
    return render_template('changelog.html', changelog=changelog_data)