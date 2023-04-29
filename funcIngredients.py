import random
import numpy as np
import ingredientArrays as arr

values = ["+1","+2","+3","+5","*2","^2","-1","-2"]
values_chances = [1/5,1/5,1/5,2/25,2/25,2/25,2/25,2/25]

class ingredient:
    def __init__(self, name, value) -> None:
        self.name = name
        self.value = value

def chances(arr):
    result = np.ones(len(arr)-1)
    chance = 0.5/(len(arr)-1)
    result = result*chance
    result = np.append(result, 0.5)
    return result

def choose_randomly(arr):
    return random.choices(arr, weights = chances(arr))[0]

def genrate_items(n):
    items = {
        "item_list" : []
    }
    for i in range(n):
        size = choose_randomly(arr.sizes)
        color = choose_randomly(arr.colors)
        pattern = choose_randomly(arr.patterns)
        special_adj = choose_randomly(arr.special_adjs)
        noun = random.choice(arr.nouns)

        value = random.choices(values, weights=values_chances)[0]

        items["item_list"].append(ingredient(f'{size}{color}{pattern}{special_adj}{noun}', value).__dict__)
    return items

