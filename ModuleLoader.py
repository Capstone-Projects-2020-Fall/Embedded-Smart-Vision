import json


def read_module_list():
    print("Loading module List...")
    with open("module_list.json") as read_file:
        module_list = json.load(read_file)
        print(module_list)
        # TODO create module object for each module loaded and pass it pack as an array
