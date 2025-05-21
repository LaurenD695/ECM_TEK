#uses faker to generate data
import json
from faker import Faker
import xml.etree.ElementTree as ET
fake = Faker()
# take in list of field names
# find field names in XML and map values
# generate dummy data JSON obj format
# replace old data with dummy data

#func: read data from XML file as a string and store in variable
file_path = "/Users/laurendipalo/dev/ecm_tek/test.XML"
def read_xml_from_file(file_path):
    try:
        with open(file_path, 'r') as f:
            xml_data = f.read()
            f.close()
    except FileNotFoundError:
        print("File not found")
    except Exception as e:
        print(f"Error: {e}")
    return xml_data

#func: generate fake data
def generate_random_values(fields: list[str]) -> dict[str, str]:
    return  {
        "F_name": fake.first_name(),
        "FirstName": fake.first_name(),
        "LastName": fake.last_name(),
        "DateOfBirth": fake.date_of_birth(minimum_age=18, maximum_age=90).isoformat(),
        "SSN": fake.ssn(),
        "Phone": fake.phone_number(),
        "Email": fake.email(),
        "Street": fake.street_address(),
        "City": fake.city(),
        "State": fake.state_abbr(),
        "PostalCode": fake.zipcode(),
        "Country": fake.country()
    }


#func: "scrub" document/replace data with fake data
def scrub_xml(xml_data: str, random_values: dict[str, str]):
    # Parses the XML data from a string into an element
    root = ET.fromstring(xml_data)

    # Loop through the random values and update the corresponding XML fields
    for field, value in random_values.items():
        element = root.find(f'.//{field}')
        if element is not None:
            element.text = value  # Update the field with the random value

    # Convert the updated XML back to a string
    return ET.tostring(root, encoding='unicode', method='xml')

# Step 1: Read the XML data from the file
xml_data = read_xml_from_file(file_path)
# List of fields to map
fields = ['FirstName', 'LastName', 'DateOfBirth', 'SSN', 'Phone', 'Email', 'Street', 'City', 'State', 'PostalCode', 'Country']
# Step 2: generate random values given list of fields, then use return values and plug into scrub function
# Step 3: store scrubbed xml as updated xml (temp print statement to ensure it works, how should i return the updated file?)
updated_xml_data = scrub_xml(xml_data, generate_random_values(fields))
print(updated_xml_data)

