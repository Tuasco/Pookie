from Protein import Protein
from time import time
from math import round

class Fire:
    def __init__(self) -> None:
        self.protein = None
        self.startTime = None


    def __str__(self) -> str:
        return f"Fire cooking {self.protein}" if self.protein is not None else "Fire is empty"
    

    def add_protein(self, protein: Protein) -> 'Fire':
        """
        Add protein to fire
        """

        self.protein = protein
        self.startTime = time()

        return self
    

    def remove_protein(self) -> int:
        """
        Remove protein from fire and mark it as cooked
        """

        if self.protein is None:
            return -1
        
        cookTime = time() - self.startTime
        self.protein.terminateCooking(cookTime)

        self.protein = None
        self.startTime = None

        return round(cookTime)