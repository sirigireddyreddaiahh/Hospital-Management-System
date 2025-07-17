def calculate_bill(patient_id, services):
    base_rate = 100  # Base rate for services
    total_bill = base_rate * len(services)
    return total_bill

def generate_invoice(patient_id, services, total_bill):
    invoice = f"Invoice for Patient ID: {patient_id}\n"
    invoice += "Services Provided:\n"
    for service in services:
        invoice += f"- {service}\n"
    invoice += f"Total Bill: ${total_bill}\n"
    return invoice