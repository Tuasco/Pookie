from Models.Poke import Poke
from Models.Protein import Protein
from Models.VFT import VFT
import csv


def file_reader_dico(filename) : 
    """ TO DO : another file_reader that returns a list of dictionaries {"traits", Poke --- instance of the class Poke}"""
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