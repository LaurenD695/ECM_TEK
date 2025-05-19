# uses Together.ai to generate data
from together import Together
import xml.etree.ElementTree as ET
import json

file_path = "/Users/laurendipalo/dev/ecm_tek/test.XML"
def read_xml_from_file(file_path):
    with open(file_path, 'r') as f:
        xml_data = f.read()
    return xml_data

client = Together()
def generate_random_values(field_name):
    response = client.chat.completions.create(
        model="marin-community/marin-8b-instruct",
        messages=[
          {
            "role": "user",
            "content": f"Give me a random {field_name} value in a JSON object. One word only per response"
          }
        ]
    )
    return response.choices[0].message.content

def map_fields_to_values(xml_data, fields):
    # Parse the XML data
    root = ET.fromstring(xml_data)

    # Initialize a dictionary to store the field-value mappings
    field_value_dict = {}

    # Loop through the fields and map them to their values
    for field in fields:
        # Try to find the corresponding XML element for each field
        if field in ["Street", "City", "State", "PostalCode", "Country"]:
            # Find the Address element and then look for the nested field
            address = root.find('.//Address')
            if address is not None:
                element = address.find(field)
                field_value_dict[field] = element.text if element is not None else None
            else:
                field_value_dict[field] = None
        else:
            # For non-nested fields, just search at the root level
            element = root.find(f'.//{field}')
            field_value_dict[field] = element.text if element is not None else None

    return field_value_dict


def get_random_field_values(fields):
    random_values = {}
    for field in fields:
        random_value = generate_random_values(field)
        random_values[field] = random_value
    return random_values


def scrub_xml(xml_data, random_values_mapping):
    # Parse the XML data
    root = ET.fromstring(xml_data)

    # Loop through the random values and update the corresponding XML fields
    for field, value in random_values_mapping.items():
        element = root.find(f'.//{field}')
        if element is not None:
            element.text = value  # Update the field with the random value

    # Convert the updated XML back to a string
    updated_xml_data = ET.tostring(root, encoding='unicode', method='xml')
    return updated_xml_data


# Step 1: Read the XML data from the file
xml_data = read_xml_from_file(file_path)

# List of fields to map
fields = ['FirstName', 'LastName', 'DateOfBirth', 'Phone', 'Email', 'Street', 'City', 'State', 'PostalCode', 'Country']

# Step 2: Map the values from the XML data
mapped_values = map_fields_to_values(xml_data, fields)
print("\nMapped XML Values:")
print(json.dumps(mapped_values, indent=2))

# Step 3: Get a random value for each field from ChatGPT
random_field_values = get_random_field_values(fields)
print("\nRandom Values from ChatGPT:")
print(json.dumps(random_field_values, indent=2))

# Step 4: Update the XML with random values
updated_xml_data = scrub_xml(xml_data, random_field_values)
print("\nUpdated XML Data with Random Values:")
print(updated_xml_data)
