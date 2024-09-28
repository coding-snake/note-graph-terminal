import json
import os.path

def create_default_json(file_path):
    default_content = '''[
    {
        "id": 0,
        "title": "root-node",
        "type": "default",
        "categ": [],
        "req-prev": [],
        "prev": [],
        "next": [],
        "opt": []
    }
]'''
    try:
        with open(file_path, 'w') as file:
            file.write(default_content)
        print(f"M: Json file created at '{file_path}'")
    except Exception as e:
        print(f"M: Failed to create json file due to {e}")



def load_json(file_path):

    if not os.path.exists(file_path):
        print(f"M: File at '{file_path}' not found")
        print(f"Creating file...")
        create_default_json(file_path)
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"M: File at '{file_path}' not found")
        return None

def save_json(file_path, data):
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"M: Failed to save data to '{file_path}' due to {e}")

def find_new_id(data):
    f_id = 0
    for obj in data:
        f_id = int(max(int(obj["id"]), f_id))
    f_id += 1

    return f_id

def query_attr(message_comp, message_or = "leave blank and press Enter to finish"):
    list_obj = []
    while True:
        tmp = input("Add a " + message_comp + " (or " + message_or + "): ")
        if tmp == "":
            break
        list_obj.append(tmp)
    return list_obj


def new_node(file_path):
    data = load_json(file_path)

    if data is None:
        print("M: Data could not be loaded")
        return

    new_id = find_new_id(data)

    ans = ""
    while ans == "":
        ans = input("Enter the title: ")
        if ans == "":
            print("M: Title can not be empty!")

    new_title = ans

    new_type = input("Enter type of node (or press enter to chose 'base'): ")
    if new_type == "":
        new_type = "base"

    new_categ = query_attr("category")
    new_req_prev = query_attr("required previous node")
    new_prev = query_attr("other previous node")
    new_next = query_attr("next node")
    new_opt = query_attr("optional node")

    new_base_node = {
        "id" : new_id,
        "title" : new_title,
        "type" : new_type,
        "categ" : new_categ,
        "req-prev" : new_req_prev,
        "prev" : new_prev,
        "next" : new_next,
        "opt" : new_opt
    }

    data.append(new_base_node)
    save_json(file_path, data)
    print(f"M: New node added succesfully! \nid: {new_id} \ntitle: {new_title}")

def add_rel(file_path):
    data = load_json(file_path)

    if data is None:
        print("M: Data could not be loaded")
        return

    while True:
        first_id = int(input("Enter id of first node: "))

        first_node = None
        for elem in data:
            if elem["id"] == first_id:
                first_node = elem
                break

        if first_node:
            print(f"Note of an id {first_id}: {first_node["title"]}")
            break
        else:
            print(f"Note with id {first_id} not found!")

    options = [
        "1) required previous",
        "2) previous",
        "3) next",
        "4) optional"
    ]

    while True:
        print("What relation would you like to add?")
        for elem in options:
            print(elem)
        f_answer = int(input("---: "))

        if 1 <= f_answer <= 4:
            break

    while True:
        second_id = int(input("Enter id of second node: "))

        second_node = None
        for elem in data:
            if elem["id"] == second_id:
                second_node = elem
                break

        if first_node:
            print(f"Note of an id {second_id}: {second_node["title"]}")
            break
        else:
            print(f"Note with id {second_id} not found!")

    if f_answer == 1:
        print(f"The node {first_id}: {first_node["title"]}\nin a relation REQUIRED PREVIOUS with\nnode {second_id}: {second_node["title"]}")
        first_node["req-prev"].append(second_id)
        second_node["next"].append(first_id)
    elif f_answer == 2:
        print(
            f"The node {first_id}: {first_node["title"]}\nin a relation PREVIOUS with\nnode {second_id}: {second_node["title"]}")
        first_node["prev"].append(second_id)
        second_node["next"].append(first_id)
    elif f_answer == 3:
        print(
            f"The node {first_id}: {first_node["title"]}\nin a relation NEXT with\nnode {second_id}: {second_node["title"]}")
        first_node["next"].append(second_id)
        print("For the second node is this a relation REQUIRED PREVIOUS? (Y/n)")

        tmp = ""
        while tmp != "Y" and tmp != "n":
            tmp = input()

        if tmp == "Y":
            second_node["req-prev"].append(first_id)
        else:
            second_node["prev"].append(first_id)
    elif f_answer == 4:
        print(
            f"The node {first_id}: {first_node["title"]}\nin a relation OPTIONAL with\nnode {second_id}: {second_node["title"]}")
        first_node["opt"].append(second_id)

    save_json(file_path, data)
    print(f"Nodes: \n{first_id} : {first_node["title"]} \n{second_id} : {second_node["title"]}\n UPDATED SUCCESFULLY")
json_path = "data.json"

print("Welcome to the note graph terminal!\nIf you are lost type 'help' to print out list of commands \nor type 'exit' to close the terminal")

commands = [
    "'exit' - exits the terminal",
    "'help' - prints out the list of commands",
    "'add node' - adds another node",
    "'add relation' - adds relation between two elements"
]

answer = ""
while answer != "exit":
    answer = input("---: ")

    if answer == "exit":
        continue
    elif answer == "help":
        for c in commands:
            print(c)
    elif answer == "add node":
        new_node(json_path)
    elif answer == "add relation":
        add_rel(json_path)
    else:
        print("If you are lost type 'help' to print out list of commands \nor type 'exit' to close the terminal")



print('Hello')
