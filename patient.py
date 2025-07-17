class Patient:
    def __init__(self, patient_id, name, age):
        self.patient_id = patient_id
        self.name = name
        self.age = age

    def add_patient(self, db_connection):
        query = "INSERT INTO patients (id, name, age) VALUES (?, ?, ?)"
        db_connection.execute_query(query, (self.patient_id, self.name, self.age))

    def get_patient_info(self):
        return {
            "id": self.patient_id,
            "name": self.name,
            "age": self.age
        }