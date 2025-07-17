# Hospital Management System

## Overview
The Hospital Management System is a comprehensive application designed to manage patient information, appointments, and billing processes in a hospital setting. This system aims to streamline operations and improve the efficiency of hospital management.

## Project Structure
```
Hospital-Management-System
├── main.py               # Entry point
├── database.py           # Handles DB connections & queries
├── patient.py            # OOP class for Patient
├── appointment.py        # OOP class for Appointment
├── billing.py            # Billing logic
├── gui.py                # Tkinter GUI
└── hospital.db           # SQLite DB file (auto-created)
```

## Features
- **Patient Management**: Add, view, and manage patient information.
- **Appointment Scheduling**: Schedule and manage appointments for patients.
- **Billing**: Calculate bills and generate invoices for services rendered.
- **User-Friendly Interface**: A simple and intuitive GUI built with Tkinter.

## Setup Instructions
1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd Hospital-Management-System
   ```
3. Install the required packages (if any):
   ```
   pip install -r requirements.txt
   ```
4. Run the application:
   ```
   python main.py
   ```

## Usage Guidelines
- Upon running the application, the main GUI will appear.
- Use the patient management section to add new patients and view existing records.
- Schedule appointments through the appointment section.
- Access the billing section to calculate and generate invoices.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.