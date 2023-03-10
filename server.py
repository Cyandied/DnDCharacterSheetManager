import json
from flask import Flask, render_template, request, redirect, url_for
from os import listdir
from os.path import isfile, join
from classes import Character

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
    if request.method == "POST":


        pass

    #     with open("data.json", "w") as f:
    #         f.write(json.dumps(data))
    
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