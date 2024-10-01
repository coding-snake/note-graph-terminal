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


def find_next_id(data, list_name):
    i = 0
    for elem in data[list_name]:
        i = max(int(elem["id"]), i)
    i += 1
    return i

def create_category(file_path, repeat = True):
    data = read_data_file(file_path)

    if data is None:
        print('M: Data could not be loaded')
        return


    category_list = []
    loop_active = True
    while loop_active:
        category = {
            "id" : find_next_id(data, "categories")
        }

        title = ""
        while title == "":
            title = input("Enter the title: ")
            if title == "":
                print("M: Title can not be empty!")

        category["title"] = title
        category_list.append(category)

        if repeat:
            while True:
                print("Would you like to add another category? (Y/n)")
                ans = input()

                if ans == "Y":
                    break
                elif ans == "n":
                    loop_active = False
                    break
                else:
                    continue
        else:
            loop_active = False

    for elem in category_list:
        data["categories"].append(elem)

    update_data_file(file_path, data)

    data = read_data_file(file_path)

    for elem in category_list:
        success = False
        for obj in data["categories"]:
            if elem["title"] == obj["title"]:
                print(f"M: Category {elem["title"]} added succesfuly")
                success = True
                break
        if success:
            print("M: Category added succesfuly")
        else:
            print("M: Category could not be added")

def create_node(file_path):
    def add_category():
        category_title = input("Enter the title: ")
        title_exists = False
        for categ in data["categories"]:
            if categ["title"] == category_title:
                title_exists = True
                category_ids.append(categ["id"])
                break

        if title_exists:
            print(f"M: Category '{category_title}'found")
        else:
            print(f"M: Category '{category_title}' NOT found")
            print(f"M: Creating category '{category_title}'...")

            category = {
                "id": find_next_id(data, "categories"),
                "title": category_title
            }
            data["categories"].append(category)

            title_exists = False
            for categ in data["categories"]:
                if categ["title"] == category_title:
                    title_exists = True
                    category_ids.append(categ["id"])
                    break

            if title_exists:
                print(f"M: Category '{category_title}' added succesfuly!")
            else:
                print(f"M: Category '{category_title}' could not be added")
    data = read_data_file(file_path)

    if data is None:
        print("M: Data could not be loaded")
        return

    node = {"id": find_next_id(data, "nodes")}

    title = ""
    while title == "":
        title = input("Enter the title: ")
        if title == "":
            print("M: Title can not be empty!")

    node["title"] = title

    data["nodes"].append(node)

    while True:
        print("Would you like to add category? (Y/n)")
        ans = input()
        if ans == "Y":
            distinct_category = True
            break
        else:
            distinct_category = False
            break

    update_data_file(file_path, data)

    if distinct_category:

        data = read_data_file(file_path)
        category_ids = []

        add_category()

        while True:
            print("Would you like to add another category? (Y/n)")
            ans = input()

            if ans == "Y":
                add_category()
            elif ans == "n":
                break
            else:
                continue

        for elem in category_ids:
            node_category = {
                "node_id" : node["id"],
                "category_id" : elem
            }

            data["nodes_to_categories"].append(node_category)

        update_data_file(file_path, data)
    else:
        data = read_data_file(file_path)
        node_category = {
            "node_id" : node["id"],
            "category_id" : 0
        }
        data["nodes_to_categories"].append(node_category)
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
    "'create node' - created a node",
    "'create category' - create a category"
]

answer = ""
while answer != "exit":
    answer = input("---: ")

    if answer == "exit":
        print("closing the terminal...")
    elif answer == "help":
        for c in commands:
            print(c)
    elif answer == "create node":
        create_node(data_path)
    elif answer == "create category":
        create_category(data_path)
    else:
        print("If you are lost type 'help' to get a list of commands")
        print("or type 'exit' to close the terminal")