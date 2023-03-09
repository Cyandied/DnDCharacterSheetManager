import json
from flask import Flask, render_template, request
from os import listdir
from os.path import isfile, join

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
    

    return render_template("index.html", files = files)

@app.route("/sheet", methods=["GET", "POST"])
def sheet():
    context = {}
    if request.method == "POST":
        data = {
            "firstName": request.form["first-name"],
            "lastName": request.form["last-name"],
            "age": request.form["age"]
        }
    #     with open("data.json", "w") as f:
    #         f.write(json.dumps(data))
    
    # with open("data.json", "r") as f:
    #     data = json.loads(f.read())
    
    # context["data"] = data

    return render_template("parts/sheet.html", context=context)

#Start server:
#flask --app server run --debug