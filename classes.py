from func import d
import math

class Spell:
    def __init__(self) -> None:
        self.name = ""
        self.level = ""
        self.classes = ""
        self.time = ""
        self.range = ""
        self.duration = ""
        self.components =""
        self.ritual =""
        self.school = ""
        self.text  =""


class Item:
    def __init__(self) -> None:
        self.name = ""
        self.detail =""
        self.weight = ""
        self.value = ""
        self.text = ""




class Feature:
    def __init__(self, title, desc) -> None:
        self.title = title
        self.desc = desc


class Character:
    def __init__(self,existingChr = None):
        self.Cname = "" if existingChr == None else existingChr["Cname"]
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
                "land":0,
                "flying":0,
                "swimming":0,
                "climbing":0
            },
            "initiative":0,
            "ac":0,
            "deathSaves":{
                "successes":0,
                "failures":0
            },
            "passivePerception":0
        } if existingChr == None else existingChr["base"]
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
            
        } if existingChr == None else existingChr["ability"]
        self.skills = {
            "acrobatics":{
                "hasSkill":0,
                "label":"acrobatics",
                "modifier":0
            },
            "animalHandling":{
                "hasSkill":0,
                "label":"animal handling",
                "modifier":0
            },
            "arcana":{
                "hasSkill":0,
                "label":"arcana",
                "modifier":0
            },
            "athletics":{
                "hasSkill":0,
                "label":"athletics",
                "modifier":0
            },
            "deception":{
                "hasSkill":0,
                "label":"deception",
                "modifier":0
            },
            "history":{
                "hasSkill":0,
                "label":"history",
                "modifier":0
            },
            "insight":{
                "hasSkill":0,
                "label":"insight",
                "modifier":0
            },
            "intimidation":{
                "hasSkill":0,
                "label":"intimidation",
                "modifier":0
            },
            "investigation":{
                "hasSkill":0,
                "label":"investigation",
                "modifier":0
            },
            "medicine":{
                "hasSkill":0,
                "label":"medicine",
                "modifier":0
            },
            "nature":{
                "hasSkill":0,
                "label":"nature",
                "modifier":0
            },
            "perception":{
                "hasSkill":0,
                "label":"perception",
                "modifier":0
            },
            "performance":{
                "hasSkill":0,
                "label":"performance",
                "modifier":0
            },
            "persuasion":{
                "hasSkill":0,
                "label":"persuasion",
                "modifier":0
            },
            "religion":{
                "hasSkill":0,
                "label":"religion",
                "modifier":0
            },
            "slightOfHand":{
                "hasSkill":0,
                "label":"slight of hand",
                "modifier":0
            },
            "stealth":{
                "hasSkill":0,
                "label":"stealth",
                "modifier":0
            },
            "survival":{
                "hasSkill":0,
                "label":"survival",
                "modifier":0
            }
        } if existingChr == None else existingChr["skills"]
        self.biography = {
            "appearance":{
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
            "notes":"",
            "personality":{
                "personalityTraits":"",
                "ideals":"",
                "bonds":"",
                "flaws":""
            },
            "people":{
                "allies":"",
                "enemies":"",
                "organizations":"",
                "other":""
            }
        } if existingChr == None else existingChr["biography"]
        self.features = {
            "profeciencies":[],
            "languages":[],
            "classFeatures":[],
            "raceFeatures":[],
            "feats":[],
            "otherFeats":[],
            "otherProfs":[],
            "resistances":[],
            "immunities":[],
            "vulnerabilities":[]
        } if existingChr == None else existingChr["features"]
        self.inventory = {
            "money":{
                "cp":0,
                "sp":0,
                "ep":0,
                "gp":0,
                "pp":0
            },
            "equipment":{
            "weapons":[],
            "armor":[],
            "consumables":[],
            "magical":[],
            "important":[],
            "misc":[],
            "treasure":[]
            }

        } if existingChr == None else existingChr["inventory"]
        self.spells = {
            "level":{
            "cantrips":[],
            "level1":[],
            "level2":[],
            "level3":[],
            "level4":[],
            "level5":[],
            "level6":[],
            "level7":[],
            "level8":[],
            "level9":[]
            },
            "spellBase":{
                "class":"",
                "ability":"",
                "saveDC":0,
                "bonus":0
            }
        } if existingChr == None else existingChr["spells"]


    def addHitDie(self):
        hitDice = self.base["hp"]["hitDice"]["sides"]
        if self.base["hp"]["hitDice"]["num"] < self.base["level"]:
            if self.base["hp"]["hitDice"]["num"] < 1:
                hpToAdd = hitDice + self.ability["modifiers"]["con"]["flat"]
                if hpToAdd > 0:
                    self.base["hp"]["max"] += hpToAdd
                else: self.base["hp"]["max"] += hitDice
                self.base["hp"]["hitDice"]["num"] += 1

            else:
                self.base["hp"]["hitDice"]["num"] += 1
                hpToAdd = d(1,hitDice) + self.ability["modifiers"]["con"]["flat"]
                if hpToAdd > 0:
                    self.base["hp"]["max"] += hpToAdd

    def calcAttributes(self):
        modifier = {}
        for attribute in self.ability:
            if attribute != "savingThrows":
                modifier[attribute] = {}
                modifier[attribute]["flat"] = math.floor((self.ability[attribute] - 10)/2)
                modifier[attribute]["sthrow"] = math.floor((self.ability[attribute] - 10)/2)
                continue
            for throw in self.ability[attribute]:
                if self.ability[attribute][throw]:
                    modifier[throw]["sthrow"] += math.ceil(1 + 1/4 * self.base["level"])
            break
        self.ability["modifiers"] = modifier

    def calcSkillProf(self):
        for skill in self.skills:
            self.skills[skill]["modifier"] = self.skills[skill]["hasSkill"] * math.ceil(1 + 1/4 * self.base["level"])


person = Character()

person.calcAttributes()
