# uses Together.ai to generate data
from together import Together
import xml.etree.ElementTree as ET
import json
import re
import argparse
import sys


parser = argparse.ArgumentParser()
parser.add_argument('filepath', help='path to XML file')
parser.add_argument('fields', nargs='+', help='list of field names to scrub')
args = parser.parse_args()

file_path = args.filepath
print(f"Filepath: {file_path}")
fields = args.fields
print(f"Fieldnames: {fields}")

#func: read data from XML file as a string and store in variable
def read_xml_from_file(file_path):
    try:
        with open(file_path, 'r') as f:
            xml_data = f.read()
    except FileNotFoundError:
        print("File not found")
    except Exception as e:
        print(f"Error: {e}")
    return xml_data

#func: map values from og xml
def map_xml_values(xml_data, fields):
    root = ET.fromstring(xml_data)
    key_values = {}

    def handle_nested_tags(element):
        for child in element:
            # checks if child tag is found in fields -> if yes, stores value
            if child.tag in fields and child.tag not in key_values:
                key_values[child.tag] = child.text.strip() if child.text else None
            # handles nested tags (i.e address -> city, state, etc)
            if len(child):
                handle_nested_tags(child)
    handle_nested_tags(root)
    return key_values

#func: generate fake data using LLM passing in field names as parameter
#problem: LLM response formatting "incorrectly" so made a function to clean up response and only extract info i need
#working on finding a better solution than just regex-ing whenever LLM acts up
client = Together()
def clean_and_parse_json(llm_output):
    cleaned = re.sub(r"^(?:```|''')\s*json\s*|^(?:```|''')\s*|\s*(?:```|''')\s*$", "", llm_output.strip(), flags=re.IGNORECASE)
    return json.loads(cleaned)

def generate_random_values(original_data):
    response = client.chat.completions.create(
        model="marin-community/marin-8b-instruct",
        messages=[
          {
            "role": "user",
            "content": (
                "Generate a valid JSON object with realistic fake values for the keys in the following original object:\n"
                f"{original_data}\n"
                "Follow these instructions:\n"
                " Values must be different from those in the original data."
                " Keys must be the same as the ones in the original data"
                "- Phone numbers must be formatted as '###-###-####'.\n"
                "Respond with only one JSON object, nothing else."
                "- You MUST avoid including any text, explanation, markdown, or code blocks.\n"
                "- You MUST output only a valid JSON object. No extra characters or formatting.\n"
            )

          }
        ]
    )
    return clean_and_parse_json(response.choices[0].message.content)

def retry_fake_data(original_data, max_retries=3):
    error = None
    for retry in range(max_retries):
        try:
            fake_data = generate_random_values(original_data)
            if not determine_if_same(original_data, fake_data):
                return fake_data
        except Exception as e:
            error = e
            max_retries -= 1
            pass
    print(f"LLM failed to generate unique data:\n{error}")
    return None

def determine_if_same(original_data, fake_data):
    for key, original_value in original_data.items():
        fake_value = fake_data.get(key)
        if original_value == fake_value:
            return True
    return False

def scrub_xml(xml_data, fake_data):
    # parses XML data
    root = ET.fromstring(xml_data)
    # Loop through the random values and update the corresponding XML fields
    for field, value in fake_data.items():
        for element in root.findall(f'.//{field}'):
            if element is not None:
                element.text = value  # updates the field with the random value
    # Convert the updated XML back to a string
    updated_xml_data = ET.tostring(root, encoding='unicode', method='xml')
    return updated_xml_data


# Step 1: Read the XML data from the file
xml_data = read_xml_from_file(file_path)
print("Original XML")
print(xml_data)

# Step 2: map original XML values to dictionary
original_values = map_xml_values(xml_data, fields)
print("\nMapped Original XML Values:")
print(json.dumps(original_values, indent=2))

#included check to ensure that intended number of fields were mapped
if len(original_values) != len(args.fields):
    print(f"[!] Error: The number of fields provided ({len(args.fields)}) does not match the number of mapped fields from XML ({len(original_values)}).")
    print(f"Fields: {args.fields}")
    print(f"Original Values: {list(original_values.keys())}")
    sys.exit(1)

# Step 3: Get a random value for each field from LLM/clean it up so that it is formatted properly
random_field_values = retry_fake_data(original_values)
print("\nRandom Values from LLM:")
print(json.dumps(random_field_values, indent=2))


# Step 4: Update the XML with random values
updated_xml_data = scrub_xml(xml_data, random_field_values)
print("\nUpdated XML Data with Random Values:")
print(updated_xml_data)
