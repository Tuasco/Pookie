import tkinter as tk

class OrderDetailWindow(tk.Toplevel):
    """
    A pop-up window (Toplevel) that displays the formatted
    details of a given poke order.
    """
    def __init__(self, parent, poke_object):
        super().__init__(parent)
        self.title("Order Details")

        # --- Window Size and Position ---
        win_width = 350
        win_height = 300
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (win_width // 2)
        y = (screen_height // 2) - (win_height // 2)
        self.geometry(f'{win_width}x{win_height}+{x}+{y}')
        self.configure(bg="seashell")
        self.resizable(False, False) # Make window not resizable

        # --- Format and Display Order ---
        formatted_text = self._format_poke_for_display(poke_object)
        
        # Use a Text widget for better formatting and scrolling if needed
        text_widget = tk.Text(self, font=("Courier", 11), wrap=tk.WORD, bg="seashell", bd=0, highlightthickness=0)
        text_widget.pack(padx=20, pady=20, fill="both", expand=True)
        text_widget.insert(tk.END, formatted_text)
        text_widget.configure(state='disabled') # Make it read-only

        close_button = tk.Button(self, text="Close", font=("Helvetica", 10, "bold"), command=self.destroy)
        close_button.pack(pady=10)

        # Make the window modal
        self.transient(parent)
        self.grab_set()
        parent.wait_window(self)


    def _format_poke_for_display(self, poke):
        """Takes a Poke object and returns a nicely formatted string."""
        if not poke:
            return "No order details to display."
        
        details = "--- ORDER DETAILS ---\n\n"
        
        if poke.base:
            details += f"Base: {poke.base.capitalize()}\n\n"
        
        if poke.protein and poke.protein.name:
            cook_time_str = f"(Cook for {poke.protein.cookTime}s)" if poke.protein.cookTime and int(poke.protein.cookTime) > 0 else "(No cooking)"
            details += f"Protein: {poke.protein.name.capitalize()} {cook_time_str}\n\n"

        if poke.sauce:
            sauce_name = poke.sauce.name if hasattr(poke.sauce, 'name') else poke.sauce
            details += f"Sauce: {sauce_name.capitalize()}\n\n"

        if poke.vft:
            details += "Toppings:\n"
            # This logic handles both lists of strings (from CSV) and lists of VFT objects (from player)
            vft_list = poke.vft
            if vft_list and not isinstance(vft_list[0], str):
                vft_list = [item.name for item in vft_list]
            
            for item in vft_list:
                details += f"  - {item.capitalize()}\n"
        
        return details