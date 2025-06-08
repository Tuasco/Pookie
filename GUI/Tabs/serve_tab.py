# In serve_tab.py

import tkinter as tk

bg_color = "seashell"  # Background color for the tab

class Serve_Tab(tk.Frame):
    """Class representing the serve tab in the Pookie GUI."""

    def __init__(self, parent, controller):
        super().__init__(parent, bg=bg_color)
        self.controller = controller
        
        label = tk.Label(self, text="Serve Your Dish", font=self.controller.font_title, bg=bg_color)
        label.pack(pady=self.controller.padding)
    
        # The button command points back to the controller's function
        self.serve_button = tk.Button(self, text="Serve", font=self.controller.font_title, command=self.controller.serve_poke, bg="lightgreen", fg="white", borderwidth=0, highlightthickness=0, padx=5, pady=5, cursor="hand2")
        self.serve_button.pack(pady=self.controller.padding)

        # --- Feedback Stars Setup ---
        self.feedback_frame = tk.Frame(self, bg=bg_color)
        self.feedback_frame.pack(pady=self.controller.padding * 2)

        self.star_canvases = []
        star_info = [
            ("Waiting Time", "green"),
            ("Accuracy", "gold"),
            ("Cooking", "darkorange"),
            ("Displacement", "deepskyblue")
        ]

        # Create a labeled canvas for each star
        for text, color in star_info:
            container = tk.Frame(self.feedback_frame, bg=bg_color)
            
            # Label for the category
            cat_label = tk.Label(container, text=text, font=self.controller.font_label, bg=bg_color)
            cat_label.pack()

            # Canvas for drawing the star
            canvas = tk.Canvas(container, width=100, height=100, bg=bg_color, highlightthickness=0)
            canvas.pack()
            
            self.star_canvases.append((container, canvas, color))


    def display_serving_feedback(self, tip, grade_wait, grade_accuracy, grade_cooking, grade_displacement):
        """Receives grades (0-100) and displays the feedback stars."""
        grades = [grade_wait, grade_accuracy, grade_cooking, grade_displacement]

        # Loop through each canvas and its corresponding grade
        for i, (container, canvas, color) in enumerate(self.star_canvases):
            # Make the container visible
            container.pack(side="left", padx=self.controller.padding)
            self._draw_filled_star(canvas, grades[i], color)

        self.tip_label = tk.Label(self, text=f"Tip: ${tip:.2f}", font=self.controller.font_title, fg="green")
        self.tip_label.pack()

        # Schedule the stars to disappear after 3 seconds (3000ms)
        self.after(3000, self.hide_feedback)


    def _draw_filled_star(self, canvas, percentage, color):
        """Draws a star filled to a specific percentage using a masking technique."""
        canvas.delete("all")

        # Draw star
        points = [
            50, 0, 61, 35, 98, 35, 68, 57, 79, 91,
            50, 70, 21, 91, 32, 57, 2, 35, 39, 35
        ]
        canvas.create_polygon(points, fill=color, outline="")
                
        # Create mask
        x0, y0, x1, y1 = canvas.bbox(canvas.create_polygon(points, fill=""))
        total_height = y1 - y0
        safe_percentage = max(0, min(100, percentage))       
        mask_height = total_height * (100 - safe_percentage) / 100.0
        bg_color = canvas.cget("bg")
        if mask_height > 0:
            canvas.create_rectangle(x0, y0, x1, y0 + mask_height, fill=bg_color, outline="")

        # Draw outline
        canvas.create_polygon(points, fill="", outline='grey', width=2)


    def hide_feedback(self):
        """Hides the feedback containers."""
        self.tip_label.destroy()
        for container, canvas, color in self.star_canvases:
            container.pack_forget()
            canvas.delete("all")