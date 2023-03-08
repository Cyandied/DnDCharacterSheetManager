import json
import classes
import base64
import requests
import xmltodict
import random

def save(character:classes.Character())->None:
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
    with open(f'itemsSpellsFeatures/{type}.json', "a") as outfile:
        json.dump(contentAsDict["compendium"][toKeep], outfile)


def d(num:int, faces:int)-> int:
    res = []
    for i in range(num):
        res.append(random.randint(1,faces))
    return sum(res)