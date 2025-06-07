import os
import tkinter as tk
from PIL import Image, ImageTk

class Icons:
    def __init__(self, canvas, folder_path="icons", size=(64, 64)):
        self.canvas = canvas
        script_dir = os.path.dirname(__file__)
        self.folder_path = os.path.join(script_dir, folder_path)

        self.size = size
        self.icons = {}

        self.load_icons()

    def load_icons(self):
        """Load all PNG images from the folder into the icons dictionary."""
        for filename in os.listdir(self.folder_path):
            if filename.endswith(".png"):
                name = os.path.splitext(filename)[0]
                img_path = os.path.join(self.folder_path, filename)
                image = Image.open(img_path).resize(self.size, Image.Resampling.LANCZOS)
                self.icons[name] = ImageTk.PhotoImage(image)

    def draw_icon(self, name, x, y):
        """Draws the icon with given name at (x, y) if it exists."""
        if name in self.icons:
            self.canvas.create_image(x, y, image=self.icons[name], anchor="center")
        else:
            print(f"Icon '{name}' not found.")



if __name__ == "main":
    root = tk.Tk()
    root.title("Food Icons from PNG")

    canvas = tk.Canvas(root, width=800, height=600, bg="white")
    canvas.pack()

    icons = Icons(canvas)  # Might need to modify the path

    # Example: place a few icons on the canvas
    positions = [
        ("avocado", 100, 100),
        ("beet",150,100),
        ("broccoli",200,100),
        ("carrot",250,100),
        ("chicken",300,100),
        ("corn",350,100),
        ("cucumber",400,100),
        ("dragon_fruit",450,100),
        ("edamame",500,100),
        ("egg",550,100),
        ("kiwi",100,200),
        ("lemon",150,200),
        ("meat",200,200),
        ("melon",250,200),
        ("mint",300,200),
        ("mushroom",350,200),
        ("onion",400,200),
        ("peas",450,200),
        ("raspberry",500,200),
        ("salad",550,200),
        ("salmon",100,300),
        ("shrimp",150,300),
        ("tofu",200,300),
        ("tomato",250,300),
        ("watermelon",300,300),
        ("music", 400, 300)
    ]

    for name, x, y in positions:
        icons.draw_icon(name, x, y)

    root.mainloop()