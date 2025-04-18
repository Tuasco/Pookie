class Poke:
    def __init__(self, base: str, vft: dict[str, list[tuple[float, float]]], sauce: str, protein: str, cookTime: int) -> None:
        self.base = base
        self.vft = vft
        self.sauce = sauce
        self.protein = protein
        self.cookTime = cookTime

    def __str__(self) -> str:
        return f"Base: {self.base}, VFT: {self.vft}, Sauce: {self.sauce}, Protein: {self.protein}, Cook Time: {self.cookTime}"
