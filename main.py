import json
import os.path

def create_data_file(f_file_path):
    content = '''{
    "nodes": [],
    "categories": [],
    "nodes_to_categories": [],
    "edges": []
}'''
    try:
        with open(f_file_path, 'w') as file:
            file.write(content)
        print(f"M: Data file created at '{f_file_path}'")
    except Exception as e:
        print(f"M: Failed to create data file due to \n{e}")

def read_data_file(f_file_path):
    if not os.path.exists(f_file_path):
        print(f"M: File at '{f_file_path}' not found")
        print(f"M: Creating file...")
        create_data_file(f_file_path)
    try:
        with open(f_file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"M: File at '{f_file_path}' not found")
        return None

def update_data_file(f_file_path, f_data, f_indent = 4):
    try:
        with open(f_file_path, 'w') as file:
            json.dump(f_data, file, indent=f_indent)
    except Exception as e:
        print(f"M: Failed to save data file at '{f_file_path}' due to \n{e}")

def validate_and_fix_data_file(f_file_path):
    def validate_and_fix_root_element(name_of_element):
        if name_of_element not in data:
            print(f"M: The element '" + name_of_element + f"' not found at '{f_file_path}'")
            print(f"M: Adding " + name_of_element + "...")
            data[name_of_element] = []
            if name_of_element in data:
                print(f"M: " + name_of_element + " added succesfuly")
            else:
                print(f"M: Failed to add " + name_of_element)

    data = read_data_file(f_file_path)
    if not isinstance(data, dict):
        print(f"M: The root element should be a dictionary")
    else:
        validate_and_fix_root_element("nodes")
        validate_and_fix_root_element("categories")
        validate_and_fix_root_element("nodes_to_categories")
        validate_and_fix_root_element("edges")

        update_data_file(f_file_path, data)

def find_next_id(f_data, f_list_name):
    i = 0
    for elem in f_data[f_list_name]:
        i = max(int(elem["id"]), i)
    i += 1
    return i

def create_category(f_file_path, f_repeat = True):
    data = read_data_file(f_file_path)

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

        if f_repeat:
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

    update_data_file(f_file_path, data)

    data = read_data_file(f_file_path)

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

def create_node(f_file_path):
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
            for elemx in data["categories"]:
                if elemx["title"] == category_title:
                    title_exists = True
                    category_ids.append(elemx["id"])
                    break

            if title_exists:
                print(f"M: Category '{category_title}' added succesfuly!")
            else:
                print(f"M: Category '{category_title}' could not be added")
    data = read_data_file(f_file_path)

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

    if distinct_category:

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

        update_data_file(f_file_path, data)
    else:
        node_category = {
            "node_id" : node["id"],
            "category_id" : 0
        }

        root_categ_exists = False
        for obj in data["categories"]:
            if obj["id"] == 0:
                root_categ_exists = True
                break

        if not root_categ_exists:
            data["categories"].append({"id" : 0, "title" : "root"})

        data["nodes_to_categories"].append(node_category)
        update_data_file(f_file_path, data)

def create_edge(f_file_path):
    data = read_data_file(f_file_path)
    source_node = input("Enter the title of source node: ")
    target_node = input("Enter the title of target node: ")

    if source_node == target_node:
        print("M: You can not connect one node to itself!")
        return

    relations = [
        "(1) dual",
        "(2) optional",
        "(3) required"
    ]
    while True:
        print("What type of relation do you want to implement?")
        for elem in relations:
            print(elem)

        ans = int(input())

        if 0 < ans < len(relations):
            break
    relation_name = relations[ans - 1]
    relation_name = relation_name[4:]

    source_exist = False
    target_exist = False

    source_id = 0
    target_id = 0

    for elem in data["nodes"]:
        if elem["title"] == source_node:
            source_exist = True
            source_id = elem["id"]
            continue
        elif elem["title"] == target_node:
            target_exist = True
            target_id = elem["id"]
            continue
        if source_exist and target_exist:
            break
    if target_exist and source_exist:
        print("M: Source node and target node found!")

        edge = {
            "id" : find_next_id(data, "edges"),
            "source_node_id" : source_id,
            "target_node_id" : target_id,
            "relation_type" : relation_name
        }
        data["edges"].append(edge)
        update_data_file(f_file_path, data)

    else:
        if not source_exist:
            print("M: Source node does not exist")
        if not target_exist:
            print("M: Target node does not exist")
        return
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
    "'create node' - creates a node",
    "'create category' - creates a category",
    "'create edge' - creates an edge between nodes"
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
    elif answer == "create edge":
        create_edge(data_path)
    else:
        print("If you are lost type 'help' to get a list of commands")
        print("or type 'exit' to close the terminal")