from Models.Order import Order
from Models.Poke import Poke
from Models.Protein import Protein
from Models.VFT import VFT
import csv


def file_reader(filename) : 
    orders=[] #list of Order objects
    
    with open(filename, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")    

        for ligne in reader:
            order_id, base, vft, sauce, protein, cookTime, trait = ligne
            vft_list = vft.split(';')

            dico_vft = {}
            for ingredient in vft_list :
                if ingredient in dico_vft.keys():
                    dico_vft[ingredient].append((0,0))
                else :
                    dico_vft[ingredient]=(0,0)

            orderedPoke = Poke(base,dico_vft,sauce,protein)


            order = Order(order_id, orderedPoke, None) #preparedPoke initialized as None at the beginning #orderTime initialized as None too until order is assigned

            orders.append(order)

    return orders


def file_reader_clients(filename) :  #creates the clients list to use in order_tab
    with open(filename, newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")

    clients =[] #list of clients with their order and their traits as dictionaries

    for ligne in reader:
        order_id, base, vft, sauce, protein, cookTime, trait = ligne
        vft_list = vft.split(';')

        client_order = {}

        client_order["trait"]= str(trait)

        client_order["order"]={}
        client_order["order"]["base"] = vft_list
        
    pass



''' TO DO : another file_reader that returns a list of dictionaries {"traits", Poke --- instance of the class Poke}'''
def file_reader_dico(filename) : 
    orders=[] #lists of dico with a trait and a Poke instance

    with open(filename, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")    
        next(reader, None)

        for ligne in reader:
            order_id, base, vft, sauce, protein, cookTime, trait = ligne
            vft_list = vft.split(';')

            dico_order = {}
            dico_order["trait"] = trait
            dico_order["poke"] = Poke(base, [VFT(vft, (0, 0)) for vft in vft_list], sauce, Protein(protein, (0, 0), int(cookTime)))

            orders.append(dico_order)

    return orders