from typing import Any


class PC:
    def __init__(self, existingPC = None) -> None:
        self.base = {
            "name":"",
            "pName":"",
            "level":"",
            "health":{
                "ap":{
                    "min":0,
                    "value":0,
                    "max":0
                },
                "hp":{
                    "min":0,
                    "value":0,
                    "max":0
                }
            },
            "deathTurns":{
                "currentTurn":0,
                "turnsTillDeath":0
            }
        }