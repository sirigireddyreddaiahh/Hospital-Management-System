class Appointment:
    def __init__(self, appointment_id, patient_id, date):
        self.appointment_id = appointment_id
        self.patient_id = patient_id
        self.date = date

    def schedule_appointment(self):
        # Logic to schedule the appointment in the database
        pass

    def get_appointment_details(self):
        return {
            "appointment_id": self.appointment_id,
            "patient_id": self.patient_id,
            "date": self.date
        }