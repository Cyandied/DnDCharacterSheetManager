import json
import base64
import requests
import xmltodict
import random

def save(character:object)->None:
    dictCharacter = character.__dict__
    with open(f'characters/{character.Cname}.json', "w") as outfile:
        json.dump(dictCharacter, outfile)

def addTo(url:str, type:str, toKeep:str)->None:
    req = requests.get(url)
    if req.status_code == requests.codes.ok:
        
        req = req.json()  # the response is a JSON
        # req is now a dict with keys: name, encoding, url, size ...
        # and content. But it is encoded with base64.
        content = base64.b64decode(req['content'])
    else:
        print('Content was not found.')
    contentAsDict = xmltodict.parse(content)
    with open(f'itemsSpellsFeatures/{type}.json', "r") as outfile:
        object = json.loads(outfile.read())

    for entry in contentAsDict["compendium"][toKeep]:
        object.append(entry)

    with open(f'itemsSpellsFeatures/{type}.json', "w") as outfile:
        outfile.write(json.dumps(object))


def d(num:int, faces:int)-> int:
    res = []
    for i in range(num):
        res.append(random.randint(1,faces))
    return sum(res)


get = "SwordCoastAdventurersGuide/items-scag.xml"

user = "kinkofer"
repo_name = "FightClub5eXML"
path_to_file = f'Sources/{get}'
url = f'https://api.github.com/repos/{user}/{repo_name}/contents/{path_to_file}'
type = ""
if get.split("/")[-1][0] == "i":
    type = "item"
else: type = "spell"

# addTo(url, f'{type}s', type)