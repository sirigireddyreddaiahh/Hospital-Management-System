from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Notebook, Style
from database import connect_db, execute_query
from patient import Patient
from appointment import Appointment
from billing import calculate_bill

class HospitalManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("SR Hospitals - Hospital Management System")
        self.root.geometry("1100x650")
        self.root.minsize(900, 550)
        self.style_widgets()
        self.db_conn = connect_db()
        self.create_tables()
        self.create_widgets()

    def style_widgets(self):
        # Modern color palette
        self.bg_color = "#f8fafc"
        self.fg_color = "#22223b"
        self.accent_color = "#1976d2"
        self.button_color = "#1976d2"
        self.button_fg = "#ffffff"
        self.entry_bg = "#ffffff"
        self.entry_fg = "#22223b"
        self.list_bg = "#e3eafc"
        self.error_color = "#e63946"
        self.success_color = "#43aa8b"
        self.root.configure(bg=self.bg_color)
        # Style for ttk Notebook tabs
        style = Style()
        style.theme_use('default')
        style.configure('TNotebook.Tab', font=('Segoe UI', 12, 'bold'), padding=[10, 5], background=self.bg_color)
        style.map('TNotebook.Tab', background=[('selected', self.accent_color)], foreground=[('selected', self.button_fg)])

    def create_widgets(self):
        # Top bar with logo and welcome text
        self.top_frame = Frame(self.root, bg=self.bg_color, height=60)
        self.top_frame.pack(side=TOP, fill=X)
        self.logo_label = Label(self.top_frame, text="🏥", font=("Segoe UI Emoji", 28), bg=self.bg_color)
        self.logo_label.pack(side=LEFT, padx=(20, 10), pady=10)
        self.title_label = Label(self.top_frame, text="Welcome to SR Hospitals", font=("Segoe UI", 22, "bold"), bg=self.bg_color, fg=self.accent_color)
        self.title_label.pack(side=LEFT, pady=10)
        
        # Side menu frame
        self.menu_frame = Frame(self.root, bg=self.bg_color, width=70)
        self.menu_frame.pack(side=LEFT, fill=Y)
        self.menu_frame.pack_propagate(False)

        # Hamburger menu button
        self.menu_button = Button(self.menu_frame, text="☰", font=("Segoe UI", 22), bg=self.bg_color, fg=self.fg_color, bd=0, command=self.toggle_menu, activebackground=self.bg_color, activeforeground=self.accent_color, cursor="hand2")
        self.menu_button.pack(pady=(20, 10))

        # Hidden menu options
        self.menu_options_frame = Frame(self.menu_frame, bg=self.bg_color)
        self.menu_visible = False

        # Menu buttons
        self.home_btn = Button(self.menu_options_frame, text="🏠 Home", font=("Segoe UI", 13), bg=self.bg_color, fg=self.fg_color, bd=0, anchor="w", command=self.show_home, cursor="hand2", activebackground=self.bg_color, activeforeground=self.accent_color)
        self.patient_btn = Button(self.menu_options_frame, text="👤 Patient", font=("Segoe UI", 13), bg=self.bg_color, fg=self.fg_color, bd=0, anchor="w", command=self.show_patient_tab, cursor="hand2", activebackground=self.bg_color, activeforeground=self.accent_color)
        self.appointment_btn = Button(self.menu_options_frame, text="📅 Appointment", font=("Segoe UI", 13), bg=self.bg_color, fg=self.fg_color, bd=0, anchor="w", command=self.show_appointment_tab, cursor="hand2", activebackground=self.bg_color, activeforeground=self.accent_color)
        self.billing_btn = Button(self.menu_options_frame, text="💳 Billing", font=("Segoe UI", 13), bg=self.bg_color, fg=self.fg_color, bd=0, anchor="w", command=self.show_billing_tab, cursor="hand2", activebackground=self.bg_color, activeforeground=self.accent_color)

        self.home_btn.pack(fill=X, pady=2, padx=10)
        self.patient_btn.pack(fill=X, pady=2, padx=10)
        self.appointment_btn.pack(fill=X, pady=2, padx=10)
        self.billing_btn.pack(fill=X, pady=2, padx=10)

        # Main content frame
        self.content_frame = Frame(self.root, bg=self.bg_color)
        self.content_frame.pack(side=LEFT, fill=BOTH, expand=True)

        # Welcome label (Home)
        self.welcome_label = Label(self.content_frame, text="Welcome to SR Hospitals\n\nSelect a section from the menu to get started.", font=("Segoe UI", 22, "bold"), bg=self.bg_color, fg=self.accent_color, justify="center")
        self.welcome_label.pack(expand=True)

        # Tabs (hidden by default)
        self.tab_control = Notebook(self.content_frame)
        self.patient_tab = Frame(self.tab_control, bg=self.bg_color)
        self.appointment_tab = Frame(self.tab_control, bg=self.bg_color)
        self.billing_tab = Frame(self.tab_control, bg=self.bg_color)
        self.tab_control.add(self.patient_tab, text='Patient Management')
        self.tab_control.add(self.appointment_tab, text='Appointment Scheduling')
        self.tab_control.add(self.billing_tab, text='Billing')

        self.setup_patient_tab()
        self.setup_appointment_tab()
        self.setup_billing_tab()

    def toggle_menu(self):
        if self.menu_visible:
            self.menu_options_frame.pack_forget()
            self.menu_visible = False
        else:
            self.menu_options_frame.pack(pady=20, fill=X)
            self.menu_visible = True

    def show_home(self):
        self.tab_control.pack_forget()
        self.welcome_label.pack(expand=True)

    def show_patient_tab(self):
        self.welcome_label.pack_forget()
        self.tab_control.pack(expand=1, fill='both')
        self.tab_control.select(self.patient_tab)

    def show_appointment_tab(self):
        self.welcome_label.pack_forget()
        self.tab_control.pack(expand=1, fill='both')
        self.tab_control.select(self.appointment_tab)

    def show_billing_tab(self):
        self.welcome_label.pack_forget()
        self.tab_control.pack(expand=1, fill='both')
        self.tab_control.select(self.billing_tab)

    def create_tables(self):
        # Create patients table
        query = """
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        );
        """
        execute_query(self.db_conn, query)

        # Create appointments table
        query = """
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY(patient_id) REFERENCES patients(id)
        );
        """
        execute_query(self.db_conn, query)

    def setup_patient_tab(self):
        # Patient registration
        Label(self.patient_tab, text="Patient Name:", bg=self.bg_color, fg=self.fg_color, font=("Segoe UI", 12, "bold")).grid(row=0, column=0, pady=8, sticky="w")
        self.patient_name_entry = Entry(self.patient_tab, bg=self.entry_bg, fg=self.entry_fg, font=("Segoe UI", 12))
        self.patient_name_entry.grid(row=0, column=1, pady=8, padx=8)

        Label(self.patient_tab, text="Age:", bg=self.bg_color, fg=self.fg_color, font=("Segoe UI", 12, "bold")).grid(row=1, column=0, pady=8, sticky="w")
        self.patient_age_entry = Entry(self.patient_tab, bg=self.entry_bg, fg=self.entry_fg, font=("Segoe UI", 12))
        self.patient_age_entry.grid(row=1, column=1, pady=8, padx=8)

        Button(self.patient_tab, text="Add Patient", command=self.add_patient, bg=self.button_color, fg=self.button_fg, font=("Segoe UI", 12, "bold"), cursor="hand2").grid(row=2, columnspan=2, pady=10)

        # Patient search/filter
        Label(self.patient_tab, text="Search by Name:", bg=self.bg_color, fg=self.fg_color, font=("Segoe UI", 12, "bold")).grid(row=3, column=0, pady=8, sticky="w")
        self.search_entry = Entry(self.patient_tab, bg=self.entry_bg, fg=self.entry_fg, font=("Segoe UI", 12))
        self.search_entry.grid(row=3, column=1, pady=8, padx=8)
        Button(self.patient_tab, text="Search", command=self.search_patients, bg=self.button_color, fg=self.button_fg, font=("Segoe UI", 12, "bold"), cursor="hand2").grid(row=3, column=2, pady=8, padx=8)

        # Patient list
        self.patient_listbox = Listbox(self.patient_tab, width=55, bg=self.list_bg, fg=self.fg_color, font=("Segoe UI", 12))
        self.patient_listbox.grid(row=4, column=0, columnspan=3, pady=8, padx=8, sticky="ew")
        self.patient_listbox.bind('<<ListboxSelect>>', self.on_patient_select)

        Button(self.patient_tab, text="Update", command=self.update_patient, bg=self.button_color, fg=self.button_fg, font=("Segoe UI", 12, "bold"), cursor="hand2").grid(row=5, column=0, pady=10)
        Button(self.patient_tab, text="Delete", command=self.delete_patient, bg=self.error_color, fg="#fff", font=("Segoe UI", 12, "bold"), cursor="hand2").grid(row=5, column=1, pady=10)
        self.load_patients()

    def add_patient(self):
        name = self.patient_name_entry.get().strip()
        age = self.patient_age_entry.get().strip()
        if not name or not age or not age.isdigit():
            messagebox.showwarning("Input Error", "Please enter a valid name and age.")
            return
        query = "INSERT INTO patients (name, age) VALUES (?, ?)"
        execute_query(self.db_conn, query, (name, int(age)))
        self.load_patients()
        messagebox.showinfo("Success", "Patient added successfully!")
        self.patient_name_entry.delete(0, END)
        self.patient_age_entry.delete(0, END)

    def load_patients(self):
        self.patient_listbox.delete(0, END)
        query = "SELECT id, name, age FROM patients"
        for row in execute_query(self.db_conn, query):
            self.patient_listbox.insert(END, f"{row[0]}: {row[1]}, Age: {row[2]}")

    def search_patients(self):
        name = self.search_entry.get().strip()
        self.patient_listbox.delete(0, END)
        query = "SELECT id, name, age FROM patients WHERE name LIKE ?"
        for row in execute_query(self.db_conn, query, (f"%{name}%",)):
            self.patient_listbox.insert(END, f"{row[0]}: {row[1]}, Age: {row[2]}")

    def on_patient_select(self, event):
        selection = self.patient_listbox.curselection()
        if selection:
            value = self.patient_listbox.get(selection[0])
            pid, rest = value.split(":", 1)
            name, age = rest.split(", Age: ")
            self.patient_name_entry.delete(0, END)
            self.patient_name_entry.insert(0, name.strip())
            self.patient_age_entry.delete(0, END)
            self.patient_age_entry.insert(0, age.strip())

    def update_patient(self):
        selection = self.patient_listbox.curselection()
        if selection:
            value = self.patient_listbox.get(selection[0])
            pid = value.split(":")[0]
            name = self.patient_name_entry.get().strip()
            age = self.patient_age_entry.get().strip()
            if not name or not age or not age.isdigit():
                messagebox.showwarning("Input Error", "Please enter a valid name and age.")
                return
            query = "UPDATE patients SET name=?, age=? WHERE id=?"
            execute_query(self.db_conn, query, (name, int(age), pid))
            self.load_patients()
            messagebox.showinfo("Success", "Patient updated successfully!")

    def delete_patient(self):
        selection = self.patient_listbox.curselection()
        if selection:
            value = self.patient_listbox.get(selection[0])
            pid = value.split(":")[0]
            query = "DELETE FROM patients WHERE id=?"
            execute_query(self.db_conn, query, (pid,))
            self.load_patients()
            messagebox.showinfo("Success", "Patient deleted successfully!")

    def setup_appointment_tab(self):
        Label(self.appointment_tab, text="Patient ID:", bg=self.bg_color, fg=self.fg_color, font=("Segoe UI", 12, "bold")).grid(row=0, column=0, pady=8, sticky="w")
        self.appointment_patient_id_entry = Entry(self.appointment_tab, bg=self.entry_bg, fg=self.entry_fg, font=("Segoe UI", 12))
        self.appointment_patient_id_entry.grid(row=0, column=1, pady=8, padx=8)

        Label(self.appointment_tab, text="Date (YYYY-MM-DD):", bg=self.bg_color, fg=self.fg_color, font=("Segoe UI", 12, "bold")).grid(row=1, column=0, pady=8, sticky="w")
        self.appointment_date_entry = Entry(self.appointment_tab, bg=self.entry_bg, fg=self.entry_fg, font=("Segoe UI", 12))
        self.appointment_date_entry.grid(row=1, column=1, pady=8, padx=8)

        Button(self.appointment_tab, text="Book Appointment", command=self.book_appointment, bg=self.button_color, fg=self.button_fg, font=("Segoe UI", 12, "bold"), cursor="hand2").grid(row=2, columnspan=2, pady=10)

        self.appointment_listbox = Listbox(self.appointment_tab, width=55, bg=self.list_bg, fg=self.fg_color, font=("Segoe UI", 12))
        self.appointment_listbox.grid(row=3, column=0, columnspan=2, pady=8, padx=8, sticky="ew")
        self.appointment_listbox.bind('<<ListboxSelect>>', self.on_appointment_select)

        Button(self.appointment_tab, text="Edit", command=self.edit_appointment, bg=self.button_color, fg=self.button_fg, font=("Segoe UI", 12, "bold"), cursor="hand2").grid(row=4, column=0, pady=10)
        Button(self.appointment_tab, text="Cancel", command=self.cancel_appointment, bg=self.error_color, fg="#fff", font=("Segoe UI", 12, "bold"), cursor="hand2").grid(row=4, column=1, pady=10)
        self.load_appointments()

    def book_appointment(self):
        patient_id = self.appointment_patient_id_entry.get().strip()
        date = self.appointment_date_entry.get().strip()
        if not patient_id or not date:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return
        query = "INSERT INTO appointments (patient_id, date) VALUES (?, ?)"
        execute_query(self.db_conn, query, (patient_id, date))
        self.load_appointments()
        messagebox.showinfo("Success", "Appointment booked successfully!")
        self.appointment_patient_id_entry.delete(0, END)
        self.appointment_date_entry.delete(0, END)

    def load_appointments(self):
        self.appointment_listbox.delete(0, END)
        query = "SELECT id, patient_id, date FROM appointments"
        for row in execute_query(self.db_conn, query):
            self.appointment_listbox.insert(END, f"{row[0]}: Patient {row[1]}, Date: {row[2]}")

    def on_appointment_select(self, event):
        selection = self.appointment_listbox.curselection()
        if selection:
            value = self.appointment_listbox.get(selection[0])
            aid, rest = value.split(":", 1)
            patient, date = rest.split(", Date: ")
            pid = patient.replace("Patient", "").strip()
            self.appointment_patient_id_entry.delete(0, END)
            self.appointment_patient_id_entry.insert(0, pid)
            self.appointment_date_entry.delete(0, END)
            self.appointment_date_entry.insert(0, date.strip())

    def edit_appointment(self):
        selection = self.appointment_listbox.curselection()
        if selection:
            value = self.appointment_listbox.get(selection[0])
            aid = value.split(":")[0]
            patient_id = self.appointment_patient_id_entry.get().strip()
            date = self.appointment_date_entry.get().strip()
            if not patient_id or not date:
                messagebox.showwarning("Input Error", "Please fill in all fields.")
                return
            query = "UPDATE appointments SET patient_id=?, date=? WHERE id=?"
            execute_query(self.db_conn, query, (patient_id, date, aid))
            self.load_appointments()
            messagebox.showinfo("Success", "Appointment updated successfully!")

    def cancel_appointment(self):
        selection = self.appointment_listbox.curselection()
        if selection:
            value = self.appointment_listbox.get(selection[0])
            aid = value.split(":")[0]
            query = "DELETE FROM appointments WHERE id=?"
            execute_query(self.db_conn, query, (aid,))
            self.load_appointments()
            messagebox.showinfo("Success", "Appointment canceled successfully!")

    def setup_billing_tab(self):
        Label(self.billing_tab, text="Patient ID:", bg=self.bg_color, fg=self.fg_color, font=("Segoe UI", 12, "bold")).grid(row=0, column=0, pady=8, sticky="w")
        self.billing_patient_id_entry = Entry(self.billing_tab, bg=self.entry_bg, fg=self.entry_fg, font=("Segoe UI", 12))
        self.billing_patient_id_entry.grid(row=0, column=1, pady=8, padx=8)

        Label(self.billing_tab, text="Services (comma separated):", bg=self.bg_color, fg=self.fg_color, font=("Segoe UI", 12, "bold")).grid(row=1, column=0, pady=8, sticky="w")
        self.billing_services_entry = Entry(self.billing_tab, bg=self.entry_bg, fg=self.entry_fg, font=("Segoe UI", 12))
        self.billing_services_entry.grid(row=1, column=1, pady=8, padx=8)

        Button(self.billing_tab, text="Calculate Bill", command=self.calculate_bill, bg=self.button_color, fg=self.button_fg, font=("Segoe UI", 12, "bold"), cursor="hand2").grid(row=2, columnspan=2, pady=10)

    def calculate_bill(self):
        patient_id = self.billing_patient_id_entry.get().strip()
        services = [s.strip() for s in self.billing_services_entry.get().split(",") if s.strip()]
        if not patient_id or not services:
            messagebox.showwarning("Input Error", "Please enter patient ID and at least one service.")
            return
        bill = calculate_bill(patient_id, services)
        messagebox.showinfo("Bill", f"Total Bill: ${bill}")

if __name__ == "__main__":
    root = Tk()
    app = HospitalManagementSystem(root)
    root.mainloop()