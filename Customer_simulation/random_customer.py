from Models.Order import Order
from Models.Poke import Poke
from Serializing.filereader import file_reader
import random

def pick_random(filename) :

    orders = file_reader(filename)
    selected_order = random.choice(orders)

    return selected_order
