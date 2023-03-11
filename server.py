import json
from flask import Flask, render_template, request, redirect, url_for
from os import listdir
from os.path import isfile, join
from classes import Character, Feature

app = Flask(__name__, static_url_path="", static_folder="static", template_folder="templates")

def getFiles():
    onlyfiles = [f for f in listdir("characters") if isfile(join("characters", f))]
    nameList = []
    for entry in onlyfiles:
        name,_ = entry.split(".")
        nameList.append(name)
    return nameList

@app.route("/", methods=["GET", "POST"])
def index():
    files = getFiles()

    if request.method == "POST":

        name_of_json =  request.form["name-of-json"]

        if f'{name_of_json}' not in files:
            with open(f'characters/{name_of_json}.json', "w") as f:
                character = Character()
                character.calcAttributes()
                character.calcSkillProf()
                f.write(json.dumps(character.__dict__))

        else:
            for i in range(2,len(files)+2):
                if f'{name_of_json}_{i}' not in files:
                    with open(f'characters/{name_of_json}_{i}.json', "w") as f:
                        character = Character()
                        character.calcAttributes()
                        character.calcSkillProf()
                        f.write(json.dumps(character.__dict__))
                    name_of_json = f'{name_of_json}_{i}'
                    break
        
        return redirect(url_for("sheet",character=name_of_json))

    return render_template("index.html", files = files)

@app.route("/sheet/<character>", methods=["GET", "POST"])
def sheet(character):
    with open(f'characters/{character}.json', "r") as f:
        sheet = json.loads(f.read())
    sheet = Character(sheet)
    if request.method == "POST":
        sheet.Cname = request.form["Cname"]
        sheet.base["class"] = request.form["class"]
        sheet.base["level"] = int(request.form["level"])
        sheet.base["background"] = request.form["background"]
        sheet.base["race"] = request.form["race"]
        sheet.base["Pname"] = request.form["Pname"]
        sheet.base["alingment"] = request.form["race"]

        sheet.ability["str"] = int(request.form["str"])
        sheet.ability["dex"] = int(request.form["dex"])
        sheet.ability["con"] = int(request.form["con"])
        sheet.ability["int"] = int(request.form["int"])
        sheet.ability["wis"] = int(request.form["wis"])
        sheet.ability["chr"] = int(request.form["chr"])

        sheet.ability["savingThrows"]["str"] = "strSave" in request.form
        sheet.ability["savingThrows"]["dex"] = "dexSave" in request.form 
        sheet.ability["savingThrows"]["con"] = "conSave" in request.form 
        sheet.ability["savingThrows"]["int"] = "intSave" in request.form
        sheet.ability["savingThrows"]["wis"] = "wisSave" in request.form
        sheet.ability["savingThrows"]["chr"] = "chrSave" in request.form

        sheet.calcAttributes()

        for skill, vals in sheet.skills.items():
            vals["hasSkill"] = int(request.form[skill])

        sheet.calcSkillProf()

        sheet.base["ac"] = request.form["ac"]
        sheet.base["passivePerception"] = 10 + sheet.ability["modifiers"]["wis"]["flat"]
        sheet.base["initiative"] = sheet.ability["modifiers"]["dex"]["flat"]

        sheet.base["deathSaves"]["failures"] = sum(["fail1" in request.form, "fail2" in request.form, "fail3" in request.form])
        sheet.base["deathSaves"]["successes"] = sum(["succ1" in request.form, "succ2" in request.form, "succ3" in request.form])

        if request.form["roll"] == "true":
            sheet.addHitDie()

        if request.form["temp"] == "":
            sheet.base["hp"]["temporary"] = 0
        elif request.form["temp"][0] == "-" or request.form["temp"][0] == "+":
            sheet.base["hp"]["temporary"] += int(request.form["temp"])
            if sheet.base["hp"]["temporary"] < 0:
                sheet.base["hp"]["value"] += sheet.base["hp"]["temporary"]
                sheet.base["hp"]["temporary"] = 0
        else: 
            sheet.base["hp"]["temporary"]=int(request.form["temp"])

        sheet.base["hp"]["hitDice"]["sides"] = int(request.form["hitdie"])
        if request.form["hpmax"] == "":
            sheet.base["hp"]["max"] = 0
        else: 
            sheet.base["hp"]["max"] = int(request.form["hpmax"])

        if request.form["hpvalue"] == "":
            sheet.base["hp"]["value"] = 0
        elif request.form["hpvalue"][0] == "-" or request.form["hpvalue"][0] == "+":
            sheet.base["hp"]["value"] += int(request.form["hpvalue"])
        else: 
            sheet.base["hp"]["value"] = int(request.form["hpvalue"])
        if (sheet.base["hp"]["value"] + sheet.base["hp"]["max"]) <= 0:
            sheet.base["hp"]["value"] = 0
            sheet.base["deathSaves"]["failures"] = 3
        elif sheet.base["hp"]["value"] < 0:
            sheet.base["hp"]["value"] = 0
        elif (sheet.base["hp"]["value"] - sheet.base["hp"]["max"]) > sheet.base["hp"]["max"]:
            sheet.base["hp"]["value"] = sheet.base["hp"]["max"]
        

        with open(f'characters/{character}.json', "w") as f:
            f.write(json.dumps(sheet.__dict__))

        if request.form["classFeatTitle"] and request.form["classFeatDesc"] != "":
            sheet.features["classFeatures"].append(Feature(request.form["classFeatTitle"],request.form["classFeatDesc"]).__dict__)
    
    # with open("data.json", "r") as f:
    #     data = json.loads(f.read())
    
    # context["data"] = data

    return render_template("parts/sheet.html", sheet = sheet, name=character)

@app.route("/new-sheet", methods=["POST"])
def new_sheet():
    print(request.body)
    return json.dumps("{'test': 'test'}")

#Start server:
#flask --app server run --debug