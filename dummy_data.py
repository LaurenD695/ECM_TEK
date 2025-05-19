# tests faker
import json
from faker import Faker

fake = Faker()

def generate_random_values():
    random_values = {
        "FirstName": [fake.first_name() for _ in range(10)],
        "LastName": [fake.last_name() for _ in range(10)],
        "DateOfBirth": [fake.date_of_birth(minimum_age=18, maximum_age=90).isoformat() for _ in range(10)],
        "SSN": [fake.ssn() for _ in range(10)],
        "Phone": [fake.phone_number() for _ in range(10)],
        "Email": [fake.email() for _ in range(10)],
        "Street": [fake.street_address() for _ in range(10)],
        "City": [fake.city() for _ in range(10)],
        "State": [fake.state_abbr() for _ in range(10)],
        "PostalCode": [fake.zipcode() for _ in range(10)],
        "Country": [fake.country() for _ in range(10)]
    }

    return random_values

random_data = generate_random_values()
json_data = json.dumps(random_data, indent=2)

