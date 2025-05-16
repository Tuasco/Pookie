class VFT:
    def __init__(self, name: str, position: tuple[float, float]) -> None:
        self.name = name
        self.position = position

    def __str__(self) -> str:
        return f"VFT Name: {self.name}, Position: {self.position}"