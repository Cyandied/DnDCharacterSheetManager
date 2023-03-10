from func import d
import math

class Character:
    def __init__(self):
        self.Cname = ""
        self.base = {
            "class":"",
            "level":0,
            "background":"",
            "race":"",
            "Pname":"",
            "alignment":"",
            "hp":{
                "value":0,
                "min":0,
                "max":0,
                "temporary":0,
                "hitDice": {
                    "sides":0,
                    "num":0
                }
            },
            "speed":{
                "running":0,
                "flying":0,
                "swimming":0,
                "climbing":0
            },
            "initiative":0,
            "ac":0,
            "deathSaves":{
                "successes":0,
                "failures":0
            }
        }
        self.ability = {
            "str":0,
            "dex":0,
            "con":0,
            "int":0,
            "wis":0,
            "chr":0,
            "savingThrows":{
                "str":False,
                "dex":False,
                "con":False,
                "int":False,
                "wis":False,
                "chr":False
            },
            
        }
        self.skills = {
            "acrobatics":False,
            "animalHandling":False,
            "Arcana":False,
            "athletics":False,
            "deception":False,
            "history":False,
            "insigt":False,
            "intimidation":False,
            "invenstigation":False,
            "medicine":False,
            "nature":False,
            "perception":False,
            "performance":False,
            "persuasion":False,
            "religion":False,
            "slightOfHand":False,
            "stealth":False,
            "survival":False,
            "passivePerception":0
        }
        self.biography = {
            "apperance":{
                "age":0,
                "height":0,
                "weight":0,
                "eyes":"",
                "skin":"",
                "hair":"",
                "description":"",
                "size":""
            },
            "portrait":"",
            "backstory":"",
            "personality":{
                "personalityTraits":"",
                "ideals":"",
                "bonds":"",
                "flaws":""
            },
            "people":{
                "allies":[],
                "enemies":[],
                "organizations":[],
                "other":[]
            }
        }
        self.features = {
            "profeciencies":[],
            "languages":[],
            "classFeatures":[],
            "raceFeatures":[],
            "feats":[],
            "other":[],
            "resistances":[],
            "immunities":[],
            "vunerabilities":[]
        }
        self.inventory = {
            "money":{
                "cp":0,
                "sp":0,
                "ep":0,
                "gp":0,
                "pp":0
            },
            "weapons":[],
            "armor":[],
            "consumables":[],
            "magical":[],
            "important":[],
            "misc":[],
            "treasure":[]
        }
        self.spells = {
            "cantrips":[],
            "level1":[],
            "level2":[],
            "level3":[],
            "level4":[],
            "level5":[],
            "level6":[],
            "level7":[],
            "level8":[],
            "level9":[],
            "spellBase":{
                "class":"",
                "ability":"",
                "saveDC":0,
                "bonus":0
            }
        }
    def addHitDie(self):
        hitDice = self.base["hp"]["hitDice"]["sides"]
        if self.base["level"] == 1:
            hpToAdd = hitDice + self.ability["modifiers"]["con"]
            self.base["hp"]["max"] += hpToAdd
    
        elif self.base["hp"]["hitDice"]["num"] < self.base["level"]:
            self.base["hp"]["hitDice"]["num"] += 1
            hpToAdd = d(1,hitDice) + self.ability["modifiers"]["con"]
            if hpToAdd > 0:
                self.base["hp"]["max"] += hpToAdd

    def calcAttributes(self):
        modifier = {}
        for attribute in self.ability:
            if attribute != "savingThrows":
                modifier[attribute] = math.floor((self.ability[attribute] - 10)/2)
                continue
            for throw in self.ability[attribute]:
                if self.ability[attribute][throw]:
                    modifier[throw] += math.ceil(1 + 1/4 * self.base["level"])
            break
        self.ability["modifiers"] = modifier




