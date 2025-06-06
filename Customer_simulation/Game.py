from Models.Order import Order
from Models.Poke import Poke
from Serializing.filereader import file_reader
import random

class Game : 

    def __init__(self, filename, orders) :
        self.filename = filename
        self.orders = []


    def add_order_to_prepare(self) :
        orders = file_reader(self.filename)
        selected_order = random.choice(orders) #modify to have the selected order disappear from the orders list ?

        selected_order.orderTime = ((datetime.now())).time()

        self.orders.append(selected_order)


    
        