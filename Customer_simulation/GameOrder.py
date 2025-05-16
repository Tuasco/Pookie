from Models.Order import Order
from Models.Poke import Poke
import math
from itertools import chain


#score distribution : 100 = 40(match ingredients)+ 30(toppings position)+ 30(cooking time)


class GameOrder : #class for an active order in the game (order to evaluate and grade)

    def __init__(self, score) :
        self.score = 100


    def is_ingredients_match(self) :
        ordered = self.orderedPoke
        prepared = self.preparedPoke

        if ordered.base != prepared.base :
            self.score -= 10

        if ordered.sauce != prepared.sauce :
            self.score -= 10

        if ordered.vft.keys() != prepared.vft.keys() :
            self.score -= 20




    def check_topping_position(self, cx, cy, r_bowl, lim_dist_toppings) : #where cx and cy are the center of the container (here a bowl) and r_bowl the radius
        ordered = self.orderedPoke
        prepared = self.preparedPoke
        dico_toppings = self.preparedBowl.vft

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
        
        if not toppings_contained :
            self.score -= 10
        
        if not toppings_balanced : 
            self.score -= 20





    def check_cooking_time(self, threshold):
        
        diff_cook_time = (abs(self.orderedPoke.cookTime - self.preparedPoke.cookTime))/self.orderedPoke.cookTime #difference in percentage between the expected and the actual cooking time

        self.score -= diff_cook_time * 30






