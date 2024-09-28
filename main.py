import json

def load_json(file_path):
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


json_path = "data.json"

print("Welcome to the note graph terminal!\nIf you are lost type 'help' to print out list of commands \nor type 'exit' to close the terminal")

commands = [
    "'exit' - exits the terminal",
    "'help' - prints out the list of commands",
    "'add node' - adds another node"
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
    else:
        print("If you are lost type 'help' to print out list of commands \nor type 'exit' to close the terminal")



print('Hello')
