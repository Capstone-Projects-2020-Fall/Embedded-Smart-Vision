# Contains information for reading in the general configuration as well as saving and updating config variables

import json


# Wrapper class to contain the information about a config update we want to do
class cfg_update:
    def __init__(self, key, data):
        # Which key do we want to access
        self.key = key
        # What do we want to set it to
        self.data = data


class Config:
    def __init__(self):
        self.vars = {}
        self.config_path = "config.json"

    def print_vars(self):
        print(self.vars)

    def set_var(self, data: cfg_update):
        print(data.key)
        if data.key in self.vars:
            # if the key in the data is a valid variable
            self.vars[data.key] = data.data
            with open(self.config_path, 'w') as outFile:
                json.dump(self.vars, outFile)

    def load_config(self):
        print("Loading configuration...")
        with open(self.config_path) as read_file:
            self.vars = json.load(read_file)
