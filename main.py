import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class CzechTrainSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Czech Train Information System")
        self.root.geometry("1000x700")
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
        self.style.configure("TButton", font=("Arial", 10), padding=5)
        self.style.configure("Header.TLabel", font=("Arial", 14, "bold"))
        self.style.configure("Treeview", font=("Arial", 9), rowheight=25)
        self.style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        self.user_role = None  
        self.show_role_selection()
    
    def show_role_selection(self):
        self.clear_window()
        
        role_frame = ttk.Frame(self.root, padding=20)
        role_frame.pack(expand=True)
        
        ttk.Label(role_frame, text="Select Your Role", style="Header.TLabel").pack(pady=20)
        
        ttk.Button(role_frame, text="Administrator", 
                  command=lambda: self.set_role("admin")).pack(fill=tk.X, pady=5)
        ttk.Button(role_frame, text="Station Staff", 
                  command=lambda: self.set_role("staff")).pack(fill=tk.X, pady=5)
        ttk.Button(role_frame, text="Passenger", 
                  command=lambda: self.set_role("user")).pack(fill=tk.X, pady=5)
    
    def set_role(self, role):
        self.user_role = role
        self.create_main_interface()
        
        roles = {
            "admin": "Administrator",
            "staff": "Station Staff",
            "user": "Passenger"
        }
        messagebox.showinfo("Welcome", f"Logged in as {roles[role]}")
    
    def create_main_interface(self):

        self.clear_window()
        
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(header_frame, text="Czech Train Information System", 
                 style="Header.TLabel").pack(side=tk.LEFT)
        
        switch_btn = ttk.Button(header_frame, text="Switch Role", command=self.show_role_selection)
        switch_btn.pack(side=tk.RIGHT)
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        self.create_timetable_tab()
        self.create_real_time_tab()
        
        if self.user_role == "user":
            self.create_user_account_tab()
        elif self.user_role == "staff":
            self.create_staff_tab()
        elif self.user_role == "admin":
            self.create_admin_tab()
            self.create_staff_tab()
            self.create_report_tab()
    
    def create_timetable_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Timetable Search")
        
        search_frame = ttk.LabelFrame(tab, text="Search Trains", padding=10)
        search_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(search_frame, text="From:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.from_entry = ttk.Entry(search_frame, width=30)
        self.from_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(search_frame, text="To:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.to_entry = ttk.Entry(search_frame, width=30)
        self.to_entry.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(search_frame, text="Date:").grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)
        self.date_entry = ttk.Entry(search_frame, width=15)
        self.date_entry.grid(row=0, column=5, padx=5, pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))
        
        ttk.Label(search_frame, text="Time:").grid(row=0, column=6, padx=5, pady=5, sticky=tk.W)
        self.time_entry = ttk.Entry(search_frame, width=10)
        self.time_entry.grid(row=0, column=7, padx=5, pady=5)
        self.time_entry.insert(0, datetime.now().strftime("%H:%M"))
        
        search_btn = ttk.Button(search_frame, text="Search", command=self.search_trains)
        search_btn.grid(row=0, column=8, padx=10, pady=5)
        
        results_frame = ttk.Frame(tab)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.tree = ttk.Treeview(results_frame, columns=("departure", "arrival", "train", "duration", "changes", "status"), 
                                selectmode="browse")
        
        self.tree.heading("#0", text="ID")
        self.tree.heading("departure", text="Departure")
        self.tree.heading("arrival", text="Arrival")
        self.tree.heading("train", text="Train")
        self.tree.heading("duration", text="Duration")
        self.tree.heading("changes", text="Changes")
        self.tree.heading("status", text="Status")
        
        self.tree.column("#0", width=50, stretch=tk.NO)
        self.tree.column("departure", width=120, anchor=tk.CENTER)
        self.tree.column("arrival", width=120, anchor=tk.CENTER)
        self.tree.column("train", width=100, anchor=tk.CENTER)
        self.tree.column("duration", width=80, anchor=tk.CENTER)
        self.tree.column("changes", width=60, anchor=tk.CENTER)
        self.tree.column("status", width=100, anchor=tk.CENTER)
        
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        

        btn_frame = ttk.Frame(tab)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(btn_frame, text="Buy Ticket", command=self.buy_ticket).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Show Route", command=self.show_route).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_data).pack(side=tk.LEFT, padx=5)
        

        self.insert_sample_data()
    
    def create_real_time_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Real-time Information")
        

        rt_frame = ttk.LabelFrame(tab, text="Train Status", padding=10)
        rt_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        

        input_frame = ttk.Frame(rt_frame)
        input_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(input_frame, text="Train Number:").pack(side=tk.LEFT, padx=5)
        self.train_num_entry = ttk.Entry(input_frame, width=15)
        self.train_num_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(input_frame, text="Check Status", command=self.check_train_status).pack(side=tk.LEFT, padx=10)
        
        self.status_text = tk.Text(rt_frame, height=10, wrap=tk.WORD, font=("Arial", 9))
        self.status_text.pack(fill=tk.BOTH, expand=True)

        self.status_text.insert(tk.END, "Enter a train number and click 'Check Status' to view current information.")
    
    def create_user_account_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="My Account")
        
        account_frame = ttk.LabelFrame(tab, text="Account Details", padding=10)
        account_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        

        info = """
        Passenger Name: Jan Novák
        Email: jan.novak@example.com
        Phone: +420 123 456 789
        Registered since: 15/03/2022
        
        Favorites:
        - Praha hl.n. to Brno hl.n.
        - Praha hl.n. to Plzeň hl.n.
        
        Upcoming trips:
        - EC 173, Praha to Brno, 15/07/2023
        """
        
        ttk.Label(account_frame, text=info.strip(), justify=tk.LEFT).pack(anchor=tk.W)
        
        btn_frame = ttk.Frame(account_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(btn_frame, text="Edit Profile", command=self.edit_profile).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="View Tickets", command=self.view_tickets).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Payment Methods", command=self.payment_methods).pack(side=tk.LEFT, padx=5)
    
    def create_staff_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Station Operations")
        
        staff_frame = ttk.LabelFrame(tab, text="Station Management", padding=10)
        staff_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        

        ttk.Label(staff_frame, text="Current Station:").pack(anchor=tk.W)
        self.station_entry = ttk.Entry(staff_frame, width=30)
        self.station_entry.insert(0, "Praha hl.n.")
        self.station_entry.pack(fill=tk.X, pady=5)
        

        ttk.Label(staff_frame, text="Station Announcement:").pack(anchor=tk.W, pady=(10,0))
        self.announcement_entry = ttk.Entry(staff_frame)
        self.announcement_entry.pack(fill=tk.X, pady=5)
        
        ttk.Button(staff_frame, text="Make Announcement", 
                  command=self.make_announcement).pack(pady=5)
        

        ttk.Label(staff_frame, text="Update Train Status:").pack(anchor=tk.W, pady=(10,0))
        
        delay_frame = ttk.Frame(staff_frame)
        delay_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(delay_frame, text="Train Number:").pack(side=tk.LEFT)
        self.delay_train_entry = ttk.Entry(delay_frame, width=10)
        self.delay_train_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(delay_frame, text="Delay (min):").pack(side=tk.LEFT)
        self.delay_min_entry = ttk.Entry(delay_frame, width=5)
        self.delay_min_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(delay_frame, text="Update", command=self.update_delay).pack(side=tk.LEFT, padx=5)
    
    def create_admin_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Administration")
        
        admin_frame = ttk.LabelFrame(tab, text="System Administration", padding=10)
        admin_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        ttk.Label(admin_frame, text="User Management", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        
        user_frame = ttk.Frame(admin_frame)
        user_frame.pack(fill=tk.X, pady=5)
        
        self.user_tree = ttk.Treeview(user_frame, columns=("name", "email", "role"), height=5)
        self.user_tree.heading("#0", text="ID")
        self.user_tree.heading("name", text="Name")
        self.user_tree.heading("email", text="Email")
        self.user_tree.heading("role", text="Role")
        
        self.user_tree.column("#0", width=50)
        self.user_tree.column("name", width=150)
        self.user_tree.column("email", width=200)
        self.user_tree.column("role", width=100)
        
        self.user_tree.pack(fill=tk.X)
        
        users = [
            ("1", "Admin User", "admin@cd.cz", "Administrator"),
            ("2", "Station Manager", "manager@cd.cz", "Staff"),
            ("3", "Jan Novák", "passenger@example.com", "Passenger")
        ]
        
        for user in users:
            self.user_tree.insert("", tk.END, text=user[0], values=user[1:])
        
        btn_frame = ttk.Frame(admin_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="Add User", command=self.add_user).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Edit User", command=self.edit_user).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete User", command=self.delete_user).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(admin_frame, text="Schedule Management", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10,0))
        
        schedule_frame = ttk.Frame(admin_frame)
        schedule_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(schedule_frame, text="Import Schedule", command=self.import_schedule).pack(side=tk.LEFT, padx=5)
        ttk.Button(schedule_frame, text="Export Schedule", command=self.export_schedule).pack(side=tk.LEFT, padx=5)
        ttk.Button(schedule_frame, text="Edit Schedule", command=self.edit_schedule).pack(side=tk.LEFT, padx=5)
    
    def create_report_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Reports")
        
        report_frame = ttk.LabelFrame(tab, text="System Reports", padding=10)
        report_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        ttk.Label(report_frame, text="Select Report Type:").pack(anchor=tk.W)
        
        self.report_var = tk.StringVar()
        reports = [
            "Daily Passenger Count",
            "Train Punctuality",
            "Revenue Analysis",
            "Ticket Sales",
            "System Usage"
        ]
        
        for report in reports:
            ttk.Radiobutton(report_frame, text=report, variable=self.report_var, 
                           value=report).pack(anchor=tk.W)
        
        self.report_var.set(reports[0])
        
        date_frame = ttk.Frame(report_frame)
        date_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(date_frame, text="From:").pack(side=tk.LEFT)
        self.report_from_entry = ttk.Entry(date_frame, width=12)
        self.report_from_entry.pack(side=tk.LEFT, padx=5)
        self.report_from_entry.insert(0, "01/07/2023")
        
        ttk.Label(date_frame, text="To:").pack(side=tk.LEFT)
        self.report_to_entry = ttk.Entry(date_frame, width=12)
        self.report_to_entry.pack(side=tk.LEFT, padx=5)
        self.report_to_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))
        
        ttk.Button(report_frame, text="Generate Report", command=self.generate_report).pack(pady=10)
        

        self.report_text = tk.Text(report_frame, height=10, wrap=tk.WORD)
        self.report_text.pack(fill=tk.BOTH, expand=True)
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    
    def insert_sample_data(self):
        sample_data = [
            ("1", "07:15", "08:45", "EC 173", "1:30", "0", "On time"),
            ("2", "08:00", "10:15", "SC 510", "2:15", "1", "Delayed 10 min"),
            ("3", "09:30", "11:00", "Ex 354", "1:30", "0", "On time"),
            ("4", "10:45", "13:20", "IC 572", "2:35", "2", "On time"),
            ("5", "12:00", "13:15", "Os 8712", "1:15", "0", "Cancelled"),
        ]
        
        for item in sample_data:
            self.tree.insert("", tk.END, text=item[0], values=item[1:])
    
    def search_trains(self):
        from_station = self.from_entry.get()
        to_station = self.to_entry.get()
        date = self.date_entry.get()
        time = self.time_entry.get()
        
        if not from_station or not to_station:
            messagebox.showerror("Error", "Please enter both departure and arrival stations")
            return
        
        messagebox.showinfo("Search", 
                          f"Searching trains from {from_station} to {to_station}\n"
                          f"on {date} at {time}")
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.insert_sample_data()
    
    def buy_ticket(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a train first")
            return
        
        item = self.tree.item(selected)
        train_info = item['values']
        messagebox.showinfo("Buy Ticket", 
                          f"Ticket for train {train_info[2]}\n"
                          f"Departure: {train_info[0]}\n"
                          f"Arrival: {train_info[1]}\n\n"
                          "Proceeding to payment...")
    
    def show_route(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a train first")
            return
        
        item = self.tree.item(selected)
        train_info = item['values']
        
        route_details = f"Route details for train {train_info[2]}:\n\n"
        route_details += f"Departure: {self.from_entry.get()} at {train_info[0]}\n"
        route_details += f"Arrival: {self.to_entry.get()} at {train_info[1]}\n"
        route_details += f"Duration: {train_info[3]}\n"
        route_details += f"Changes: {train_info[4]}\n\n"
        route_details += "Main stops:\n- Praha hl.n.\n- Kolín\n- Pardubice\n- Brno hl.n."
        
        for child in self.notebook.winfo_children():
            if "Real-time Information" in self.notebook.tab(child, "text"):
                for widget in child.winfo_children():
                    if isinstance(widget, tk.Text):
                        widget.delete(1.0, tk.END)
                        widget.insert(tk.END, route_details)
                        self.notebook.select(child)
                        return
    
    def refresh_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.insert_sample_data()
        messagebox.showinfo("Info", "Data refreshed")
    
    def check_train_status(self):
        train_num = self.train_num_entry.get()
        if not train_num:
            messagebox.showwarning("Warning", "Please enter a train number")
            return
        
        status_messages = {
            "173": "EC 173 (Praha - Brno)\nStatus: On time\nExpected departure: 07:15\nPlatform: 5",
            "510": "SC 510 (Praha - Ostrava)\nStatus: Delayed by 15 minutes\nNew departure: 08:15\nPlatform: 1",
            "354": "Ex 354 (Praha - Plzeň)\nStatus: On time\nDeparture: 09:30\nPlatform: 3",
            "572": "IC 572 (Praha - Bratislava)\nStatus: Cancelled\nAlternative: IC 573 at 11:00",
            "8712": "Os 8712 (Praha - Beroun)\nStatus: On time\nDeparture: 12:00\nPlatform: 8"
        }
        
        if train_num in status_messages:
            self.status_text.delete(1.0, tk.END)
            self.status_text.insert(tk.END, status_messages[train_num])
        else:
            self.status_text.delete(1.0, tk.END)
            self.status_text.insert(tk.END, f"No information available for train {train_num}")
    
    def edit_profile(self):
        messagebox.showinfo("Edit Profile", "Profile editing functionality would be implemented here")
    
    def view_tickets(self):
        messagebox.showinfo("View Tickets", "Displaying user's purchased tickets")
    
    def payment_methods(self):
        messagebox.showinfo("Payment Methods", "Managing payment methods")
    
    def make_announcement(self):
        announcement = self.announcement_entry.get()
        if not announcement:
            messagebox.showwarning("Warning", "Please enter an announcement")
            return
        
        station = self.station_entry.get()
        messagebox.showinfo("Announcement Made", 
                          f"Announcement at {station}:\n\n{announcement}")
    
    def update_delay(self):
        train_num = self.delay_train_entry.get()
        delay = self.delay_min_entry.get()
        
        if not train_num or not delay:
            messagebox.showwarning("Warning", "Please enter both train number and delay")
            return
        
        try:
            delay = int(delay)
        except ValueError:
            messagebox.showerror("Error", "Delay must be a number")
            return
        
        messagebox.showinfo("Status Updated", 
                          f"Train {train_num} delay updated to {delay} minutes")
    
    def add_user(self):
        messagebox.showinfo("Add User", "User creation dialog would appear here")
    
    def edit_user(self):
        selected = self.user_tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a user first")
            return
        
        user = self.user_tree.item(selected)
        messagebox.showinfo("Edit User", f"Editing user {user['values'][0]}")
    
    def delete_user(self):
        selected = self.user_tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a user first")
            return
        
        user = self.user_tree.item(selected)
        if messagebox.askyesno("Confirm", f"Delete user {user['values'][0]}?"):
            self.user_tree.delete(selected)
    
    def import_schedule(self):
        messagebox.showinfo("Import Schedule", "Schedule import functionality would be implemented here")
    
    def export_schedule(self):
        messagebox.showinfo("Export Schedule", "Schedule export functionality would be implemented here")
    
    def edit_schedule(self):
        messagebox.showinfo("Edit Schedule", "Schedule editing functionality would be implemented here")
    
    def generate_report(self):
        report_type = self.report_var.get()
        date_from = self.report_from_entry.get()
        date_to = self.report_to_entry.get()
        
        report_content = f"""
        {report_type} Report
        Period: {date_from} to {date_to}
        
        Summary:
        - Total passengers: 12,456
        - Revenue: CZK 1,245,600
        - Most popular route: Praha hl.n. to Brno hl.n.
        - Punctuality: 87.3%
        
        Detailed statistics would be displayed here...
        """
        
        self.report_text.delete(1.0, tk.END)
        self.report_text.insert(tk.END, report_content.strip())

if __name__ == "__main__":
    root = tk.Tk()
    app = CzechTrainSystem(root)
    root.mainloop()