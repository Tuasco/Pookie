from VFT import VFT
from Protein import Protein

class Poke:
    def __init__(self, base: str = None, vft: list[VFT] = [], sauce: str = None, protein: Protein = None) -> None:
        self.base = base
        self.vft = vft
        self.sauce = sauce
        self.protein = protein


    def __str__(self) -> str:
        return f"Base: {self.base}, VFT: {self.vft}, Sauce: {self.sauce}, Protein: {self.protein}, Cook Time: {self.cookTime}"
    

    def add_base(self, base: str):
        """
        Add a certain base by name at a certain position
        """

        if (base is None):
            self.base = base

        return self


    def add_vft(self, vft: VFT):
        """
        Add a certain VFT (Vegetable, Fruit or Topping) by name at a certain position
        """

        if (vft in self.vft):
            self.vft.append(vft)
        else:
            self.vft = [vft]

        return self
    

    def remove_vft(self, vft: VFT):
        """
        Remove a certain VFT (Vegetable, Fruit or Topping) by name at a certain position
        """

        if (vft in self.vft):
            self.vft.remove(vft)

        return self
    

    def add_sauce(self, sauce: str):
        """
        Add a certain sauce by name at a certain position
        """

        if (sauce is None):
            self.sauce = sauce

        return self
    

    def add_protein(self, protein: Protein):
        """
        Add a certain protein by name at a certain position
        """

        if (protein is None):
            self.protein = protein

        return self
    

    def compare(self, poke: 'Poke'):
        """
        Compare two pokes and give score
        """
        pass
