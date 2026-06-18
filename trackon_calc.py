import tkinter as tk
from tkinter import ttk, messagebox
import math

class TrackonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trackon Rate Calculator")
        self.root.geometry("350x480")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f2f5")
        
        # Colors
        self.c_prime = "#c2185b"
        self.c_std = "#2e7d32"
        self.c_dark = "#1a237e"

        self.company = tk.StringVar(value="prime")
        
        self.create_widgets()

    def create_widgets(self):
        # Header
        header = tk.Label(self.root, text="📦 Trackon Calculator", font=("Segoe UI", 18, "bold"), bg="#f0f2f5", fg=self.c_dark)
        header.pack(pady=(15, 10))

        # Company Toggle
        toggle_frame = tk.Frame(self.root, bg="#f0f2f5")
        toggle_frame.pack(pady=5)

        self.btn_prime = tk.Radiobutton(toggle_frame, text="🔴 Prime", variable=self.company, value="prime",
                                        indicatoron=0, width=10, bg="#fce4ec", fg="black",
                                        activebackground=self.c_prime, activeforeground="white",
                                        selectcolor=self.c_prime, font=("Arial", 11, "bold"))
        self.btn_std = tk.Radiobutton(toggle_frame, text="🟢 Standard", variable=self.company, value="standard",
                                      indicatoron=0, width=10, bg="#e8f5e9", fg="black",
                                      activebackground=self.c_std, activeforeground="white",
                                      selectcolor=self.c_std, font=("Arial", 11, "bold"))
        self.btn_prime.pack(side="left", padx=5)
        self.btn_std.pack(side="left", padx=5)

        # Service Type
        tk.Label(self.root, text="Service:", bg="#f0f2f5", font=("Arial", 12, "bold")).pack(pady=(15, 5))
        self.service = ttk.Combobox(self.root, state="readonly", font=("Arial", 11))
        self.service['values'] = ('DOX', 'Surface (Non-DOX)', 'Smart Express')
        self.service.current(0)
        self.service.pack(fill="x", padx=30)

        # Zone
        tk.Label(self.root, text="Zone:", bg="#f0f2f5", font=("Arial", 12, "bold")).pack(pady=(15, 5))
        self.zone = ttk.Combobox(self.root, state="readonly", font=("Arial", 11))
        self.zone['values'] = ('MP', 'ROI', 'NE')
        self.zone.current(0)
        self.zone.pack(fill="x", padx=30)

        # Weight
        tk.Label(self.root, text="Weight (Kg):", bg="#f0f2f5", font=("Arial", 12, "bold")).pack(pady=(15, 5))
        self.entry_wt = tk.Entry(self.root, font=("Arial", 14), justify="center")
        self.entry_wt.pack(fill="x", padx=30, ipady=5)

        # Button
        calc_btn = tk.Button(self.root, text="💰 CALCULATE", command=self.calculate,
                             bg=self.c_dark, fg="white", font=("Arial", 14, "bold"),
                             activebackground="#0d47a1", cursor="hand2")
        calc_btn.pack(fill="x", padx=30, pady=20, ipady=5)

        # Result Area
        self.res_frame = tk.Frame(self.root, bg="#fff", relief="solid", bd=1)
        self.res_frame.pack(fill="x", padx=30, pady=5)
        self.lbl_amt = tk.Label(self.res_frame, text="₹0", font=("Segoe UI", 28, "bold"), bg="#fff", fg=self.c_dark)
        self.lbl_amt.pack(pady=10)
        self.lbl_detail = tk.Label(self.res_frame, text="Enter weight to calculate", font=("Arial", 10), bg="#fff", fg="#666")
        self.lbl_detail.pack(pady=(0, 10))

    def calculate(self):
        try:
            w = float(self.entry_wt.get())
            if w <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter valid weight!")
            return

        comp = self.company.get()
        zone = self.zone.get().lower()
        svc = self.service.get()
        amt = 0
        detail = ""
        color = self.c_dark

        try:
            # ==========================
            # PRIME LOGIC
            # ==========================
            if comp == 'prime':
                if 'DOX' in svc:
                    # Prime DOX: ₹250/300/350 per 500gm
                    rates = {'mp': 250, 'roi': 300, 'ne': 350}
                    slabs = math.ceil(w / 0.5)
                    amt = slabs * rates[zone]
                    detail = f"DOX: {slabs} slab(s) × ₹{rates[zone]}"
                    color = self.c_prime
                else:
                    # Surface / Smart not defined for Prime in our chat logic yet
                    messagebox.showinfo("Info", "Prime sirf DOX service ke liye setup hai abhi.")
                    return

            # ==========================
            # STANDARD LOGIC
            # ==========================
            else:
                if 'DOX' in svc:
                    # Standard DOX: ₹100/260/450 Flat for 0-1kg
                    base_rates = {'mp': 100, 'roi': 260, 'ne': 450}
                    
                    if w <= 1:
                        amt = base_rates[zone]
                        detail = f"DOX: Flat (0-1kg)"
                    else:
                        # For > 1kg (Assumption: Standard follows typical courier logic or stays flat if not defined)
                        # Based on user input "standard me rate galat... rate pura 1kg ka lagega"
                        # Assuming >1kg adds per 500gm extra (approximate addl rates based on ratio or fixed)
                        # Let's use standard addl logic: usually ~80% of base per 500gm
                        extra_wt = w - 1
                        extra_slabs = math.ceil(extra_wt / 0.5)
                        
                        # Addl rates estimation (since not explicitly given, using 70-80% of base)
                        addl_rates = {'mp': 80, 'roi': 200, 'ne': 350} 
                        
                        amt = base_rates[zone] + (extra_slabs * addl_rates[zone])
                        detail = f"DOX: 1kg Flat + {extra_slabs} addl slab(s)"

                    color = self.c_std

                elif 'Surface' in svc:
                    cw = math.ceil(w) # Round up weight
                    rate = 0
                    slab_detail = ""
                    
                    if zone == 'mp':
                        if cw <= 5: rate, slab_detail = 100, "0-5kg"
                        elif cw <= 10: rate, slab_detail = 85, "5-10kg"
                        else: raise ValueError("MP Surface > 10kg")
                        
                    elif zone == 'roi':
                        if cw <= 3: rate, slab_detail = 150, "0-3kg"
                        elif cw <= 7: rate, slab_detail = 100, "3-7kg"
                        elif cw <= 10: rate, slab_detail = 90, "7-10kg"
                        else: raise ValueError("ROI Surface > 10kg")
                        
                    elif zone == 'ne':
                        if cw <= 3: rate, slab_detail = 185, "0-3kg"
                        elif cw <= 7: rate, slab_detail = 125, "3-7kg"
                        elif cw <= 10: rate, slab_detail = 115, "7-10kg"
                        else: raise ValueError("NE Surface > 10kg")

                    amt = rate * cw
                    detail = f"Surface: ₹{rate}/kg ({slab_detail}) × {cw}kg"

                elif 'Smart' in svc:
                    cw = math.ceil(w)
                    rates = {'mp': 81, 'roi': 104, 'ne': 126}
                    amt = rates[zone] * cw
                    detail = f"Smart: ₹{rates[zone]}/kg × {cw}kg"

            # Update UI
            self.lbl_amt.config(text=f"₹{amt}", fg=color)
            self.lbl_detail.config(text=detail)

        except ValueError as e:
            messagebox.showwarning("Limit Exceeded", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = TrackonApp(root)
    root.mainloop()
