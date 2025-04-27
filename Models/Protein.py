class Protein:
    def __init__(self, name: str, cookTime: int = -1):
        self.name = name
        self.cookTime = cookTime

    def __str__(self) -> str:
        return f"Protein: {self.name}, Cook Time: {self.cookTime}"