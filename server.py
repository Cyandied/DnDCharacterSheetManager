import json
from flask import Flask, render_template, request, redirect, url_for, session, flash
from os import listdir, remove
from os.path import isfile, join
from classes import Character, Feature, Spell, Item, Area
from flask_login import LoginManager, UserMixin, login_user, login_required
import uuid
import func

class User():
    def __init__(self, name, password, id = None) -> None:
        self.name = name
        self.password = password
        self.id = id or str(uuid.uuid4())
    def to_json(self):        
        return {"name": self.name}

    def is_authenticated(self):
        return True

    def is_active(self):   
        return True           

    def is_anonymous(self):
        return False          

    def get_id(self):         
        return str(self.id)
    


app = Flask(__name__, static_url_path="", static_folder="static", template_folder="templates")

app.secret_key = "i/2r:='d8$V{[:gHm5x?#YBB-D-6)N"



login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    with open("users.json","r") as f:
        users = json.loads(f.read())
    for user in users:
        if user_id == user["id"]:
            correct_user = User(user["name"], user["password"], user["id"])
            
    return correct_user

def getFiles():
    onlyfiles = [f for f in listdir("characters") if isfile(join("characters", f))]
    nameList = []
    for entry in onlyfiles:
        name,_ = entry.split(".")
        nameList.append(name)
    return nameList

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        with open("users.json", "r") as f:
            users = json.loads(f.read())
        verified_user = False
        for user in users:
            if request.form["user"] == user["name"]:
                if request.form["pass"] == user["password"]:
                    verified_user = User(user["name"], user["password"], user["id"])
                    break
        
        if verified_user:
            login_user(verified_user)
            return redirect(url_for("index"))
    
    
    return render_template("login.html")


@app.route("/index", methods=["GET", "POST"])
@login_required
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

@app.route("/getMapMarkers", methods=["GET"])
def getMapMarkers():
    with open(f'static/mapStuff/markers.json', "r") as f:
        map = json.loads(f.read())
    return map

@app.route("/getGeoJSON", methods=["GET"])
def getGeoJSON():
    with open(f'static/mapStuff/geojson.json', "r") as f:
        geojson = json.loads(f.read())
    return geojson

@app.route("/getAreaItems", methods=["GET"])
def getAreaItems():
    with open(f'static/mapStuff/areas.json', "r") as f:
        areas = json.loads(f.read())
    relavantArea = Area("", 0,existingArea = areas[request.args.get("area")])
    return relavantArea.searchArea(focus = request.args.get("focus"))

@app.route("/map", methods=["GET", "POST"])   
def map():

    markerFiles = listdir("static/mapStuff/markerTypes")
    markers = []
    for marker in markerFiles:
        name,_ = marker.split(".")
        markers.append(name)


    with open(f'static/mapStuff/markers.json', "r") as f:
        map = json.loads(f.read())

    if request.method == "POST":

        with open(f'static/mapStuff/markers.json', "r") as f:
            map = json.loads(f.read())
        
        ids = []
        for marker in map:
            ids.append(marker["id"])

        if request.form["delete"]:
            for marker in map:
                if marker["id"] == int(request.form["id"]):
                    map.remove(marker)

        attributes = func.getAttributes(request.form["attribNames"], request.form["attribVals"])

        if request.form["name"] and int(request.form["id"]) not in ids:
            newMarker = {
                "name":request.form["name"],
                "description":request.form["desc"],
                "attributes":{
                    "names":attributes[0],
                    "values":attributes[1]
                },
                "iconType":request.form["icon"],
                "lat":request.form["lat"],
                "lang":request.form["lang"],
                "id":map[-1]["id"] + 1 if len(map)>0 else 1
            }
            map.append(newMarker)
        if int(request.form["id"]) in ids:
            for marker in map:
                if marker["id"] == int(request.form["id"]):
                    marker["name"]=request.form["name"]
                    marker["description"]=request.form["desc"]
                    marker["iconType"]=request.form["icon"]
                    marker["lat"]=request.form["lat"]
                    marker["lang"]=request.form["lang"]
                    marker["attributes"] = {
                    "names":attributes[0],
                    "values":attributes[1]
                    }

    with open(f'static/mapStuff/markers.json', "w") as f:
        f.write(json.dumps(map))

    return render_template("map.html", mapInfo = map, markers = markers)


@app.route("/sheet/<character>", methods=["POST","GET"])
# @login_required
def sheet(character):
    active_tab = "overview"
    
    with open(f'characters/{character}.json', "r") as f:
        sheet = json.loads(f.read())
    with open("itemsSpellsFeatures/spells.json","r") as f:
        spellsMaster = json.loads(f.read())
    with open("itemsSpellsFeatures/items.json","r") as f:
        itemsMaster = json.loads(f.read())

    sheet = Character(sheet)
    if request.method == "POST":
        sheet.Cname = request.form["Cname"]
        sheet.base["class"] = request.form["class"]
        sheet.base["level"] = int(request.form["level"])
        sheet.base["background"] = request.form["background"]
        sheet.base["race"] = request.form["race"]
        sheet.base["Pname"] = request.form["Pname"]
        sheet.base["alingment"] = request.form["alingment"]

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

        sheet.base["speed"]["land"] = request.form["land"]
        sheet.base["speed"]["flying"] = request.form["flying"]
        sheet.base["speed"]["swimming"] = request.form["swimming"]
        sheet.base["speed"]["climbing"] = request.form["climbing"]

        sheet.base["ac"] = request.form["ac"]
        sheet.base["passivePerception"] = 10 + sheet.skills["perception"]["modifier"]
        sheet.base["initiative"] = sheet.ability["modifiers"]["dex"]["flat"]

        sheet.base["deathSaves"]["failures"] = sum(["fail1" in request.form, "fail2" in request.form, "fail3" in request.form])
        sheet.base["deathSaves"]["successes"] = sum(["succ1" in request.form, "succ2" in request.form, "succ3" in request.form])

        if request.form["roll"] == "true" and sheet.base["hp"]["hitDice"]["sides"] != 0:
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
        if (sheet.base["hp"]["value"] + sheet.base["hp"]["max"]) <= 0 and sheet.base["hp"]["max"] > 0:
            sheet.base["hp"]["value"] = 0
            sheet.base["deathSaves"]["failures"] = 3
        elif sheet.base["hp"]["value"] < 0:
            sheet.base["hp"]["value"] = 0
        elif (sheet.base["hp"]["value"] - sheet.base["hp"]["max"]) > sheet.base["hp"]["max"]:
            sheet.base["hp"]["value"] = sheet.base["hp"]["max"]
        
        if request.form["classFeatTitle"] != "" and request.form["classFeatDesc"] != "":
            sheet.features["classFeatures"].append(Feature(request.form["classFeatTitle"],request.form["classFeatDesc"]).__dict__)

        if request.form["raceFeatTitle"] != "" and request.form["raceFeatDesc"] != "":
            sheet.features["raceFeatures"].append(Feature(request.form["raceFeatTitle"],request.form["raceFeatDesc"]).__dict__)

        if request.form["featsTitle"] != "" and request.form["featsDesc"] != "":
            sheet.features["feats"].append(Feature(request.form["featsTitle"],request.form["featsDesc"]).__dict__)

        if request.form["otherFeatTitle"] != "" and request.form["otherFeatDesc"] != "":
            sheet.features["otherFeats"].append(Feature(request.form["otherFeatTitle"],request.form["otherFeatDesc"]).__dict__)

        
        if request.form["othercontent"] != "":
            sheet.features["otherProfs"].append(request.form["othercontent"])

        if request.form["profcontent"] != "":
            sheet.features["profeciencies"].append(request.form["profcontent"])

        if request.form["langcontent"] != "":
            sheet.features["languages"].append(request.form["langcontent"])

        if request.form["resiscontent"] != "":
            sheet.features["resistances"].append(request.form["resiscontent"])

        if request.form["immucontent"] != "":
            sheet.features["immunities"].append(request.form["immucontent"])

        if request.form["vuneracontent"] != "":
            sheet.features["vulnerabilities"].append(request.form["vuneracontent"])

        if request.form["delete-features-title"] != "":
            print(request.form["delete-features-title"])
            print(request.form["delete-features-destination"])
            get = sheet.features[request.form["delete-features-destination"]]
            if isinstance(get[0], str):
                get.remove(request.form["delete-features-title"])
            else:
                for index, object in enumerate(get):
                    if object["title"] == request.form["delete-features-title"]:
                        get.pop(index)
        
        
        if request.form["delete-spells-title"] != "":
            print(request.form["delete-spells-title"])
            print(request.form["delete-spells-destination"])
            get = sheet.spells["level"][request.form["delete-spells-destination"]]
            for index, object in enumerate(get):
                if object["name"] == request.form["delete-spells-title"]:
                    get.pop(index)

        for name in sheet.biography["appearance"].keys():
            sheet.biography["appearance"][name] = request.form[name]

        for name in sheet.biography["personality"].keys():
            sheet.biography["personality"][name] = request.form[name]

        for name in sheet.biography["people"].keys():
            sheet.biography["people"][name] = request.form[name]

        sheet.biography["backstory"] = request.form["backstory"]
        sheet.biography["notes"] = request.form["notes"]

        file = request.files["profile-picture"]
        if file:
            file_extension = file.filename.split(".")[-1]
            file_name = f'{character}.{file_extension}'
            if sheet.biography["portrait"]:
                remove(join("static","profilePics", sheet.biography["portrait"]))
            file.save(join("static","profilePics", file_name))

            sheet.biography["portrait"] = file_name

        for level in sheet.spells["level"]:
            if level != "cantrips":
                sheet.spells["spellSlots"][level]["value"] = request.form[f'{level}-value']
                sheet.spells["spellSlots"][level]["max"] = request.form[f'{level}-max']

        if request.form["add-to-spell-list-name"] != "":
            for spell in spellsMaster:
                if spell["name"] == request.form["add-to-spell-list-name"]:
                    sheet.spells["level"][request.form["add-to-spell-list-level"]].append(spell)
                    break

        if request.form["spell-name-custom"] != "":
            custom_spell = Spell()
            custom_spell.name = request.form["spell-name-custom"]
            custom_spell.level = request.form["spell-level-custom"]
            custom_spell.classes = request.form["spell-classes-custom"]
            custom_spell.time = request.form["spell-time-custom"]
            custom_spell.range = request.form["spell-range-custom"]
            custom_spell.duration = request.form["spell-duration-custom"]
            custom_spell.components = request.form["spell-components-custom"]
            custom_spell.ritual = request.form["spell-ritual-custom"]
            custom_spell.school = request.form["spell-school-custom"]
            custom_spell.text = request.form["spell-text-custom"]

            with open(f'itemsSpellsFeatures/spells.json', "r") as outfile:
                object = json.loads(outfile.read())
            object.append(custom_spell.__dict__)
            with open(f'itemsSpellsFeatures/spells.json', "w") as outfile:
                outfile.write(json.dumps(object))
            if request.form["add-to-only-master"] == "":
                sheet.spells["level"][request.form["add-to-spell-list-level"]].append(custom_spell.__dict__)



        if request.form["delete-items-title"] != "":
            print(request.form["delete-items-title"])
            print(request.form["delete-items-destination"])
            get = sheet.inventory["equipment"][request.form["delete-items-destination"]]
            for index, object in enumerate(get):
                if object["name"] == request.form["delete-items-title"]:
                    get.pop(index)

        if request.form["add-to-item-list-name"] != "":
            for item in itemsMaster:
                if item["name"] == request.form["add-to-item-list-name"]:
                    item["amount"] = 1
                    sheet.inventory["equipment"][request.form["add-to-item-list-level"]].append(item)
                    break

        if request.form["item-name-custom"] != "":
            custom_item = Item()
            custom_item.name = request.form["item-name-custom"]
            custom_item.detail = request.form["item-detail-custom"]
            custom_item.weight = request.form["item-weight-custom"]
            custom_item.value = request.form["item-value-custom"]
            custom_item.text = request.form["item-text-custom"]

            with open(f'itemsSpellsFeatures/items.json', "r") as outfile:
                object = json.loads(outfile.read())
            object.append(custom_item.__dict__)
            with open(f'itemsSpellsFeatures/items.json', "w") as outfile:
                outfile.write(json.dumps(object))
            if request.form["add-to-only-master"] == "":
                item = custom_item.__dict__
                item["amount"] = 1
                sheet.inventory["equipment"][request.form["add-to-item-list-level"]].append(custom_item.__dict__)


        for slot in sheet.inventory["equipment"]:
            for item in sheet.inventory["equipment"][slot]:
                item["amount"] = request.form[f'{item["name"]}-amount'] if f'{item["name"]}-amount' in request.form else 1

        for monies in sheet.inventory["money"]:
            sheet.inventory["money"][monies] = request.form[monies]

        for thing in sheet.spells["spellBase"]:
            sheet.spells["spellBase"][str(thing)] = request.form[thing]
        active_tab = request.form["current-tab"]


    with open(f'characters/{character}.json', "w") as f:
        f.write(json.dumps(sheet.__dict__))

    

    return render_template("parts/sheet.html", sheet = sheet, name=character, itemsMaster = itemsMaster, spellsMaster = spellsMaster, active_tab = active_tab)

#Start server:
#flask --app server run --debug