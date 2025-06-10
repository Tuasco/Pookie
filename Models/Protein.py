class Protein:
    def __init__(self, name: str, position: tuple[float, float], cookTime: int = -1) -> None:
        self.name = name
        self.cookTime = cookTime
        self.position = position


    def __str__(self) -> str:
        return f"Prot: {self.name} \n- Time: {f"{self.cookTime} min" if self.cookTime != -1 else 'raw'}"
    

    def terminateCooking(self, cookTime: int) -> 'Protein':
        """
        Mark protein as done cooking
        """

        self.cookTime = cookTime

        return self