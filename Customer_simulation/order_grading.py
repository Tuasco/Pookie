#compares the prepared Poke to the ordered Poke and jugdes que "quality" of the poke

'''
To check :
- if all the ingredients are there
- if cookingTime matches
- quality of the presentation : checks if toppings are in the bowl if they're well arranged in the bowl
'''
'''..............................................................................................'''

from Models.Order import Order
from Models.Poke import Poke
import math
from itertools import chain


def is_ingredients_match(order) :
    
    ingredients_complete = True
    ordered = order.orderedPoke
    prepared = order.preparedPoke

    if ordered.base != prepared.base :
        ingredients_complete = False

    if ordered.sauce != prepared.sauce :
        ingredients_complete = False

    if ordered.sauce != prepared.sauce :
        ingredients_complete = False

    return ingredients_complete


def check_topping_position(order, cx, cy, r_bowl, lim_dist_toppings) : #where cx and cy are the center of the container (here a bowl) and r_bowl the radius
    ordered = order.orderedPoke
    prepared = order.preparedPoke
    dico_toppings = order.preparedBowl.vft

    #check if all toppings IN the bowl
    toppings_contained = True
    index=0

    while index < len(dico_toppings) and toppings_contained :
        x,y = dico_toppings[dico_toppings.keys()[index]]
        toppings_contained = (x - cx)**2 + (y - cy)**2 <= r_bowl**2 #condition for coordinates of a point in a circle
        index+=1
    

    # checks if toppings well spread in the bowl : 
    # we'll compare the average distance between each pair of ingredients
    # if they're relatively similar, the ingredients are evenly spread (we'll compare to a threshold lim_dist_toppings adapted to the size of the bowl)
    toppings_balanced = True
    total_dist=0
    pair_count=0
    ingredients_coord_from_dico = list(dico_toppings.values())
    list_coord_toppings = list(chain(*[item if isinstance(item, tuple) else (item,) for item in ingredients_coord_from_dico]))
    
    for i in range(len(list_coord_toppings)):
        for j in range(i + 1, len(list_coord_toppings)):
            total_dist += math.sqrt((list_coord_toppings[j][0] - list_coord_toppings[i][0])**2 + (list_coord_toppings[j][1] - list_coord_toppings[i][1])**2)
            pair_count += 1

    toppings_balanced = total_dist/pair_count <= lim_dist_toppings


    return toppings_contained, toppings_balanced


def check_cooking_time(order, threshold):
    well_cooked = True
    diff_cook_time = abs(order.orderedPoke.cookTime - order.preparedPoke.cookTime)

    if diff_cook_time > threshold :
        well_cooked = False

    return well_cooked


def score(order) : 
    '''calculates score based on the previous functions'''
 

