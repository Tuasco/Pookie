from Models.Poke import Poke
from time import time

class Order:
    def __init__(self, order_id: int, orderedPoke: Poke, orderTime: time) -> None:
        self.order_id = order_id
        self.orderedPoke = orderedPoke
        self.preparedPoke = Poke()
        self.orderTime = orderTime


    def __str__(self) -> str:
        return f"Order ID: {self.order_id}, Poke: {self.orderedPoke}, Order Time: {self.orderTime}"