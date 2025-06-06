from Models.Order import Order
from Models.Poke import Poke
import csv

def file_reader(filename) : 
    with open(filename, newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
    
    dico_vft = {}
    orders=[] #list of Order objects

    for ligne in reader:
        order_id, base, vft, sauce, protein, cookTime = ligne
        vft_list = vft.split(';')
                
        for ingredient in vft_list :
            if ingredient in dico_vft.keys():
                dico_vft[ingredient].append((0,0))
            else :
                dico_vft[ingredient]=(0,0)

        orderedPoke = Poke(base,dico_vft,sauce,protein,cookTime)


        order = Order(order_id, orderedPoke, None, None) #preparedPoke initialized as None at the beginning #orderTime initialized as None too until order is assigned

        orders.append(order)

    return orders
                