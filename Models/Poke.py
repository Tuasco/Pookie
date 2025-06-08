from Models.VFT import VFT
from Models.Protein import Protein
from Models.Sauce import Sauce

class Poke:
    def __init__(self, base: str = None, vft: list = None, sauce: Sauce = None, protein: Protein = None) -> None:
        self.base = base
        # If vft is None, create a new empty list. This ensures each Poke has its own list.
        self.vft = [] if vft is None else vft
        self.sauce = sauce
        self.protein = protein


    def __str__(self) -> str:
        beautified_vft = ""
        for ingredient in self.vft:
            beautified_vft += f"{ingredient}, "
        return f"Base: {self.base} \nVFT: {beautified_vft[:-2]} \nSauce: {self.sauce} \nProtein: {self.protein}"
    

    def add_base(self, base: str) -> 'Poke':
        """
        Add a certain base by name at a certain position
        """

        if (base is None):
            self.base = base

        return self


    def add_vft(self, vft: VFT) -> 'Poke':
        """
        Add a certain VFT (Vegetable, Fruit or Topping) by name at a certain position
        """

        if (vft in self.vft):
            self.vft.append(vft)
        else:
            self.vft = [vft]

        return self
    

    def remove_vft(self, vft: VFT) -> 'Poke':
        """
        Remove a certain VFT (Vegetable, Fruit or Topping) by name at a certain position
        """

        if (vft in self.vft):
            self.vft.remove(vft)

        return self
    

    def add_sauce(self, sauce: Sauce) -> 'Poke':
        """
        Add a certain sauce by name at a certain position
        """

        if (sauce is None):
            self.sauce = sauce

        return self
    

    def add_protein(self, protein: Protein) -> 'Poke':
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