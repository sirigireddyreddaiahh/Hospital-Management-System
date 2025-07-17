import tkinter as tk
from tkinter import messagebox
from database import connect_db
from gui import HospitalManagementSystem  # <-- Change here

def main():
    # Initialize the database connection
    conn = connect_db()
    if conn is None:
        messagebox.showerror("Database Error", "Failed to connect to the database.")
        return

    # Set up the GUI
    root = tk.Tk()
    root.title("Hospital Management System")
    app = HospitalManagementSystem(root)  # <-- Change here
    
    # Start the GUI event loop
    root.mainloop()

if __name__ == "__main__":
    main()