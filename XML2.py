#uses faker to generate data
import json
from faker import Faker
import xml.etree.ElementTree as ET

# take in list of field names
# find field names in XML and map values
# generate dummy data JSON obj format
# replace old data with dummy data

#step 1: read data from XML file as a string and store in variable
file_path = "/Users/laurendipalo/dev/ecm_tek/test.XML"
def read_xml_from_file(file_path):
    with open(file_path, 'r') as f:
        xml_data = f.read()
    return xml_data

#step 2: map fieldnames (keys) to values
def map_fields_to_values(xml_data, field_names: list):
    # Parse the XML data
    root = ET.fromstring(xml_data)

    # Initialize a dictionary to store the field-value mappings
    field_value_dict = {}

    # Loop through the fields and map them to their values
    for field in field_names:
        # Try to find the corresponding XML element for each field
        element = root.find(f'.//{field}')
        if element is not None:
            field_value_dict[field] = element.text
        else:
            field_value_dict[field] = None  # In case the field is not found in the XML

    return field_value_dict

#step 3: generate fake data
fake = Faker()
def generate_random_values() -> dict[str, str]:
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


#step 4: "scrub" document/replace data with fake data
def scrub_xml(xml_data: str, random_values: dict[str, str]):
    # Parse the XML data
    root = ET.fromstring(xml_data)

    # Loop through the random values and update the corresponding XML fields
    for field, value in random_values.items():
        element = root.find(f'.//{field}')
        if element is not None:
            element.text = value  # Update the field with the random value

    # Convert the updated XML back to a string
    # print(xml_data)
    updated_xml_data = ET.tostring(root, encoding='unicode', method='xml')

    return updated_xml_data


# Step 1: Read the XML data from the file
xml_data = read_xml_from_file(file_path)
# List of fields to map
fields = ['FirstName', 'LastName', 'DateOfBirth', 'SSN', 'Phone', 'Email', 'Street', 'City', 'State', 'PostalCode', 'Country']

# Step 2: Map the values from the XML data
mapped_values = map_fields_to_values(xml_data, fields)
# print("\nMapped XML Values:")
print(json.dumps(mapped_values, indent=2))

# Step 3: Get a random value for each field
random_values = generate_random_values()
# print("\nRandom Values from Faker")
print(json.dumps(random_values, indent=2))

# Step 4: Update the XML with random values
updated_xml_data = scrub_xml(xml_data, random_values)
print(updated_xml_data)

