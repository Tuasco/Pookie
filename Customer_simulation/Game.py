from Models.Order import Order
from Models.Poke import Poke
from Serializing.filereader import file_reader
import random


class Game : 

    def __init__(self, filename, orders, score) :
        self.filename = filename
        self.orders = []
        self.score = 0


    def add_order_to_prepare(self, new_order) :
        orders = file_reader(self.filename)
        selected_order = random.choice(orders) #modify to have the selected 
        