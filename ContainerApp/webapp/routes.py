from flask import render_template, url_for, flash, redirect, request
from webapp import app, Content
from webapp.utils import load_changelog_json, filter_datacards_by_faction, filter_datacards_by_keyword, parse_spaces_in_faction_name
import copy

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')


@app.route("/datacards", methods=['GET', 'POST'])
def datacards():
    datacards_data = copy.deepcopy(Content.DATACARDS)
    all_factions =   copy.deepcopy(Content.FACTIONS)
    all_keywords =   copy.deepcopy(Content.DATACARD_TAGS)

    if request.method == 'POST':
        faction_list = request.form.getlist('faction-checkbox')
        keyword_list = request.form.getlist('keyword-checkbox')
        datacards_data = filter_datacards_by_faction(datacards_data, faction_list)
        datacards_data = filter_datacards_by_keyword(datacards_data, keyword_list, False)

    return render_template(
        'datacards.html',
        datacards=datacards_data,
        all_factions=all_factions,
        all_keywords=all_keywords,
        weapon_ability_tooltip=Content.weapon_ability_tooltip,
        parse_spaces_in_faction_name=parse_spaces_in_faction_name)


@app.route("/army_builder")
def army_builder():
    return render_template('army_builder.html')


@app.route("/changelog")
def changelog():
    changelog_data = load_changelog_json()
    return render_template('changelog.html', changelog=changelog_data)