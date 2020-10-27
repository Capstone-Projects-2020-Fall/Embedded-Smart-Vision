# Contains information for reading in the general configuration as well as saving and updating config variables

import json


class Config:
    def __init__(self):
        self.vars = {}
        self.config_path = "config.json"

    def print_vars(self):
        print(self.vars)

    def set_var(self, key, data):
        self.vars[key] = data

    def load_config(self):
        print("Loading configuration...")
        with open(self.config_path) as read_file:
            self.vars = json.load(read_file)
