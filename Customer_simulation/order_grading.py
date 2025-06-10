# Compares the prepared Poke to the ordered Poke and judges the "quality" of the poke

from Models.Poke import Poke
from Models.Order import Order
import math
import numpy as np
from time import time


def score(order: Order, made_poke: Poke, layout_data):
    """
    Calculates the final score and tip by calling all specialized grading functions.
    
    Args:
        order (Order): The original customer order object.
        made_poke (Poke): The poke object created by the player.
        layout_data (dict): The positional data for ingredients and sauce.
        
    Returns:
        tuple: A 5-element tuple containing (tip, wait_score, accuracy_score, cook_score, displacement_score).
    """
    # Call each grading function to get the score for each category
    grade_w = check_waiting_time(order.orderTime)
    grade_a = check_ingredients_difference(order.orderedPoke, made_poke)
    grade_c = check_cooking_time(order.orderedPoke, made_poke)
    grade_d = calculate_displacement_score(layout_data)
    
    # Calculate the tip based on the sum of all grades
    total_score = grade_w + grade_a + grade_c + grade_d
    tip = total_score / 100.0  # e.g., a total score of 250 results in a $2.50 tip
    
    # Return the final 5-element tuple in the specified order
    return (tip, grade_w, grade_a, grade_c, grade_d)


def check_waiting_time(order_timestamp):
    """
    Grades the waiting time. Score hits 0 if the wait is 240 seconds or more.
    """
    wait_penalty = (time() - order_timestamp) * (100.0 / 120.0)
    score = int(max(0, 100 - wait_penalty) * 2)
    return score if score < 100 else 100


def check_ingredients_difference(order_poke: Poke, made_poke: Poke):
    """
    Grades the accuracy of ingredients. Score hits 0 if 4 or more ingredients are wrong.
    """
    # This logic correctly counts both extra ingredients and missing ingredients.
    wrong_ingredients_count = sum([1 for vft in made_poke.vft if vft.name not in [t_vft.name for t_vft in order_poke.vft]]) \
                            + sum([1 for vft in order_poke.vft if vft.name not in [t_vft.name for t_vft in made_poke.vft]])
    
    penalty = wrong_ingredients_count * 25
    return max(0, 100 - penalty)


def check_cooking_time(order_poke: Poke, made_poke: Poke):
    """
    Grades the cooking time accuracy. Score hits 0 if the time is off by 3 units (30 seconds) or more and the protein is not the one asked for.
    """
    if made_poke.protein is None:
        return 0

    order_cook_time = order_poke.protein.cookTime if order_poke.protein.cookTime != -1 else 0
    made_cook_time = made_poke.protein.cookTime if made_poke.protein.cookTime != -1 else 0
    
    return (50 if order_poke.protein.name == made_poke.protein.name else 0) + max(0, 50 - abs(order_cook_time - made_cook_time) * 17)


def calculate_displacement_score(layout_data):
    """
    The "Judge": Scores the poke's layout based on the collected data.
    Returns a score from 0 to 100.
    """
    if not layout_data:
        return 50 # Default score if there's no data

    # --- Ingredient Score: How evenly are toppings spread? ---
    ingredient_positions = layout_data["ingredient_positions"]
    bowl_center = layout_data["bowl_center"]
        
    if len(ingredient_positions) > 1:
        distances = [math.hypot(pos[0] - bowl_center[0], pos[1] - bowl_center[1]) for pos in ingredient_positions]
        distance_std_dev = np.std(distances)
        ingredient_score = max(0, 100 - distance_std_dev * 1.5)
    else:
        ingredient_score = 50 # Score if 0 or 1 ingredient

    # --- Sauce Score: How evenly is the sauce distributed? ---
    sauce_path = layout_data["sauce_path"]
        
    if len(sauce_path) > 10:
        x_coords = [p[0] for p in sauce_path]
        y_coords = [p[1] for p in sauce_path]
        x_std_dev = np.std(x_coords)
        y_std_dev = np.std(y_coords)
            
        if min(x_std_dev, y_std_dev) > 0:
            spread_ratio = max(x_std_dev, y_std_dev) / min(x_std_dev, y_std_dev)
        else:
            spread_ratio = 5
                
        sauce_score = max(0, 100 - (spread_ratio - 1) * 20)
    else:
        sauce_score = 50 # Score for little or no sauce

    final_score = (ingredient_score + sauce_score) / 2
    return int(final_score)