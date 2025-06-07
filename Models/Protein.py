class Protein:
    def __init__(self, name: str, cookTime: int = -1) -> None:
        self.name = name
        self.cookTime = cookTime


    def __str__(self) -> str:
        return f"Protein: {self.name} \nCooking time: {f"{self.cookTime} min" if self.cookTime != -1 else 'No cooking'}"
    

    def terminateCooking(self, cookTime: int) -> 'Protein':
        """
        Mark protein as done cooking
        """

        self.cookTime = cookTime

        return self