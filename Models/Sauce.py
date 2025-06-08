import math

class Sauce:
    def __init__(self, name: str, path: list[tuple[int, int]]) -> None:
        self.name = name
        self.path = path
        # The surface is calculated as the total length of the drawn path
        self.surface = self._calculate_surface()

    def _calculate_surface(self) -> int:
        """Calculates the length of the path drawn by the user."""
        distance = 0
        # Sum the distance between each consecutive point in the path
        for i in range(len(self.path) - 1):
            p1 = self.path[i]
            p2 = self.path[i+1]
            distance += math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
        return int(distance)

    def __str__(self) -> str:
        return f"Sauce Name: {self.name}, Surface: {self.surface}"