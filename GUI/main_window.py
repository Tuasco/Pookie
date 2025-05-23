import tkinter as tk 
from Tabs import difficulty_tab, order_tab, base_tab, veg_fruit_tab, protein_tab, extras_sauces_tab, serve_tab

tab_classes=[difficulty_tab.Game_difficulty_Tab, 
             order_tab.Order_Tab, 
             base_tab.Base_Tab, 
             veg_fruit_tab.Veg_Fruit_Tab, 
             protein_tab.Protein_Tab, 
             extras_sauces_tab.Extras_Sauces_Tab, 
             serve_tab.Serve_Tab]

class PookieGUI(tk.Tk):
    """
    Principal class for the Pookie game GUI.
    Inherits from tkinter.Tk to create the main window.
    """
    def __init__(self):
        super().__init__()
        self.title("Pookie")
        self.geometry("800x600")   
        
        # Top navigation bar
        nav_bar = tk.Frame(self, bg="lightgray")
        nav_bar.pack(side="top", fill="x")

        for page in tab_classes:
            b = tk.Button(nav_bar, text=page.__name__.replace("_"," ")[:-4], command=lambda n=page.__name__: self.show_frame(n))
            b.pack(side="left", padx=2, pady=4)

        # Main layout: left = changing frame; right = order list
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True)

        # Left dynamic content area
        self.container = tk.Frame(main_frame, bg="white")
        self.container.pack(side="left", fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.create_order_panel(main_frame)

        self.pages= {}
        
        for page in tab_classes:
            # Dynamically create pages and store them in the pages dictionary
            page_name = page.__name__
            frame = page(parent=self.container, controller=self)
            self.pages[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.show_frame("Game_difficulty_Tab")
        
    def show_frame(self, page_name):
        """
        Show a frame for the given page name.
        """
        frame = self.pages[page_name]
        frame.tkraise()
        
    
    def select_order(self, order_id, widget):
        # Reset visuals for all
        for _, lbl in self.order_receipts:
            lbl.config(bg="white")

        # Highlight selected
        widget.config(bg="#cceeff")  # light blue

        # Save selected
        self.selected_order = order_id
        print(f"Selected: {order_id}")


    def create_order_panel(self, parent):
        right_panel = tk.Frame(parent, width=200, bg="lightblue")
        right_panel.pack(side="right", fill="y")

        tk.Label(right_panel, text="Orders", font=("Helvetica", 14, "bold")).pack(pady=5)
        
        self.selected_order = None  # to store the selected receipt
        self.order_receipts = []    # to keep track of all receipt widgets


        canvas = tk.Canvas(right_panel, borderwidth=0, width=200)
        scrollbar = tk.Scrollbar(right_panel, orient="vertical", command=canvas.yview) #canvas.yview tells the scrollbar to scroll the canvas vertically
        self.order_frame = tk.Frame(canvas)

        self.order_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.order_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Example dummy orders
        for i in range(5):
            order_id = f"Order #{1000+i}"
            label = tk.Label(self.order_frame, text=f"{order_id}\n- base\n- topping\n- protein",
                            bg="white", font=("Courier", 10), bd=1, relief="solid", pady=5)
            label.pack(pady=4, fill="x", padx=5)

            # Store reference to the label
            self.order_receipts.append((order_id, label))

            # Add click binding
            label.bind("<Button-1>", lambda e, oid=order_id, lbl=label: self.select_order(oid, lbl))


if __name__=="__main__":
    app = PookieGUI()
    app.mainloop()