import json
import os.path

def create_data_file(file_path):
    f_content = '''{
    "nodes": [],
    "categories": [],
    "nodes_to_categories": [],
    "edges": []
}'''
    try:
        with open(file_path, 'w') as file:
            file.write(f_content)
        print(f"M: Data file created at '{file_path}'")
    except Exception as e:
        print(f"M: Failed to create data file due to \n{e}")

def read_data_file(file_path):
    if not os.path.exists(file_path):
        print(f"M: File at '{file_path}' not found")
        print("M: Creating file...")
        create_data_file(file_path)
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"M: File at '{file_path}' not found")
        return None

def update_data_file(file_path, data, indent = 4):
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=indent)
    except Exception as e:
        print(f"M: Failed to save data file at '{file_path}' due to \n{e}")

def validate_and_fix_data_file(file_path):
    def validate_and_fix_root_element(name_of_element):
        if name_of_element not in data:
            print(f"M: The element '" + name_of_element + f"' not found at '{file_path}'")
            print(f"M: Adding " + name_of_element + "...")
            data[name_of_element] = []
            if name_of_element in data:
                print(f"M: " + name_of_element + " added succesfuly")
            else:
                print(f"M: Failed to add " + name_of_element)

    data = read_data_file(file_path)
    if not isinstance(data, dict):
        print(f"M: The root element should be a dictionary")
    else:
        validate_and_fix_root_element("nodes")
        validate_and_fix_root_element("categories")
        validate_and_fix_root_element("nodes_to_categories")
        validate_and_fix_root_element("edges")

        update_data_file(file_path, data)

# -------- MAIN FUNCTION --------

data_path = "data.json"

print("Checking out the data file...")
validate_and_fix_data_file(data_path)

print("Welcome to the note terminal!")
print("If you are lost type 'help' to get a list of commands")
print("or type 'exit' to close the terminal")

commands = [
    "'help' - prints out the list of commands",
    "'exit' - exits the terminal",
]

answer = ""
while answer != "exit":
    answer = input("---: ")

    if answer == "exit":
        print("closing the terminal...")
    elif answer == "help":
        for c in commands:
            print(c)
    else:
        print("If you are lost type 'help' to get a list of commands")
        print("or type 'exit' to close the terminal")